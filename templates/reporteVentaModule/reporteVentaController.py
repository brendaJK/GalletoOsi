from flask import Flask,render_template, request, jsonify
import re
from flask import flash,redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from datetime import datetime,timedelta
from models import db
from models import Venta
from sqlalchemy import func
import forms
import secrets
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import extract


def reporte_venta():
    inventario = Venta.query.all()
    return render_template('reporteVentaModule/reporteVenta.html', inventario=inventario)

def obtener_ventas_por_mes(mes):
    # Consulta las ventas para el mes dado
    ventas = Venta.query.filter(extract('month', Venta.fecha) == mes).all()
    return ventas

def obtener_ventas_por_dia(dia):
    # Consulta las ventas para el día dado
    ventas = Venta.query.filter(extract('day', Venta.fecha) == dia).all()
    return ventas

from flask import Flask,render_template, request, jsonify
import re
from flask import flash,redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from datetime import datetime,timedelta
from models import db
from models import Venta
from sqlalchemy import func
import forms
import secrets
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import extract


def reporte_venta():
    inventario = Venta.query.all()
    return render_template('reporteVentaModule/reporteVenta.html', inventario=inventario)

def obtener_ventas_por_mes(mes):
    # Consulta las ventas para el mes dado
    ventas = Venta.query.filter(extract('month', Venta.fecha) == mes).all()
    return ventas

def obtener_ventas_por_dia(dia):
    # Mapeo de nombres de días de la semana a números de día de la semana
    dias_semana = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }

    # Obtener el número de día de la semana
    num_dia_semana = dias_semana.get(dia.lower())

    if num_dia_semana is None:
        return []  # Si el valor no corresponde a un día de la semana, retornar una lista vacía
    
    # Calcular la fecha correspondiente al día de la semana actual
    hoy = datetime.now()
    fecha_dia_semana = hoy - timedelta(days=hoy.weekday() - num_dia_semana)

    # Consultar las ventas para la fecha calculada
    ventas = Venta.query.filter(func.date(Venta.fecha) == fecha_dia_semana.date()).all()
    return ventas

def filtrar_y_imprimir():
    venta = forms.ReporteVentaForm(request.form)
    
    valor_seleccionado = venta.tipo.data
    if valor_seleccionado is None:
        flash('Debe seleccionar un mes o un día.', 'error')
        return redirect('/reporte_venta')

    valor_seleccionado = valor_seleccionado.lower()
    print("Valor seleccionado:", valor_seleccionado)
    
    # Mapeo de nombres de meses a números de mes
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    # Verificar si el valor seleccionado es un mes
    if valor_seleccionado in meses.keys():
        valor_mes = meses[valor_seleccionado]
        # Realizar la consulta de ventas por mes
        ventas = obtener_ventas_por_mes(valor_mes)
        print(ventas)
    # Verificar si el valor seleccionado es un día
    elif valor_seleccionado in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']:
        # Realizar la consulta de ventas por día
        ventas = obtener_ventas_por_dia(valor_seleccionado)
        print(ventas)
    else:
        # Valor seleccionado no reconocido
        flash('El valor seleccionado no es válido.', 'error')
        return redirect('/reporte_venta')
    
    # Verificar si se encontraron ventas
    if not ventas:
        flash('No se encontraron ventas para el valor seleccionado.', 'warning')
    
    # Renderizar la plantilla con las ventas obtenidas
    return render_template('reporteVentaModule/reporteVenta.html', inventario=ventas)
