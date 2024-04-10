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
    fechaProduccion = db.Column(db.Date)
    costoProduccion = db.Column(db.Double)
    fechaCaducidad = db.Column(db.Date)
    idUsuario = db.Column(db.Integer)
    Estatus = db.Column(db.String(64))
    nombreGalleta = db.Column(db.String(64))
    cantidadProducida = db.Column(db.Integer)

# Modelo de datos de producto
class Producto(db.Model):
    __tablename__ = 'producto'
    idProducto = db.Column(db.Integer, primary_key = True)
    idReceta = db.Column(db.Integer)
    
# Modelo de datos de MermaProuccion
class MermaProduccion(db.Model):
    __tablename__ = 'merma_produccion'
    idMerma = db.Column(db.Integer, primary_key = True)
    idInventario = db.Column(db.Integer)
    idProduccion = db.Column(db.Integer)
    idUsuario = db.Column(db.Integer)
    cantidadMerma = db.Column(db.Double)
    Descripcion = db.Column(db.String(150))
    EstatusStock = db.Column(db.String(25))


 # Modelo de datos de receta
class Recetas(db.Model):
    __tablename__ = 'recetas'
    idReceta = db.Column(db.Integer, primary_key = True, autoincrement = True)
    idRecetaDetalle = db.Column(db.Integer)
    nombreGalleta = db.Column(db.String(64))
    descripcion = db.Column(db.String(100))
    cantidadGalletas = db.Column(db.Integer)
    pesoGalleta = db.Column(db.Double)

# Modelo de datos de RecetaDetalle
class RecetaDetalle(db.Model):
    __tablename__ = 'recetasDetalle'
    idRecetaDetalle = db.Column(db.Integer, primary_key = True, autoincrement = True)
    idReceta = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    ingrediente = db.Column(db.String(70))
    material = db.Column(db.String(64))
    idIngrediente = db.Column(db.Integer)


# Modelo de datos de proveedor
class Proveedor(db.Model): 
    __tablename__='proveedor' 
    idProveedor=db.Column(db.Integer,primary_key=True) 
    razonSocial=db.Column(db.String(300)) 
    nombreP=db.Column(db.String(100))
    estatus=db.Column(db.String(8))
    fechaAgregado=db.Column(db.DateTime, default= datetime.now())

# Modelo de datos de Materias Primas 
class MateriaPrimas(db.Model): 
    __tablename__='materiaPrima' 
    idMP=db.Column(db.Integer,primary_key=True)
    nombreMa=db.Column(db.String(100))
    tipoPro=db.Column(db.String(10))
    estatus=db.Column(db.String(10))


 # Modelo de datos de Compra de Materias primas   
class CompraMateriaPrima(db.Model): 
    __tablename__='compraMateriaPrima'
    idCMP=db.Column(db.Integer,primary_key=True)
    idMP=db.Column(db.Integer)
    idProveedor=db.Column(db.Integer)
    costo=db.Column(db.Float)
    cantidad=db.Column(db.String(100))
    estatus=db.Column(db.String(10))
    idUsuario=db.Column(db.Integer)
    fechaCompra=db.Column(db.DateTime,default=datetime.now)

# Modelo de datos de Merma de Materias Primas
class MermaMateriaPrima(db.Model): 
    __tablename__='mermaMateriaPrima' 
    idMermaMa=db.Column(db.Integer,primary_key=True)
    idMP=db.Column(db.Integer)
    idMPI=db.Column(db.Integer)
    costo=db.Column(db.Float)
    descripcion=db.Column(db.String(100))
    estatus=db.Column(db.String(10))
    idUsuario=db.Column(db.Integer)
    fecha=db.Column(db.DateTime)

#Modelo de datos de Inventario de Materias Primas
class InventarioMateriaPrima(db.Model): 
    __tablename__='inventarioMateriaPrima'
    idMPI=db.Column(db.Integer,primary_key=True)
    idCMP=db.Column(db.Integer)
    cantidad=db.Column(db.String(100))
    estatus=db.Column(db.String(10))
    fechaCaducidad=db.Column(db.DateTime)    
    
    
class Usuarios(db.Model):
    __tablename__='usuarios'
    idUsuario = db.Column(db.Integer,primary_key=True)
    correo = db.Column(db.String(100))
    contrasenia = db.Column(db.String(64))
    token = db.Column(db.String(15))
    rol = db.Column(db.String(45))
    nombre = db.Column(db.String(50))
    estatus = db.Column(db.String(20))

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    passwor = db.Column(db.String(64), nullable=False) 
    token = db.Column(db.String(5), nullable=True) 
    rol = db.Column(db.String(50), nullable=False)
