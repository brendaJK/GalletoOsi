from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship


db = SQLAlchemy()

# Modelo de datos Venta xd
class Venta(db.Model):
    __tablename__ = 'venta'
    idVenta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    total = db.Column(db.Float)
    cantidadVendida = db.Column(db.Integer)
    idCaja = db.Column(db.Integer, db.ForeignKey('caja.idCaja'))
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))

    
    detallesVenta = relationship('DetalleVenta', backref='venta')

# Modelo de datos DetalleVenta xd
class DetalleVenta(db.Model):
    __tablename__ = 'detalleVenta'
    idDetalleVenta = db.Column(db.Integer, primary_key=True)
    subtotal = db.Column(db.Float)
    tipoVenta = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    nombreGalleta = db.Column(db.String(50))
    idVenta = db.Column(db.Integer, db.ForeignKey('venta.idVenta'))

    
# Modelo de datos Caja xd
class Caja(db.Model):
    __tablename__ = 'caja'
    idCaja = db.Column(db.Integer, primary_key=True)
    dineroCaja = db.Column(db.Float)

# Modelo de datos Produccion
class Produccion(db.Model):
    __tablename__ = 'produccion'
    idProduccion = db.Column(db.Integer, primary_key = True)
    idReceta = db.Column(db.Integer)
    fechaProduccion = db.Column(db.Date)
    costoProduccion = db.Column(db.Double)
    fechaCaducidad = db.Column(db.Date)
    nombreProducto = db.Column(db.String(150))
    cantiadadProducida = db.Column(db.Integer)
    Estatus = db.Column(db.String(25))
    idUsuario = db.Column(db.Integer)

# Modelo de datos de producto
class Producto(db.Model):
    __tablename__ = 'producto'
    idProducto = db.Column(db.Integer, primary_key = True)
    idReceta = db.Column(db.Integer)
    
class MermaProduccion(db.Model):
    __tablename__ = 'merma_produccion'
    idMerma = db.Column(db.Integer, primary_key = True)
    idInventario = db.Column(db.Integer)
    idProduccion = db.Column(db.Integer)
    idUsuario = db.Column(db.Integer)
    cantidadMerma = db.Column(db.Double)
    Descripcion = db.Column(db.String(150))
    Estatus = db.Column(db.String(25))


class Proveedor(db.Model): #creamos el mapeado para poder crear la tabla
    __tablename__='proveedor' # nos permite agregar un  nombre especifico
    idProveedor=db.Column(db.Integer,primary_key=True) #necesario el id para fungir como clave primaria y permita generar el campo siempre lo requiere 
    razonSocial=db.Column(db.String(300)) # con db.Column asignando el tipo de dato
    nombreP=db.Column(db.String(100))
    estatus=db.Column(db.String(8))
    fechaAgregado=db.Column(db.DateTime,default=datetime.now)  # Aquí está el cambio
    
class MateriaPrimas(db.Model): #creamos el mapeado para poder crear la tabla
    __tablename__='materiaPrima' # nos permite agregar un  nombre especifico
    idMP=db.Column(db.Integer,primary_key=True)
    nombreMa=db.Column(db.String(100))
    tipoPro=db.Column(db.String(10))
    estatus=db.Column(db.String(10))
    
class CompraMateriaPrima(db.Model): #creamos el mapeado para poder crear la tabla
    __tablename__='compraMateriaPrima' # nos permite agregar un  nombre especifico
    idCMP=db.Column(db.Integer,primary_key=True)
    idMP=db.Column(db.Integer)
    idProveedor=db.Column(db.Integer)
    costo=db.Column(db.Float)
    cantidad=db.Column(db.String(100))
    estatus=db.Column(db.String(10))
    idUsuario=db.Column(db.Integer)
    fechaCompra=db.Column(db.DateTime,default=datetime.now)

class MermaMateriaPrima(db.Model): #creamos el mapeado para poder crear la tabla
    __tablename__='mermaMateriaPrima' # nos permite agregar un  nombre especifico
    idMermaMa=db.Column(db.Integer,primary_key=True)
    idMP=db.Column(db.Integer)
    idMPI=db.Column(db.Integer)
    costo=db.Column(db.Float)
    descripcion=db.Column(db.String(100))
    estatus=db.Column(db.String(10))
    idUsuario=db.Column(db.Integer)
    fecha=db.Column(db.DateTime)

class InventarioMateriaPrima(db.Model): #creamos el mapeado para poder crear la tabla
    __tablename__='inventarioMateriaPrima' # nos permite agregar un  nombre especifico
    idMPI=db.Column(db.Integer,primary_key=True)
    idCMP=db.Column(db.Integer)
    cantidad=db.Column(db.String(100))
    estatus=db.Column(db.String(10))
    fechaCaducidad=db.Column(db.DateTime)    

#Modelo de datos Usuario xd
class Usuario(db.Model):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key = True)
    correo = db.Column(db.String(255))
    contrasenia = db.Column(db.String(255))
    token = db.Column(db.String(255))
    rol = db.Column(db.String(25))
    nombreCompleto = db.Column(db.String(255))
    estatusUsuario = db.Column(db.String(25))
