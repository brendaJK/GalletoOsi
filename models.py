from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
db = SQLAlchemy()

# Modelo de datos para Venta xd
class Venta(db.Model):
    __tablename__ = 'venta'
    idVenta = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.String(50))
    subtotal = db.Column(db.Double)
    usuario = db.Column(db.String(50))
    tipoVenta = db.Column(db.String(50))
    nombreCliente = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)

    db.Column(db.Integer, db.ForeignKey('inventario.id'), nullable=False)
    producto = db.relationship('Inventario', backref='detalleVenta', lazy=True)
    
    
# Modelo de datos Caja xd
class Caja(db.Model):
    __tablename__ = 'caja'
    id = db.Column(db.Integer, primary_key = True)
    dinero = db.Column(db.Double)


# Modelo de datos Produccion
class Produccion(db.Model):
    __tablename__ = 'produccion'
    idProduccion = db.Column(db.Integer, primary_key = True)
    idProducto = db.Column(db.Integer)
    fechaProduccion = db.Column(db.Date)
    descripcion = db.Column(db.String(100))
    costoProduccion = db.Column(db.Double)
    fechaCaducidad = db.Column(db.Date)
    cantidadStock = db.Column(db.Integer)
    cantidadProducida = db.Column(db.Integer)
    estatusProduccion = db.Column(db.String(40))

# Modelo de datos de producto
class Producto(db.Model):
    __tablename__ = 'producto'
    idProducto = db.Column(db.Integer, primary_key = True)
    idReceta = db.Column(db.Integer)
    idMateriaPrima = db.Column(db.Integer)
    nombreProducto = db.Column(db.String(64))
    

# Modelo de datos de Materia Prima (al que le toco esta tabla no se que mas vaya a agregar)
# class Materia_Prima(db.Model):
#     __tablename__ = 'materia_prima'
#     idMateriaPrima = db.Column(db.Integer, primary_key = True)
#     idProveedor = db.Column(db.Integer)
#     nombreMateriaP = db.Column(db.String(64))
#     cantidad = db.Column(db.Double)