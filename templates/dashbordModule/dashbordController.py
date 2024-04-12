import os
from flask_login import login_required
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
import ssl
import smtplib
import random
import string
from flask import send_file
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from models import LogsInicio, Usuarios
from email.message import EmailMessage

from models import db,Login, DetalleVenta, Venta
from sqlalchemy import func

bcrypt = Bcrypt()

@login_required
def dashbord():
    masVendido = db.session.query(func.count(DetalleVenta.nombreGalleta), DetalleVenta.nombreGalleta)\
                      .group_by(DetalleVenta.nombreGalleta)\
                      .order_by(func.count(DetalleVenta.nombreGalleta).desc())\
                      .limit(1)\
                      .all()
    ventaDia = db.session.query(func.sum(Venta.total)).scalar()
    
    return render_template('dashbordModule/dashbord.html',masVendido = masVendido , ventaDia= ventaDia) 

@login_required
def ventaDia():

    ventaDia = db.session.query(func.sum(Venta.total)).scalar()
    
    return render_template('dashbordModule/dashbord.html', ventaDia= ventaDia) 

@login_required
def descargar_logs():
    registros_logs = LogsInicio.query.all()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)    
    tabla_datos = [['Nombre', 'Fecha', 'Hora', 'Estatus']] 
    for log in registros_logs:
        usuario = Usuarios.query.get(log.idUsuario)
        nombre_usuario = usuario.nombre if usuario else 'Desconocido' 
        tabla_datos.append([nombre_usuario, log.fecha, log.hora, log.estatus])
    
    tabla = Table(tabla_datos)
    estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    tabla.setStyle(estilo_tabla)
    elementos = [tabla]
    doc.build(elementos)
    buffer.seek(0)    
    nombre_archivo = 'logs.pdf'
    return send_file(buffer, as_attachment=True, download_name=nombre_archivo)