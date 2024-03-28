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
