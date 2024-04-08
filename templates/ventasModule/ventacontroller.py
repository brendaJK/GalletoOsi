from flask import render_template, request, redirect, url_for, current_app, jsonify
from models import db
from sqlalchemy import text, update 
import forms
from models import Venta, Caja, DetalleVenta,Produccion
from datetime import datetime


def venta():
    sql = text("""
        SELECT idReceta, nombreProducto, MIN(idProduccion) AS idProduccion, 
               SUM(cantiadadProducida) AS total_cantidad_producida,
               AVG(costoProduccion / cantiadadProducida) AS costo_por_unidad
        FROM produccion
        GROUP BY idReceta, nombreProducto;
    """)
    result = db.session.execute(sql)
    produccion = result.fetchall()

    margen_beneficio = 0.5  
    productos_con_precio_venta = []
    
    for producto in produccion:
        costo_por_unidad = producto.costo_por_unidad
        precio_venta_por_unidad = costo_por_unidad * (1 + margen_beneficio)
        producto_con_precio_venta = {
            "idReceta": producto.idReceta,
            "nombreProducto": producto.nombreProducto,
            "idProduccion": producto.idProduccion,
            "total_cantidad_producida": producto.total_cantidad_producida,
            "costo_por_unidad": costo_por_unidad,
            "precio_venta_por_unidad": precio_venta_por_unidad
        }
        productos_con_precio_venta.append(producto_con_precio_venta)

    return render_template('ventasModule/venta.html', produccion=productos_con_precio_venta)


def actualizar_caja():
    try:
        monto_recibido = float(request.form['montoRecibido'])
        total_venta = float(request.form['totalVenta'])
        saldo_actual = db.session.query(Caja).first().dineroCaja 
        total = saldo_actual + monto_recibido
        cambio = monto_recibido - total_venta

        nuevo_saldo = total - cambio
        db.session.query(Caja).update({'dineroCaja': nuevo_saldo})
        db.session.commit()

        return jsonify({'success': True, 'cambio': cambio})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def confirmar_venta():
    data = request.get_json() 
    detalles_venta = data['detallesVenta']
    total_venta = data['totalVenta']
    cantidad_vendida_total = 0

    for detalle in detalles_venta:
        if detalle['tipoVenta'] == 'gramo':
            cantidad_comprada_gramos = detalle['cantidad']
            cantidad_comprada_galletas = calcular_cantidad_galletas(cantidad_comprada_gramos)
        elif detalle['tipoVenta'] == 'caja':
            cantidad_cajas = detalle['cantidad']
            cantidad_comprada_galletas = cantidad_cajas * 20  # Cada caja contiene 20 galletas
        elif detalle['tipoVenta'] == 'unidad':
            cantidad_comprada_galletas = detalle['cantidad']
        else:
            return jsonify({'error': 'Tipo de venta no reconocido'}), 400

        producciones_galletas = Produccion.query.filter_by(nombreProducto=detalle['tipoGalleta'], Estatus='En proceso').filter(Produccion.cantiadadProducida > 0).order_by(Produccion.fechaProduccion).all()
        cantidad_comprada_galletas_restantes = cantidad_comprada_galletas

        for produccion in producciones_galletas:
            cantidad_disponible = produccion.cantiadadProducida
            if cantidad_disponible >= cantidad_comprada_galletas_restantes:
                produccion.cantiadadProducida -= cantidad_comprada_galletas_restantes
                cantidad_comprada_galletas_restantes = 0
                cantidad_vendida_total += cantidad_comprada_galletas
                break  
            else:
                cantidad_comprada_galletas_restantes -= cantidad_disponible
                produccion.cantiadadProducida = 0
                cantidad_vendida_total += cantidad_disponible

        if cantidad_comprada_galletas_restantes > 0:
            for produccion in producciones_galletas:
                cantidad_disponible = produccion.cantiadadProducida
                if cantidad_disponible > 0:
                    if cantidad_disponible >= cantidad_comprada_galletas_restantes:
                        produccion.cantiadadProducida -= cantidad_comprada_galletas_restantes
                        cantidad_comprada_galletas_restantes = 0
                        cantidad_vendida_total += cantidad_comprada_galletas_restantes
                    else:
                        cantidad_comprada_galletas_restantes -= cantidad_disponible
                        produccion.cantiadadProducida = 0
                        cantidad_vendida_total += cantidad_disponible
                    break  

    # Crear detalles de venta
    detalles_insertados = []
    for detalle in detalles_venta:
        nuevo_detalle = DetalleVenta(
            subtotal=detalle['subtotal'],
            tipoVenta=detalle['tipoVenta'],
            cantidad=detalle['cantidad'],
            nombreGalleta=detalle['tipoGalleta'],
            idVenta=None  # No asignar ID de venta aquí
        )
        detalles_insertados.append(nuevo_detalle)

    
    # Crear la venta
    nueva_venta = Venta(
        fecha=str(datetime.now()),
        total=total_venta,
        cantidadVendida=cantidad_vendida_total,
        idCaja=1,
        idUsuario=1  # Asigna el ID de usuario correspondiente
    )
    nueva_venta.detallesVenta.extend(detalles_insertados)


    # Agregar la nueva venta a la sesión y hacer commit para insertarla en la base de datos
    db.session.add(nueva_venta)
    db.session.commit()
   
    return jsonify({'message': 'Datos de venta procesados correctamente'}), 200










def calcular_cantidad_galletas(cantidad_gramos):
    peso_por_galleta = 25  # Peso promedio de cada galleta en gramos
    cantidad_galletas = cantidad_gramos // peso_por_galleta
    return cantidad_galletas
