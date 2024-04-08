from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from templates.ventasModule.ventacontroller import venta, confirmar_venta, actualizar_caja, proveedorpago, pagoMateriaPrima, agregarDinero
from templates.produccionModule.produccionController import produccion
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

app.route('/venta')(venta)
app.route('/confirmar-venta', methods=['POST'])(confirmar_venta)
app.route('/actualizar_caja', methods=['POST'])(actualizar_caja)
app.route('/pago-proveedor', methods=['POST'])(proveedorpago)
app.route('/pago-materiaPrima', methods=['POST'])(pagoMateriaPrima)
app.route('/agregar-dinero-caja', methods=['POST'])(agregarDinero)
app.route('/produccion')(produccion)


if __name__ == '__main__':
    from models import db
    db.init_app(app)
    with app.app_context():
         db.create_all()
    
    app.run(debug=True)
