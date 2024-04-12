from flask import Flask, session
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from templates.ventasModule.ventacontroller import venta, confirmar_venta, actualizar_caja, proveedorpago, pagoMateriaPrima, agregarDinero
from templates.produccionModule.produccionController import produccion
from templates.loginModule.loginController import login, verificar_token, olvidar_contrasena, restablecer_contrasena, dashbord
from templates.recetasModule.recetasController import recetas, eliminar_ingrediente, recetas_detalle, agregar_ingrediente
from templates.loginModule.loginController import login, verificar_token, olvidar_contrasena, restablecer_contrasena, dashbord, vistaLogin, logout
from templates.dashbordModule.dashbordController import dashbord, descargar_logs
from templates.dashbordModule.dashbordController import dashbord, ventaDia
#from templates.usuariosModule.usuarioNuevoController import usuarioNuevo, eliminar_usuario, activar_usuario

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, Login
from flask_bcrypt import generate_password_hash

from templates.materiaPrimaModule.materiasPrimasController import maPrimas,eliminar_materia,comprarMateriasPrimas,inventarioMateriasPrimas,eliminar_inventario
from templates.proveedorModule.proveedorController import proveedores,eliminar_proveedor
from templates.reporteVentaModule.reporteVentaController import reporte_venta, filtrar_y_imprimir
from templates.produccionModule.produccionController import productos
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import db, Usuarios, LogsInicio
from flask_bcrypt import generate_password_hash
from flask_cors import CORS
from flask_login import LoginManager, logout_user, current_user

csrf=CSRFProtect()
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

login_manager = LoginManager()
login_manager.init_app(app)


current_user_id = None

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('vistaLogin'))

@app.before_request
def check_session_expiry():
    if current_user.is_authenticated: 
        last_activity = session.get('last_activity')
        if last_activity is not None:
            last_activity = last_activity.replace(tzinfo=None) 
            delta = datetime.now() - last_activity
            if delta > timedelta(minutes=1): 
                idUsuario = current_user.id
                nueva_salida = LogsInicio(idUsuario=idUsuario, fecha=datetime.now().date(), hora=datetime.now().time(), estatus='Salio')
                db.session.add(nueva_salida)
                db.session.commit()
                session.clear()
                logout_user()
                return redirect(url_for('vistaLogin'))
        session['last_activity'] = datetime.now()


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
app.route('/eliminar_inventario/<int:inventario_id>', methods=['POST'])(eliminar_inventario)
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

app.route('/descargar_logs', methods=['GET'])(descargar_logs)

app.route('/logout')(logout)




app.route('/dashbord')(dashbord)



app.route('/ventaDia')(ventaDia)



#app.route('/usuarioNuevo')(usuarioNuevo)
#app.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])(eliminar_usuario)

#app.route('/activar_usuario/<int:usuario_id>', methods=['POST'])(activar_usuario)

app.route('/productos')(productos)




if __name__ == '__main__':
    from models import db
    db.init_app(app)
    with app.app_context():
         db.create_all()
    
    app.run(debug=True)
