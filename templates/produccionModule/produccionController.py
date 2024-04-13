from flask import render_template, request, redirect, url_for,flash
from flask_login import login_required
import re
from models import db
import forms
from models import Produccion,Producto

caracteresEspeciales = re.compile(r'[^a-zA-Z0-9\s]')
@login_required
def produccion():

    print('Si jala jaja.')

    return render_template('produccionModule/produccion.html')


@login_required
def sanitize_input(input_str):
    # Eliminar caracteres especiales usando la expresión regular
    return caracteresEspeciales.sub('', input_str)
@login_required
def productos():
    producto_form = forms.ProductoForm(request.form)
    productos = Producto.query.all()
    
    if request.method=='POST' and producto_form.validate():
        try:
                nombre = sanitize_input(producto_form.nombre.data)
                produc = Producto(nombre= nombre, estatus='Activo')
                db.session.add(produc)                    
                db.session.commit()
                flash('El producto ha sido agregado exitosamente.', 'error')
                
                
        except Exception as e:
                print(f"Error en la base de datos: {e}")
                db.session.rollback()
    return render_template('produccionModule/productos.html', form=producto_form,producto=productos)