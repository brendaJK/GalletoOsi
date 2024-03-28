
from wtforms import Form,StringField, EmailField, SelectField, IntegerField, validators

#formulario para venta xd   
class VentasForm(Form):
    nombreCliente = StringField('Nombre del Cliente', [validators.DataRequired(message="El campo es requerido"), validators.Length(min=4, max=50, message="Ingrese un nombre válido")])
    tipoVenta = SelectField('Tipo de Venta', choices=[('unidad', 'Unidad'), ('caja', 'Caja'), ('gramo', 'Gramo')], validators=[validators.DataRequired(message="Seleccione un tipo de venta")])
    cantidad = IntegerField('Cantidad', [validators.DataRequired(message="El campo es requerido"), validators.NumberRange(min=1, message="La cantidad debe ser mayor que cero")])
    tipoGalleta = SelectField('Tipo de Galleta', choices=[('chocolate', 'Chocolate'), ('vainilla', 'Vainilla'), ('fresa', 'Fresa')], validators=[validators.DataRequired(message="Seleccione un tipo de galleta")])

