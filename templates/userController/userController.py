from flask import render_template, request, redirect, url_for, current_app, jsonify
from models import db
from sqlalchemy import text, update 
import forms
from models import Usuario
from datetime import datetime

def user():
        usuarios_activos = Usuario.query.filter_by(estatusUsuario='Activo').all()
    
        return render_template()


def registrar_usuario():
   
    datos_usuario = request.json
    
  
    nuevo_usuario = Usuario(
        correo=datos_usuario.get('correo'),
        contrasenia=datos_usuario.get('contrasenia'),
        rol=datos_usuario.get('rol'),
        nombreCompleto=datos_usuario.get('nombreCompleto'),
        estatusUsuario='Activo'
    )

    db.session.add(nuevo_usuario)
    db.session.commit()
    
    respuesta = {'mensaje': 'Usuario registrado correctamente'}
    return jsonify(respuesta), 200


def bajaUser():
        return