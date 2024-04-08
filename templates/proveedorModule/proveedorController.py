from flask import Flask,render_template, request
import re
from flask import flash,redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from datetime import datetime,timedelta
from models import db
from models import Proveedor
from sqlalchemy import func
import forms
import secrets
from datetime import datetime
from sqlalchemy import text

csrf=CSRFProtect()
app=Flask(__name__)
app.config.from_object(DevelopmentConfig)

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

def proveedores():
    proveedor_form = forms.ProveForm(request.form)
    proveedores = Proveedor.query.filter_by(estatus='activo').all()
    
    if request.method=='POST' and proveedor_form.validate():
        try:
                razon_social = sanitize_input(proveedor_form.razonSocial.data)
                nombre_proveedor = sanitize_input(proveedor_form.nombreP.data)

                prove = Proveedor(razonSocial=razon_social, nombreP=nombre_proveedor, estatus='Activo')
                db.session.add(prove)                    
                db.session.commit()
                flash('El proveedor ha sido agregado exitosamente.', 'error')
                proveedor_form = forms.ProveForm()
                
        except Exception as e:
                print(f"Error en la base de datos: {e}")
                db.session.rollback()
    return render_template('proveedorModule/proveedor.html', form=proveedor_form,proveedor=proveedores)


def eliminar_proveedor(proveedor_id):
    proveedor = Proveedor.query.get(proveedor_id)
    if proveedor:
        try:
            proveedor.estatus = 'Inactivo'  # Cambiar el estado del proveedor
            db.session.commit()
            flash('El proveedor ha sido eliminado exitosamente.', 'success')
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
            flash('Error al eliminar el proveedor.', 'error')
    else:
        flash('Proveedor no encontrado.', 'error')

    return redirect('/proveedores')


