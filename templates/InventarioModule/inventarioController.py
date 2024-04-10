from flask import render_template, request, redirect, url_for
from models import db
from datetime import datetime, timedelta
import forms
from models import Produccion, Usuarios, Recetas, RecetaDetalle
from sqlalchemy import text, func
import re


def Inventario ():

    galletasInv = db.session.query(
    Produccion.nombreGalleta,
    func.sum(Produccion.cantidadProducida).label('stock'),
    func.avg(Produccion.costoProduccion).label('costoPromedioProduccion')
    ).filter(Produccion.Estatus == 'Disponible').group_by(Produccion.nombreGalleta).all()

    for resultado in galletasInv:
        print(resultado.nombreGalleta, resultado.stock, resultado.costoPromedioProduccion)

    return render_template('InventarioModule/Inventario.html', Inv = galletasInv)