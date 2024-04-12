from flask import Flask,render_template, request
import re
from flask import flash,redirect
from flask_login import login_required

from config import DevelopmentConfig
from flask import g
from datetime import datetime,timedelta
from models import db
from models import Proveedor,Usuario
from sqlalchemy import func
import forms
import secrets
from datetime import datetime
from sqlalchemy import text

caracteresEspeciales = re.compile(r'[^a-zA-Z0-9\s]')
@login_required
def sanitize_input(input_str):
    # Eliminar caracteres especiales usando la expresión regular
    return caracteresEspeciales.sub('', input_str)

@login_required
def usuarioNuevo():
    usuarioNuevo_form = forms.UsuarioNuevoForm(request.form)
    usuarios = Usuario.query.all()
    
    
    if request.method=='POST' and usuarioNuevo_form.validate():
        try:
                segundoApellido = ""
                nombre = sanitize_input(usuarioNuevo_form.nombre.data)
                primerApellido = sanitize_input(usuarioNuevo_form.primerApellido.data)
                segundoApellido = sanitize_input(usuarioNuevo_form.segundoApellido.data)
                correo = usuarioNuevo_form.correo.data
                contrasenia = usuarioNuevo_form.contrasenia.data
                rol = usuarioNuevo_form.nombre.data
                if segundoApellido == "":
                    nombreCompleto = f"{nombre} {primerApellido}"
                elif segundoApellido != "":
                    nombreCompleto = f"{nombre} {primerApellido} {segundoApellido}"

                usuario = Usuario(nombreCompleto=nombreCompleto, correo=correo, contrasenia = contrasenia, rol = rol, estatusUsuario='Activo')
                db.session.add(usuario)                    
                print('whos bad', usuario)
                db.session.commit()
                flash('El proveedor ha sido agregado exitosamente.', 'error')
        except Exception as e:
                print(f"Error en la base de datos: {e}")
                db.session.rollback()
    return render_template('usuariosModule/usuarioNuevo.html', form=usuarioNuevo_form, usuario=usuarios)


@login_required
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        try:
            print('idusuario',usuario_id)
            usuario.estatusUsuario = 'Inactivo'  # Cambiar el estado del proveedor
            db.session.commit()
            flash('El usuario ha sido desactivado, por lo que no podra acceder al sistema hasta que sea activado de nuevo.', 'success')
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
            flash('Error al eliminar el usuario.', 'error')
    else:
        flash('Usuario no encontrado.', 'error')

    return redirect('/usuarioNuevo')

@login_required
def activar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        try:
            print('idusuario',usuario_id)
            usuario.estatusUsuario = 'Activo'  # Cambiar el estado del proveedor
            db.session.commit()
            flash('El usuario ha sido activado, por lo que ya podra acceder al sistema .', 'success')
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
            flash('Error al activar el usuario.', 'error')
    else:
        flash('Usuario no encontrado.', 'error')

    return redirect('/usuarioNuevo')


