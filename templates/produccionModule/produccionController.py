from flask import render_template, request, redirect, url_for
from models import db
from datetime import datetime, timedelta
import forms
from models import Produccion, Usuarios

def produccion():

    return render_template('produccionModule/produccion.html')

def guardarProduccion():

    create_form = forms.produccionForm(request.form)

    if request.method == 'POST':


        #costoProd = #Se necesita calcular

        idUs = db.session.query(Usuarios.idUsuario).filter(Usuarios.nombre.like('%Mario%')).scalar()

        #costoProd = create_form.costoProduccion.data
        fechaProd = datetime.now()
        #fechaCad = create_form.fechaCaducidad.data

        prod = Produccion(
            #costoProduccion = costoProd,
            #fechaProduccion = fechaProd,
            #fechaCaducidad = fechaCad

            fechaProduccion = fechaProd,
            costoProduccion = '',
            fechaCaducidad = fechaProd + timedelta(days=10),
            idUsuario = idUs
        )
        db.session.add(prod)
        db.session.commit()


        print('Operacion realizada.')


    return render_template('produccionModule/produccion.html')