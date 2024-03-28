from flask import render_template, request, redirect, url_for
from models import db
import forms
from models import Venta

def venta():
    form = forms.VentasForm()  # Crea una instancia del formulario
    return render_template('ventasModule/venta.html', form=form)  # Pasa el formulario al renderizar la plantilla



def guardar_venta():
    if request.method == 'POST':
        ventas_clase = forms.VentasForm(request.form)
        nombre_cliente = ventas_clase.nombreCliente.data
        tipo_venta = ventas_clase.tipoVenta.data
        cantidad = ventas_clase.cantidad.data
        tipo_galleta = ventas_clase.tipoGalleta.data
        nueva_venta = Venta(nombre=nombre_cliente, tipo=tipo_venta, cantidad=cantidad, tipo_galleta=tipo_galleta)
        db.session.add(nueva_venta)
        db.session.commit()
        return redirect(url_for('ventaModule.venta'))
    else:
       
        ventas_clase = forms.VentasForm()

    return render_template('ventasModule/venta.html', form=ventas_clase)
# TODO arreglar despues de qeu las tablas en la base de datos esten creadas
