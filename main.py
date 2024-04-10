from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from templates.ventasModule.ventacontroller import venta, guardar_venta 
from templates.produccionModule.produccionController import produccion
from templates.loginModule.loginController import login, verificar_token, olvidar_contrasena, restablecer_contrasena, dashbord, vistaLogin, logout
from templates.recetasModule.recetasController import recetas, guardar_recetas
from templates.dashbordModule.dashbordController import dashbord
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, Usuarios
from flask_bcrypt import generate_password_hash
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
csrf = CSRFProtect()
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

app.route('/venta')(venta)  
app.route('/guardar_venta', methods=['POST'])(guardar_venta)

app.route('/produccion')(produccion)

app.route('/recetas')(recetas)
app.route('/guardar_recetas', methods=['POST'])(guardar_recetas)

# app.route('/agregar_ingrediente/<int:receta_id>', methods=['POST'])(agregar_ingrediente)
app.route('/')(vistaLogin)
app.route('/login', methods=['GET', 'POST'])(login)
app.route('/verificar_token', methods=['GET', 'POST'])(verificar_token)
app.route('/olvidar_contrasena', methods=['GET', 'POST'])(olvidar_contrasena)
app.route('/restablecer_contrasena/<token>', methods=['GET', 'POST'])(restablecer_contrasena)
app.route('/dashbord')(dashbord)

app.route('/logout')(logout)

if __name__ == '__main__':
    from models import db
    db.init_app(app)
    with app.app_context():
         db.create_all()
    
    app.run(debug=True)
