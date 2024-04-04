from flask import render_template, request, redirect, url_for
from models import db

import forms
from models import Produccion

def produccion():

    return render_template('produccionModule/produccion.html')

def guardarProduccion():

    create_form = forms.produccionForm(request.form)

    if request.method == 'POST':
        costoProd = create_form.costoProduccion.data
        fechaProd = create_form.fechaProduccion.data
        fechaCad = create_form.fechaCaducidad.data

        prod = Produccion(
            costoProduccion = costoProd,
            fechaProduccion = fechaProd,
            fechaCaducidad = fechaCad
        )
        db.session.add(prod)
        db.session.commit()


    return 