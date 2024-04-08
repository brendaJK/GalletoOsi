from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from templates.ventasModule.ventacontroller import venta, confirmar_venta, actualizar_caja, proveedorpago, pagoMateriaPrima, agregarDinero
from templates.produccionModule.produccionController import produccion
from templates.loginModule.loginController import login, verificar_token, olvidar_contrasena, restablecer_contrasena, dashbord
from templates.recetasModule.recetasController import recetas, eliminar_ingrediente, recetas_detalle, agregar_ingrediente
from templates.loginModule.loginController import vistaLogin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, Login
from flask_bcrypt import generate_password_hash

from templates.materiaPrimaModule.materiasPrimasController import maPrimas,eliminar_materia,comprarMateriasPrimas,inventarioMateriasPrimas
from templates.proveedorModule.proveedorController import proveedores,eliminar_proveedor
from templates.reporteVentaModule.reporteVentaController import reporte_venta, filtrar_y_imprimir
csrf=CSRFProtect()
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

app.route('/venta',methods=['GET','POST'])(venta)
app.route('/confirmar-venta', methods=['POST'])(confirmar_venta)
app.route('/actualizar_caja', methods=['POST'])(actualizar_caja)
app.route('/pago-proveedor', methods=['POST'])(proveedorpago)
app.route('/pago-materiaPrima', methods=['POST'])(pagoMateriaPrima)
app.route('/agregar-dinero-caja', methods=['POST'])(agregarDinero)
app.route('/produccion')(produccion)

app.route('/maPrimas',methods=['GET', 'POST'])(maPrimas)

app.route('/comprarMateriasPrimas', methods=['GET', 'POST'])(comprarMateriasPrimas)
app.route('/eliminar_materia/<int:materia_id>', methods=['POST'])(eliminar_materia)
app.route('/inventarioMateriasPrimas',methods=['GET', 'POST'])(inventarioMateriasPrimas)
app.route('/proveedores',methods=['GET', 'POST'])(proveedores)
app.route('/eliminar_proveedor/<int:proveedor_id>',methods=['POST'])(eliminar_proveedor)
app.route('/reporte_venta',methods=['GET', 'POST'])(reporte_venta)
app.route('/filtrar_y_imprimir',methods=['GET', 'POST'])(filtrar_y_imprimir)



app.route('/recetas')(recetas)
app.route('/eliminar_ingrediente/<int:detalle_id>', methods=['POST'])(eliminar_ingrediente)
app.route('/recetas/<int:receta_id>', methods=['GET', 'POST'])(recetas_detalle)
app.route('/agregar_ingrediente', methods=['POST'])(agregar_ingrediente)

# app.route('/agregar_ingrediente/<int:receta_id>', methods=['POST'])(agregar_ingrediente)
app.route('/')(vistaLogin)
app.route('/login', methods=['GET', 'POST'])(login)
app.route('/verificar_token', methods=['GET', 'POST'])(verificar_token)
app.route('/olvidar_contrasena', methods=['GET', 'POST'])(olvidar_contrasena)
app.route('/restablecer_contrasena/<token>', methods=['GET', 'POST'])(restablecer_contrasena)
app.route('/dashbord')(dashbord)


if __name__ == '__main__':
    from models import db
    db.init_app(app)
    with app.app_context():
         db.create_all()
    
    app.run(debug=True)
