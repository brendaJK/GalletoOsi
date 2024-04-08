
from wtforms import Form,StringField, EmailField, SelectField, IntegerField, validators,DateField,FloatField,TextAreaField

#formulario para venta xd   
class VentasForm(Form):
    nombreCliente = StringField('Nombre del Cliente', [validators.DataRequired(message="El campo es requerido"), validators.Length(min=4, max=50, message="Ingrese un nombre válido")])
    tipoVenta = SelectField('Tipo de Venta', choices=[('unidad', 'Unidad'), ('caja', 'Caja'), ('gramo', 'Gramo')], validators=[validators.DataRequired(message="Seleccione un tipo de venta")])
    cantidad = IntegerField('Cantidad', [validators.DataRequired(message="El campo es requerido"), validators.NumberRange(min=1, message="La cantidad debe ser mayor que cero")])
    tipoGalleta = SelectField('Tipo de Galleta', choices=[('chocolate', 'Chocolate'), ('vainilla', 'Vainilla'), ('fresa', 'Fresa')], validators=[validators.DataRequired(message="Seleccione un tipo de galleta")])

class produccionForm(Form):
        costoProduccion = StringField('nombre del producto', [validators.DataRequired(message="El campo es requerido"), validators.Length(min=4, max=64, message="Ingrese un nombre válido")])
        fechaProduccion = StringField('nombre del producto', [validators.DataRequired(message="El campo es requerido"), validators.Length(min=4, max=64, message="Ingrese un nombre válido")])
        descripcion = StringField('nombre del producto', [validators.DataRequired(message="El campo es requerido"), validators.Length(min=4, max=64, message="Ingrese un nombre válido")])
        fechaCaducidad = StringField('nombre del producto', [validators.DataRequired(message="El campo es requerido"), validators.Length(min=4, max=64, message="Ingrese un nombre válido")])
    
class ProveForm(Form):
    id=IntegerField('id')
    
    razonSocial= StringField('Razon social',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=300, message='Ingrese una razon social valida')
    ])
    nombreP= StringField('Nombre proveedor',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=100, message='Ingrese un nombre valido')
    ])
    
class MateForm(Form):
    id=IntegerField('id')
    tipoPro= StringField('Tipo proveedor',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=100)
    ])
    nombreMa= StringField('Nombre materia',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=100)
    ])
    

class CompraMateForm(Form):
    idCMP=IntegerField('idCMP') 
    materia=IntegerField('Materia prima') 
    proveedor= SelectField('Proveedor') 
    costo= FloatField('Costo',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=2,max=100)
    ])
    cantidad= IntegerField('Cantidad',[
        validators.DataRequired(message='El campo es requerido')
    ])
    presentacion= StringField('presentacion',[
        validators.DataRequired(message='El campo es requerido')
    ])
    fechaCaducidad= DateField('fechaCaducidad',[
        validators.DataRequired(message='El campo es requerido')
    ])

class InvenMateForm(Form):
    id=IntegerField('id') 
    descripcion= TextAreaField('Descripcion',[
        validators.DataRequired(message='El campo es requerido')
    ])
    
class ReporteVentaForm(Form):
    id=IntegerField('id') 
    tipo= SelectField('tipo',[
        validators.DataRequired(message='El campo es requerido')
    ])