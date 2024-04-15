import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
import ssl
import smtplib
import random
import string
from email.message import EmailMessage
from models import Login
from models import db
bcrypt = Bcrypt()

#PASSWORD DE GOOGLE PARA PODER HACER LA VERIFICACIONES Y RECUPERAR
passwordCorreo = "uhiv hvpi sebw xukk"
email_sender = "cristianleyvacr7@gmail.com"

# TOKEN PARA VERIFICACION
def generar_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#TOKEN ARA REUPERAR CONTRASEÑA
def generar_token2():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

#FUNCIO PARA ENVIAR CORREO DE VERIFICACION DE DOS PASOS
def enviar_correo(email, token):
    subject = "Validacion de dos pasos"
    body = f"""
        Recibes este correo electrónico porque hemos detectado un intento de inicio de sesión en tu cuenta. Para garantizar la seguridad de tu cuenta, hemos implementado un sistema de verificación de dos pasos.

        Si no has intentado acceder a tu cuenta recientemente, te recomendamos encarecidamente que cambies tu contraseña inmediatamente y tomes medidas adicionales para proteger tu cuenta.

        Por otro lado, si has intentado iniciar sesión, utiliza el siguiente código de verificación de dos pasos para acceder a tu cuenta de forma segura:

        Tu código de verificación de dos pasos es: {token}

        Por favor, ingresa este código en la página de inicio de sesión para completar el proceso de verificación.

        Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en ponerte en contacto con nuestro equipo de soporte.
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, passwordCorreo)
        smtp.sendmail(email_sender, email, em.as_string())

# FUNCION DEL LOGIN
def vistaLogin():
    return render_template('loginModule/login.html') 
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        usuario = Login.query.filter_by(correo=correo).first()
        if usuario:
            token = generar_token()
            usuario.token = token
            db.session.commit()            
            enviar_correo(correo, token)            
            return redirect(url_for('verificar_token'))
        else:
            flash("Correo electrónico o contraseña incorrectos", "error")
            return render_template('loginModule/login.html')
        
    return render_template('loginModule/login.html')

#FUNCION DE VISTA DE VERIFICACION DE TOKEN
def verificar_token():
    if request.method == 'POST':
        correo = request.form['correo']
        token = request.form['token']
        usuario = Login.query.filter_by(correo=correo, token=token).first()
        if usuario:
            return redirect(url_for('dashbord'))
        else:
            flash("Correo electrónico o token incorrectos", "error")
            return render_template('loginModule/verificar_token.html')
    return render_template('loginModule/verificar_token.html')

#CORREO PARA RECUERAR CONTRASEÑA
def enviar_correo_restauracion(email, token):
    subject = "Restablecimiento de contraseña - Don Galleto"
    body = f"""
        Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Don Galleto.
        Si no realizaste esta solicitud, puedes ignorar este correo electrónico y tu contraseña permanecerá sin cambios.

        Para restablecer tu contraseña, haz clic en el siguiente enlace o cópialo y pégalo en tu navegador:

        {url_for('restablecer_contrasena', token=token, _external=True)}

        Si tienes alguna pregunta o necesitas asistencia, no dudes en ponerte en contacto con nuestro equipo de soporte.

        ¡Gracias!
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, passwordCorreo)
        smtp.sendmail(email_sender, email, em.as_string())

# PRIMERA PANTALLA CUANDO VAS A RECUPERAR CONTRASEÑA
def olvidar_contrasena():
    if request.method == 'POST':
        correo = request.form['correo']
        usuario = Login.query.filter_by(correo=correo).first()
        if usuario:
            token = generar_token2() 
            usuario.token = token
            db.session.commit()
            enviar_correo_restauracion(correo, token) 
            flash("Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.", "success")
            return redirect(url_for('login'))
        else:
            flash("No se encontró ninguna cuenta asociada a ese correo electrónico.", "error")
    return render_template('loginModule/olvidar_contrasena.html')

# FUNCION PARA CONFIRMAR TU CONTRASEÑA
def restablecer_contrasena(token):
    usuario = Login.query.filter_by(token=token).first()
    if usuario:
        if request.method == 'POST':
            nueva_contrasena = request.form['nueva_contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            if nueva_contrasena == confirmar_contrasena:
                hashed_password = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
                usuario.contrasenia = hashed_password
                usuario.token = None 
                db.session.commit()
                flash("Tu contraseña ha sido restablecida correctamente. Ahora puedes iniciar sesión con tu nueva contraseña.", "success")
                return redirect(url_for('login'))
            else:
                flash("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", "error")
                return render_template('restablecer_contrasena.html', token=token)
        return render_template('restablecer_contrasena.html', token=token)
    else:
        flash("El enlace de restablecimiento de contraseña no es válido o ha expirado.", "error")
        return redirect(url_for('login'))

# INICIO

def dashbord():
    return render_template('dashbordModule/dashbordController.html') 

