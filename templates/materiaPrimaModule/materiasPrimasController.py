from flask import Flask,render_template, request
import re
from flask import flash,redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from datetime import datetime,timedelta
from models import db
from models import Proveedor,MateriaPrimas, CompraMateriaPrima, InventarioMateriaPrima,MermaMateriaPrima
from sqlalchemy import func
import forms
import secrets
from datetime import datetime
from sqlalchemy import text



#por que queremos trabajar con ese
from flask import render_template, request
from flask import request
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload

caracteresEspeciales = re.compile(r'[^a-zA-Z0-9\s]')

def sanitize_input(input_str):
    # Eliminar caracteres especiales usando la expresión regular
    return caracteresEspeciales.sub('', input_str)

def maPrimas():
    materia_form = forms.MateForm(request.form)
    materias = MateriaPrimas.query.filter_by(estatus='Pagado').all()
    
    if request.method == 'POST':
        try:
            nombre_materia = sanitize_input(materia_form.nombreMa.data)
            materia = MateriaPrimas(tipoPro=materia_form.tipoPro.data, nombreMa=nombre_materia, estatus='Disponible')
            db.session.add(materia)                    
            db.session.commit()
            flash('La materia prima ha sido agregada exitosamente.', 'error')
            materias = MateriaPrimas.query.all()
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
    return render_template('materiaPrimaModule/maPrimas.html', form=materia_form, materia=materias)

def eliminar_materia(materia_id):
    materia = MateriaPrimas.query.get(materia_id)
    if materia:
        try:
            # Cambiar el estatus de la materia prima a 'Inactivo' en lugar de 'Proveedor'
            materia.estatus = 'Inactivo'
            db.session.commit()
            flash('La materia prima ha sido eliminada exitosamente.', 'success')  # Corregir el mensaje de éxito
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
            flash('Error al eliminar la materia prima.', 'error')
    else:
        flash('Materia prima no encontrada.', 'error')

    return redirect('/maPrimas')


def comprarMateriasPrimas():
    
    compraMateria_form = forms.CompraMateForm(request.form)
    compras = db.session.query(
        CompraMateriaPrima.costo,
        CompraMateriaPrima.cantidad,
        CompraMateriaPrima.fechaCompra,
        Proveedor.nombreP,
        MateriaPrimas.nombreMa
    ).join(
        Proveedor, CompraMateriaPrima.idProveedor == Proveedor.idProveedor
    ).join(
        MateriaPrimas, CompraMateriaPrima.idMP == MateriaPrimas.idMP
    ).all()
    proveedores = Proveedor.query.all()  
    opciones_proveedor = [(proveedor.idProveedor, proveedor.nombreP) for proveedor in proveedores]
    compraMateria_form.proveedor.choices = opciones_proveedor
    
    materiaprima = MateriaPrimas.query.all()  
    opciones_materia = [(materia.idMP, materia.nombreMa) for materia in materiaprima]
    compraMateria_form.materia.choices = opciones_materia

    if request.method == 'POST':
        try:
            cantidad = 0
            fecha_compra = datetime.now()  # Obtener la fecha actual
            fecha_caducidad = compraMateria_form.fechaCaducidad.data
            cantidad =  int(compraMateria_form.cantidad.data)
            presentacion = compraMateria_form.presentacion.data
            print(type(compraMateria_form.cantidad.data))
            print("Cantidad:", cantidad)
            print("Presentacion:", presentacion)
            
            cantidadInventario = 0  
            orale=5
            
            if presentacion == 'Galones':
              cantidadInventario = 3.78 * cantidad
              print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Medios galones':
                cantidadInventario = 1.89 * (cantidad)
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Litros':
                cantidadInventario = 1 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Costal':
                cantidadInventario = 10 * (cantidad)
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Medio costal':
                cantidadInventario = orale * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Kilos':
                cantidadInventario = 1 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Pieza':
                cantidadInventario = 1 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Caja de 12 piezas':
                cantidadInventario = 12 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Caja de 6 piezas':
                cantidadInventario = 6 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Cartera de 12 piezas':
                cantidadInventario = 12 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Cartera de 18 piezas':
                cantidadInventario = 18 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Cartera de 30 piezas':
                cantidadInventario = 30 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Cartera de 90 piezas':
                cantidadInventario = 90 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
            elif presentacion == 'Cartera de 360 piezas':
                cantidadInventario = 360 * cantidad
                print("Cantidad de inventario para Galones:", cantidadInventario)
                
            print(cantidadInventario)
            cantidad_es = f"{cantidad} {presentacion}"
            print(type(cantidadInventario))
            compra = CompraMateriaPrima(idMP=compraMateria_form.materia.data, idProveedor=compraMateria_form.proveedor.data, 
                                        costo=compraMateria_form.costo.data, cantidad=cantidad_es, estatus='Pedido', idUsuario = 2)
            db.session.add(compra)      
            
            # Llamar al procedimiento almacenado para insertar la compra y el inventario
            
            
            db.session.commit()

            flash('La compra ha sido agregada exitosamente.', 'success')
            compras = db.session.query(
                CompraMateriaPrima.costo,
                CompraMateriaPrima.cantidad,
                CompraMateriaPrima.fechaCompra,
                Proveedor.nombreP,
                MateriaPrimas.nombreMa
            ).join(
                Proveedor, CompraMateriaPrima.idProveedor == Proveedor.idProveedor
            ).join(
                MateriaPrimas, CompraMateriaPrima.idMP == MateriaPrimas.idMP
            ).all()
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()

    return render_template('materiaPrimaModule/comprarMateriasPrimas.html', form=compraMateria_form, compraMateria=compras)



