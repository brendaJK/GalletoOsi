from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField,TelField,IntegerField,SubmitField,PasswordField,TextAreaField,EmailField
from wtforms import EmailField
from wtforms import validators


class UserForm(Form):
    nombre= StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='Ingresa nombre valido')
    ])
    apaterno= StringField('apaterno',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='Ingresa apellido valido')
    ])
    amaterno= StringField('amaterno',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='Ingresa apellido valido')
    ])
    email= EmailField('email',[
        validators.Email(message='Ingresa un correo valido')
    ])
    edad= IntegerField('edad',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='Ingresa una edad valida')
    ])
    
class UserForm2(Form):
    
    id=StringField('id')
    nombre= StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='Ingresa nombre valido')
    ])
    apaterno= StringField('apaterno',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='Ingresa apellido valido')
    ])
    email= EmailField('email',[
        validators.Email(message='Ingresa un correo valido')
    ])
    
class UserFormVenta(Form):
    
    tipo= StringField('Tipo compra',[
        validators.DataRequired(message='El campo es requerido')
    ])
    galleta= StringField('Galleta',[
        validators.DataRequired(message='El campo es requerido')
    ])
    cantidad= IntegerField('Cantidad',[
        validators.DataRequired(message='El campo es requerido')
    ])
    
    

class LoginForm(FlaskForm):
    username= StringField('Usuario',[
        validators.DataRequired(message='El campo es requerido')
    ])
    password= PasswordField('Contraseña',[
        validators.DataRequired(message='El campo es requerido')
    ])
    email= EmailField('Email',[
        validators.Email(message='Ingresa un correo valido')
    ])
    
class VerificacionForm(Form):
    codigo= StringField('Codigo',[
        validators.DataRequired(message='El campo es requerido')
    ])
    

class UsuNuevoForm(FlaskForm):
    username= StringField('Usuario',[
        validators.DataRequired(message='El campo es requerido')
    ])
    password = PasswordField('Contraseña', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=8, message='Ingresa una contraseña válida'),
        validators.Regexp(
            regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+])[A-Za-z0-9!@#$%^&*()_+]+$',
            message='La contraseña debe contener al menos una mayúscula, al menos un carácter especial, letras minúsculas y números'
        )
    ])
    email= EmailField('Email',[
        validators.Email(message='Ingresa un correo valido')
    ])
    
class InvenForm(Form):
    id=StringField('id')
    nombre= StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido')
    ])
    precioF= IntegerField('Precio fabricacion',[
        validators.DataRequired(message='El campo es requerido')
    ])
    precioV= IntegerField('Precio Venta',[
        validators.DataRequired(message='El campo es requerido')
    ])
    stock= IntegerField('Stock',[
        validators.DataRequired(message='El campo es requerido')
    ])
    
    