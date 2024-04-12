import os
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
import ssl
import smtplib
import random
import string
from email.message import EmailMessage
from models import Usuarios, LogsInicio
from models import db
from flask_login import current_user
from datetime import datetime
import asyncio

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

# Función para registrar la entrada en logs_inicio
def registrar_entrada(idUsuario):
    nueva_entrada = LogsInicio(idUsuario=idUsuario, fecha=datetime.now().date(), hora=datetime.now().time(), estatus='Entro')
    db.session.add(nueva_entrada)
    db.session.commit()

# Función para registrar la salida en logs_inicio
def registrar_salida(idUsuario):
    nueva_salida = LogsInicio(idUsuario=idUsuario, fecha=datetime.now().date(), hora=datetime.now().time(), estatus='Salio')
    db.session.add(nueva_salida)
    db.session.commit()
        
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        usuario = Usuarios.query.filter_by(correo=correo).first()
        if usuario:
            if usuario.intentos_fallidos >= 3:
                flash("Tu cuenta ha sido bloqueada debido a demasiados intentos fallidos. Por favor, ponte en contacto con el administrador.", "error")
                return render_template('loginModule/login.html')
            if check_password_hash(usuario.contrasenia, contrasenia):
                token = generar_token()
                usuario.token = token
                usuario.intentos_fallidos = 0
                login_user(usuario)
                db.session.commit()
                enviar_correo(correo, token)
                return redirect(url_for('verificar_token'))
            else:
                usuario.intentos_fallidos += 1 
                db.session.commit()
                flash("Correo electrónico o contraseña incorrectos. Intento fallido número {}.".format(usuario.intentos_fallidos), "error")
                return render_template('loginModule/login.html')
        else:
            flash("Correo electrónico o contraseña incorrectos", "error")
            return render_template('loginModule/login.html')
        
    return render_template('loginModule/login.html')

#FUNCION DE VISTA DE VERIFICACION DE TOKEN
def verificar_token():
    if request.method == 'POST':
        correo = request.form['correo']
        token = request.form['token']
        usuario = Usuarios.query.filter_by(correo=correo, token=token).first()
        if usuario:
            session['rol'] = usuario.rol
            registrar_entrada(current_user.id)
            if session['rol'] == 'Administrador':
                return redirect(url_for('dashbord'))
            if session['rol'] == 'Empleado':
                return redirect(url_for('venta'))
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
        usuario = Usuarios.query.filter_by(correo=correo).first()
        if usuario:
            token = generar_token2() 
            usuario.token = token
            db.session.commit()
            enviar_correo_restauracion(correo, token) 
            flash("Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.", "success")
            return redirect(url_for('vistaLogin'))
        else:
            flash("No se encontró ninguna cuenta asociada a ese correo electrónico.", "error")
    return render_template('loginModule/olvidar_contrasena.html')

# FUNCION PARA CONFIRMAR TU CONTRASEÑA
def restablecer_contrasena(token):
    usuario = Usuarios.query.filter_by(token=token).first()
    if usuario:
        if request.method == 'POST':
            confirmar_contrasena = request.form['confirmar_contrasena']
            with open('static/validaciones.txt', 'r') as file:
                contraseñas_inseguras = file.read().splitlines()
            if confirmar_contrasena in contraseñas_inseguras:
                flash("La contraseña es demasiado insegura. Por favor, elija una contraseña más segura.", "error")
                return render_template('loginModule/restablecer_contrasena.html', token=token)
            
            if len(confirmar_contrasena) < 8 or not any(c.isupper() for c in confirmar_contrasena) \
                or not any(c.islower() for c in confirmar_contrasena) or not any(c.isdigit() for c in confirmar_contrasena):
                flash("La contraseña debe tener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula y un número.", "error")
                return render_template('loginModule/restablecer_contrasena.html', token=token)            
            
            if len(confirmar_contrasena) < 8 or not any(c.isupper() for c in confirmar_contrasena) \
                or not any(c.islower() for c in confirmar_contrasena) or not any(c.isdigit() for c in confirmar_contrasena):
                flash("La contraseña de confirmación debe tener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula y un número.", "error")
                return render_template('loginModule/restablecer_contrasena.html', token=token)
            
            hashed_password = bcrypt.generate_password_hash(confirmar_contrasena).decode('utf-8')
            usuario.contrasenia = hashed_password
            usuario.token = None 
            db.session.commit()
            flash("Tu contraseña ha sido restablecida correctamente. Ahora puedes iniciar sesión con tu nueva contraseña.", "success")
            return redirect(url_for('vistaLogin'))
        
        return render_template('loginModule/restablecer_contrasena.html', token=token)
    else:
        flash("El enlace de restablecimiento de contraseña no es válido o ha expirado.", "error")
        return redirect(url_for('vistaLogin'))


# INICIO

@login_required
def dashbord():
    return render_template('dashbordModule/dashbordController.html') 

@login_required
def logout():
    registrar_salida(current_user.id)
    logout_user()
    return redirect(url_for('vistaLogin'))