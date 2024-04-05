import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import ssl
import smtplib
import random
import string
from email.message import EmailMessage

app = Flask(__name__)
load_dotenv()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#CONECCION A BASE DE DATOS  
class Config(object):
    SECRET_KEY = 'Clave nueva'
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@127.0.0.1/proyectoFinal'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config.from_object(Config)
#MI MODELO DEL LOGIN
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    passwor = db.Column(db.String(64), nullable=False) 
    token = db.Column(db.String(5), nullable=True) 
    rol = db.Column(db.String(50), nullable=False)
    
#PASSWORD DE GOOGLE PARA PODER HACER LA VERIFICACIONES Y RECUPERAR
passwordCorreo = os.getenv("password")
email_sender = "cristianleyvacr7@gmail.com"

# TOKEN PARA VERIFICACION
def generar_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#TOKEN ARA REUPERAR CONTRASEÑA
def generar_token2():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
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
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        passwor = request.form['passwor']
        usuario = Login.query.filter_by(correo=email).first()
        if usuario:
            token = generar_token()
            usuario.token = token
            db.session.commit()            
            enviar_correo(email, token)            
            return redirect(url_for('verificar_token'))
        else:
            flash("Correo electrónico o contraseña incorrectos", "error")
            return render_template('login.html')
        
    return render_template('login.html')

#FUNCION DE VISTA DE VERIFICACION DE TOKEN
@app.route('/verificar-token', methods=['GET', 'POST'])
def verificar_token():
    if request.method == 'POST':
        email = request.form['email']
        token = request.form['token']
        usuario = Login.query.filter_by(correo=email, token=token).first()
        if usuario:
            return redirect(url_for('home'))
        else:
            flash("Correo electrónico o token incorrectos", "error")
            return render_template('verificar_token.html')
    return render_template('verificar_token.html')

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
@app.route('/olvidar-contrasena', methods=['GET', 'POST'])
def olvidar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Login.query.filter_by(correo=email).first()
        if usuario:
            token = generar_token2() 
            usuario.token = token
            db.session.commit()
            enviar_correo_restauracion(email, token) 
            flash("Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.", "success")
            return redirect(url_for('login'))
        else:
            flash("No se encontró ninguna cuenta asociada a ese correo electrónico.", "error")
    return render_template('olvidar_contrasena.html')

# FUNCION PARA CONFIRMAR TU CONTRASEÑA
@app.route('/restablecer-contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    usuario = Login.query.filter_by(token=token).first()
    if usuario:
        if request.method == 'POST':
            nueva_contrasena = request.form['nueva_contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            if nueva_contrasena == confirmar_contrasena:
                hashed_password = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
                usuario.passwor = hashed_password
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

@app.route('/home')
def home():
    return "¡Bienvenido a la página de inicio!"

if __name__ == '__main__':
    app.run(debug=True)
