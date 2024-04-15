from flask import render_template, request, redirect, url_for, current_app, jsonify
from models import db
from sqlalchemy import text, update 
import forms
from models import Venta, Caja, DetalleVenta, CompraMateriaPrima, Proveedor, MateriaPrimas, InventarioMateriaPrima, InventarioGalletas,Productos
from datetime import datetime


def venta():
    # Actualizar el estado a "Agotado" si la cantidadStock es 0
    actualizar_estado_agotado()
    
    try:
        # Consulta para obtener el precio de venta y la cantidad total producida de cada galleta en stock
        precios_venta = db.session.query(InventarioGalletas.nombreGalleta.label('nombreProducto'),
                                          db.func.sum(InventarioGalletas.cantidadStock).label('total_cantidad_producida'),
                                          Productos.precio_venta).\
                                          join(Productos, InventarioGalletas.nombreGalleta == Productos.nombre).\
                                          filter(InventarioGalletas.Estatus == 'En stock').\
                                          group_by(InventarioGalletas.nombreGalleta, Productos.precio_venta).all()

        return render_template('ventasModule/venta.html', produccion=precios_venta)
    except Exception as e:
        # Manejar errores si hay algún problema con la consulta
        return f"Error al obtener los datos de venta: {str(e)}"
def actualizar_estado_agotado():
    try:
       
        db.session.query(InventarioGalletas).filter(InventarioGalletas.cantidadStock == 0).update({InventarioGalletas.Estatus: 'Agotado'})
        db.session.commit() 
        return "Se actualizó el estado correctamente."
    except Exception as e:
        db.session.rollback() 
        return f"Error al actualizar el estado: {str(e)}"


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

        producciones_galletas = InventarioGalletas.query.filter_by(nombreGalleta=detalle['tipoGalleta'], Estatus='En stock').filter(InventarioGalletas.cantidadStock > 0).order_by(InventarioGalletas.fechaProduccion).all()
        cantidad_comprada_galletas_restantes = cantidad_comprada_galletas

        for produccion in producciones_galletas:
            cantidad_disponible = produccion.cantidadStock
            if cantidad_disponible >= cantidad_comprada_galletas_restantes:
                produccion.cantidadStock -= cantidad_comprada_galletas_restantes
                cantidad_comprada_galletas_restantes = 0
                cantidad_vendida_total += cantidad_comprada_galletas
                break  
            else:
                cantidad_comprada_galletas_restantes -= cantidad_disponible
                produccion.cantidadStock = 0
                cantidad_vendida_total += cantidad_disponible

        if cantidad_comprada_galletas_restantes > 0:
            for produccion in producciones_galletas:
                cantidad_disponible = produccion.cantidadStock
                if cantidad_disponible > 0:
                    if cantidad_disponible >= cantidad_comprada_galletas_restantes:
                        produccion.cantidadStock -= cantidad_comprada_galletas_restantes
                        cantidad_comprada_galletas_restantes = 0
                        cantidad_vendida_total += cantidad_comprada_galletas_restantes
                    else:
                        cantidad_comprada_galletas_restantes -= cantidad_disponible
                        produccion.cantidadStock = 0
                        cantidad_vendida_total += cantidad_disponible
                    break  

 
    detalles_insertados = []
    for detalle in detalles_venta:
        nuevo_detalle = DetalleVenta(
            subtotal=detalle['subtotal'],
            tipoVenta=detalle['tipoVenta'],
            cantidad=detalle['cantidad'],
            nombreGalleta=detalle['tipoGalleta'],
            idVenta=None  
        )
        detalles_insertados.append(nuevo_detalle)

    
    nueva_venta = Venta(
        fecha=str(datetime.now()),
        total=total_venta,
        cantidadVendida=cantidad_vendida_total,
        idCaja=1,
        idUsuario=1 
    )
    nueva_venta.detallesVenta.extend(detalles_insertados)


   
    db.session.add(nueva_venta)
    db.session.commit()
   
    return jsonify({'message': 'Datos de venta procesados correctamente'}), 200

def calcular_cantidad_galletas(cantidad_gramos):
    peso_por_galleta = 25  # Peso promedio de cada galleta
    cantidad_galletas = cantidad_gramos // peso_por_galleta
    return cantidad_galletas

def proveedorpago():
        compras = db.session.query(
        CompraMateriaPrima.idCMP,
        Proveedor.razonSocial,
        MateriaPrimas.nombreMa,
        CompraMateriaPrima.costo,
        CompraMateriaPrima.cantidad,
        CompraMateriaPrima.estatus
    ).join(Proveedor, CompraMateriaPrima.idProveedor == Proveedor.idProveedor
    ).join(MateriaPrimas, CompraMateriaPrima.idMP == MateriaPrimas.idMP
    ).filter(CompraMateriaPrima.estatus == 'Pedido'
    ).all()

        return render_template('ventasModule/pagoProveedor.html', compras=compras)


def pagoMateriaPrima():
    data = request.get_json()
    idCMP = data['idCMP']
    totalPagar = float(data['totalPagar'])
    fecha_caducidad = datetime.strptime(data['fechaCaducidad'], '%Y-%m-%d')

    inventario = InventarioMateriaPrima.query.filter_by(idCMP=idCMP).first()
    inventario.fechaCaducidad = fecha_caducidad
    inventario.estatus = "Disponible"
    db.session.commit()

    compra = CompraMateriaPrima.query.get(idCMP)
    compra.estatus = 'Pagado'
    db.session.commit()

    caja = Caja.query.first() 
    caja.dineroCaja -= totalPagar
    db.session.commit()

    return jsonify({'message': 'Pago realizado correctamente'}), 200

def rechazoMateriaPrima():
    data = request.get_json()
    idCMP = data['idCMP']
    totalPagar = float(data['totalPagar'])
    estatus = data['estatus']

    compra = CompraMateriaPrima.query.get(idCMP)
    compra.estatus = estatus
    db.session.commit()

    inventario = InventarioMateriaPrima.query.filter_by(idCMP=idCMP).first()
    inventario.fechaCaducidad = datetime.now()
    inventario.estatus = "Rechazado"
    db.session.commit()

    return jsonify({'message': 'Pago realizado correctamente'}), 200


def agregarDinero():
    data = request.get_json()
    monto = data.get('monto')

    if monto is None:
        return jsonify({'error': 'Falta el monto'}), 400

    try:
        monto = float(monto)
    except ValueError:
        return jsonify({'error': 'El monto debe ser un número válido'}), 400
    
    caja = Caja.query.first()  
    if caja:
        caja.dineroCaja += monto
        db.session.commit()
        return jsonify({'message': f'Se han agregado ${monto} a la caja correctamente'}), 200
    else:
        return jsonify({'error': 'No se encontró la caja'}), 404