def inventarioMateriasPrimas():
    iventarioMateria_form = forms.InvenMateForm(request.form)
    inventario = db.session.query(
        InventarioMateriaPrima.fechaCaducidad,
        InventarioMateriaPrima.idMPI,
        CompraMateriaPrima.fechaCompra,
        CompraMateriaPrima.costo,
        InventarioMateriaPrima.cantidad,
        MateriaPrimas.nombreMa,
        Proveedor.nombreP
    ).join(
        CompraMateriaPrima, InventarioMateriaPrima.idCMP == CompraMateriaPrima.idCMP
    ).join(
        MateriaPrimas, CompraMateriaPrima.idMP == MateriaPrimas.idMP
    ).join(
        Proveedor, CompraMateriaPrima.idProveedor == Proveedor.idProveedor
    ).all()
    
    
    return render_template('materiaPrimaModule/inventarioMateriasPrimas.html', form=iventarioMateria_form, inventario=inventario)



def eliminar_inventario(inventario_id):
    # Obtener el registro de inventario correspondiente al inventario_id
    inventario = InventarioMateriaPrima.query.get(inventario_id)
    
    # Verificar si el inventario existe
    if inventario:
        try:
            # Cambiar el estado del inventario a "Eliminado" (o similar)
            inventario.estatus = "Eliminado"
            
            # Obtener los detalles del inventario para el ID dado
            inventario_detalles = db.session.query(
                InventarioMateriaPrima.fechaCaducidad,
                InventarioMateriaPrima.idMPI,
                CompraMateriaPrima.fechaCompra,
                CompraMateriaPrima.costo,
                InventarioMateriaPrima.cantidad,
                MateriaPrimas.nombreMa,
                MateriaPrimas.idMP,
                Proveedor.nombreP
            ).join(
                CompraMateriaPrima, InventarioMateriaPrima.idCMP == CompraMateriaPrima.idCMP
            ).join(
                MateriaPrimas, CompraMateriaPrima.idMP == MateriaPrimas.idMP
            ).join(
                Proveedor, CompraMateriaPrima.idProveedor == Proveedor.idProveedor
            ).filter(InventarioMateriaPrima.idMPI == inventario_id).all()
            
            # Crear un nuevo registro de merma para el inventario eliminado
            nueva_merma = MermaMateriaPrima(
                idMP=inventario_detalles[0].idMP,
                idMPI=inventario_detalles[0].idMPI,
                costo=inventario_detalles[0].costo,
                descripcion="Inventario eliminado",  # Puedes agregar una descripción estática o personalizada
                estatus="Eliminado",  # Opcional: establecer el estado de la merma
                idUsuario=2,  # Reemplaza usuario_actual con el usuario real
                fecha=datetime.now()  # Obtener la fecha actual
            )
            
            # Agregar la nueva merma a la base de datos
            db.session.add(nueva_merma)
            
            # Guardar los cambios en la base de datos
            db.session.commit()
            
            flash('El inventario ha sido eliminado exitosamente.', 'success')
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
            flash('Error al eliminar el inventario.', 'error')
    else:
        flash('Inventario no encontrado.', 'error')

    return redirect("/inventarioMateriasPrimas")
