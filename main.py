<<<<<<< HEAD
from flask import Flask,render_template, request,jsonify, Response, url_for,make_response,session

from flask import flash,redirect
=======
from flask import Flask,render_template, request,jsonify, Response, url_for,make_response
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import flash,redirect, session
>>>>>>> e740196a6f1999f45f60105484b5f15c22196838
from flask_wtf.csrf import CSRFProtect
import io
from fpdf import FPDF
from pymongo import MongoClient
from bson import ObjectId
import forms
from flask import Blueprint, render_template, request
from forms import LoginForm
from flask import jsonify
import hashlib
from pymongo import MongoClient
from email.message import EmailMessage
import ssl
import secrets


import smtplib

#lo ideal es que la url este en una variable de entorno
#pero para efectos de la prueba se deja asi
clientMongo = MongoClient("mongodb+srv://kookie01jeon:jungkook2722@galleto.js0ke36.mongodb.net/")
db = clientMongo.get_database('usuario')

from flask import jsonify, redirect
import secrets

csrf=CSRFProtect()
app=Flask(__name__)
app.secret_key = 'mysecretkey'


#por que queremos trabajar con ese

# from wtforms import DecimalField
# Definir el campo total

# En tu vista de Flask
mensaje = " "

@app.route("/osi", methods=["GET", "POST"])
def osi():
    return render_template('principal.html')

@app.route("/veriff", methods=["GET", "POST"])
def veriff():
    
    
    global mensaje 
    form = forms.VerificacionForm(request.form)
    
    if request.method == 'POST':
        codigo = form.codigo.data
        print('2')
        print('antes de entrar')
        print(mensaje)
        print(codigo)
        if codigo == mensaje :
                print('3')
                email = session.get('email')
                session_token = secrets.token_hex(16)
                print(session_token)            
                print(email)
                db.usuarios.update_one({'email': email}, {'$set': {'sesion': session_token}})
                
                datos_usuario = db.usuarios.find_one({'email': email}, {'_id': 1, 'username': 1, 'email': 1, 'sesion': 1})  
                session['datos_usuario'] = datos_usuario
                print('funciono')
            
                return redirect('/osi')
        else:
            flash("El codigo no es correcto", "error")
            print('no funciono')
    
    print('orale')
    return render_template('verificacion.html', form=form)


    
@app.route("/venta", methods=["GET", "POST"])
def venta():
    form = forms.UserFormVenta(request.form)
    
    # Obtener los nombres de los productos desde la base de datos
    productos = db.producto.find({}, {'nombreProducto': 1})  # Reemplaza 'nombreProducto' con el nombre correcto del campo
    opciones_galleta = [(producto['nombreProducto'], producto['nombreProducto']) for producto in productos]
    
    # Pasar las opciones al formulario para que pueda renderizarlas en el select
    form.galleta.choices = opciones_galleta
    
    if request.method == 'POST' and form.validate():
        tipo = request.form['tipo']
        galleta = request.form['galleta']
        cantidad = int(request.form['cantidad'])

    # Verificar si hay suficiente stock
        inventario = db.inventario.find_one({'nombre': galleta})
        if inventario:
            stock_disponible = int(inventario['stock'])
            equivalencia = int(inventario['equivalencia']) if 'equivalencia' in inventario else 1
        
            cantidad_ajustada = calcular_cantidad_ajustada(tipo, cantidad, equivalencia)
        
            if cantidad_ajustada > stock_disponible:
                flash('No hay suficiente stock para completar la venta.', 'error')
                return redirect(url_for('venta'))
            else:
            # Restar la cantidad vendida del stock en el inventario
                nuevo_stock = stock_disponible - cantidad_ajustada
                db.inventario.update_one({'nombre': galleta}, {'$set': {'stock': nuevo_stock}})
                
        else:
            flash('El producto seleccionado no está disponible en el inventario.', 'error')
            return redirect(url_for('venta'))
            
        # Calcular el costo de la venta
        costo_venta = calcular_costo_venta(tipo, cantidad)
        
        venta = {
            'tipo_venta': tipo,
            'galleta': galleta,
            'cantidad': cantidad,
            'costo_venta': costo_venta
        }
        
        try:
            db.venta.insert_one(venta)
        except Exception as e:
            print(e)

        # Restar la cantidad de productos vendidos del inventario
        try:
            if tipo == 'Unidad':
                cantidad_unidades = cantidad 
                db.producto.update_one({'nombre': galleta}, {'$inc': {'cantidadExistencias': -cantidad}})
            elif tipo == 'Gramos':
                cantidad_unidades = cantidad // 100
                db.producto.update_one({'nombre': galleta}, {'$inc': {'cantidadExistencias': -cantidad_unidades}})
            elif tipo == 'Dinero':
                cantidad_unidades = cantidad // 10
                db.producto.update_one({'nombre': galleta}, {'$inc': {'cantidadExistencias': -cantidad_unidades}})
            elif tipo == 'Caja':
                cantidad_unidades = cantidad * 10
                db.producto.update_one({'nombre': galleta}, {'$inc': {'cantidadExistencias': -cantidad_unidades}})
        except Exception as e:
            print(e)
        
        
        
        flash('Venta realizada con éxito.', 'success')
        return redirect(url_for('venta'))
        
    return render_template('venta.html', form=form)

def calcular_costo_venta(tipo, cantidad):
    if tipo == 'Unidad':
        costo_venta = cantidad * 10  # Cada unidad vale 10
    elif tipo == 'Gramos':
        costo_venta = cantidad * 0.1  # Cada gramo vale 0.1
    elif tipo == 'Dinero':
        costo_venta = cantidad  # El costo ya está en dinero
    elif tipo == 'Caja':
        costo_venta = cantidad * 100  # Cada caja vale 100
    return costo_venta

def calcular_cantidad_ajustada(tipo, cantidad, equivalencia):
    if tipo == 'Unidad':
        return cantidad
    elif tipo == 'Gramos':
        return cantidad // 100
    elif tipo == 'Dinero':
        return cantidad // 10
    elif tipo == 'Caja':
        return cantidad * 10

@app.route("/inventario",methods=["GET","POST"])
def inventario():
    inventario = db.inventario.find()
    
    
    return render_template('inventario.html', inventario=inventario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('index.html', form=form)
    elif request.method == 'POST':
        # Obtener el hash de la contraseña del formulario
        passw = hashlib.sha256(form
        .password.data.encode()).hexdigest()

        # Buscar el usuario en la base de datos
        usuario = db.usuarios.find_one({'username': form.username.data, 'password': passw})
        if usuario:
            
            
            emailPrueba = db.usuarios.find_one({'username': form.username.data},{"email": 1, "_id": 0})
            print(emailPrueba)
            email = usuario.get('email')
            codigoVeri(email)# Obtener el correo electrónico del usuario
            print(email)
            session['email'] = email
            
            return  redirect('/veriff')
        else:
            return render_template('index.html', form=form, message='Credenciales incorrectas')
    else:
        return render_template('index.html', form=form, message='Datos incorrectos')
    
def codigoVeri(email):
    global mensaje
    codigo_verificacion = secrets.token_hex(4)  # Código aleatorio de 8 caracteres
    mensaje = codigo_verificacion
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('kookie01jeon@gmail.com', 'zuvl ffvb ntjt hqke ')
    server.sendmail('jonarrodi99@gmail.com' , email ,mensaje)
    server.quit()
    print('Correo enviado osi')    

"""
Esta ruta se encarga de cerrar la sesión de un usuario
debes de recibir un json con el siguiente formato:
{
    "username": "nombre_de_usuario"
}

"""
@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    print(data)
    usuario = db.usuarios.update_one({'username': data['username']}, {'$set': {'sesion': ''}})
    return redirect('/login')



"""
Esta ruta se encarga de crear un usuario
debes de recibir un json con el siguiente formato:
{
    "username": "nombre_de_usuario",
    "password": "contraseña"
}
de preferencia insertalos con postman

"""
@app.route('/login/crear', methods=['POST'])
def crear_usuario():
    data = request.json
    #sacar la password del json y hashearla
    data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
    print(data)
    #insertar el usuario en la base de datos
    db.usuarios.insert_one(data)
    return jsonify({'message': 'Usuario creado correctamente'}), 200

"""
Esta ruta se encarga de obtener todos los usuarios
solo es para pruebas
"""
@app.route('/login/obtener', methods=['GET'])
def obtener_usuarios():
    usuarios = db.usuarios.find()
    usuarios = list(usuarios)
    for usuario in usuarios:
        usuario['_id'] = str(usuario['_id'])
    return jsonify(usuarios), 200


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    if request.method == 'GET':
        id = request.args.get('id')
        # Encontrar el documento con el ID correspondiente en la colección 'inventario'
        inve = db.inventario.find_one({'_id': ObjectId(id)})
        # Pasar los datos encontrados al formulario
        create_form = forms.InvenForm(request.form, data=inve)
        create_form.id.data = id 
    else:
        create_form = forms.InvenForm(request.form)
        
    if request.method == 'POST':
        try:
            id = request.form['id']
            # Eliminar el documento con el ID correspondiente de la colección 'inventario'
            db.inventario.delete_one({'_id': ObjectId(id)})
            return redirect('/inventario')
        except Exception as e:
            print(e)  # Manejar las excepciones adecuadamente
            
            
        
    return render_template('eliminar.html', form=create_form)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    if request.method == 'GET':
        id = request.args.get('id')
        # Encontrar el documento con el ID correspondiente en la colección 'inventario'
        inve = db.inventario.find_one({'_id': ObjectId(id)})
        # Crear el formulario de modificación con los datos del documento
        create_form = forms.InvenForm(request.form, data=inve)
        create_form.id.data = id  # Establecer el ID como valor predeterminado en el campo 'id' del formulario
    elif request.method == 'POST':
        try:
            id = request.form['id']
            
            
            precioV = request.form['precioV']
            stock = request.form['stock']
            # Actualizar el documento con los datos modificados
            db.inventario.update_one({'_id': ObjectId(id)}, {'$set': {'precioV': precioV, 'stock': stock}})
            return redirect('/inventario')
        except Exception as e:
            print(e)  # Manejar las excepciones adecuadamente
        
    return render_template('modificar.html', form=create_form)



@app.route("/reporte",methods=["GET","POST"])
def reporte():
    venta = db.venta.find()
    return render_template('reporte.html', venta=venta)


@app.route('/generar_pdf')
def generar_pdf():
    # Obtener los datos para la tabla (venta)
    venta = obtener_datos_para_tabla()  # Asegúrate de tener esta función implementada

    # Crear un objeto PDF
    pdf = FPDF()
    pdf.add_page()

    # Configurar la fuente y el tamaño del texto
    pdf.set_font("Arial", size=12)

    # Agregar encabezado
    pdf.cell(200, 10, txt="Reporte de Ventas", ln=True)

    # Agregar los datos de la tabla al PDF
    for ven in venta:
        pdf.cell(50, 10, f"Forma de venta: {ven['tipo_venta']}", ln=True)
        pdf.cell(50, 10, f"Galleta: {ven['galleta']}", ln=True)
        pdf.cell(50, 10, f"Cantidad: {ven['cantidad']}", ln=True)
        pdf.cell(50, 10, f"Total venta: {ven['costo_venta']}", ln=True)
        pdf.cell(200, 10, ln=True)  # Agregar espacio entre filas

    # Guardar el PDF en un buffer de memoria
    buffer = io.BytesIO()
    pdf.output(buffer)

    # Crear una respuesta PDF
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte.pdf'
    return response

# De aqui para abajo va lo de recuperar la contraseña jaja salu2

@app.route('/ResetPass', methods = ['POST', 'GET'])
def rPass():
    create_form = forms.ResetPassForm(request.form)
    if request.method == 'GET':
        return render_template('ResetPass.html', form = create_form)
    if request.method == 'POST':

        
        email = db.usuarios.find_one({'email': create_form.email.data})
        if email:

            token = secrets.token_urlsafe(16)
            print(token)
            session['reset_token'] = token
            user = email.get('username')

            de = 'GalletoInc@gmail.com'
            para = email.get('email')
            asunto = 'Recuperacion de Contraseña'

            mensaje = MIMEMultipart()
            mensaje['From'] = de
            mensaje['To'] = para
            mensaje['Subject'] = asunto
            cuerpo = f'''\
                       Hola,

                       Has solicitado recuperar tu contraseña. 
                       Por favor, sigue este enlace para restablecerla:

                       http://localhost:5000/restablecer-contraseña?token={token}

                       Si no solicitaste esto, ignora este mensaje.

                       Saludos,
                        
                        Don galleto'''
            texto = MIMEText(cuerpo, 'plain')
            mensaje.attach(texto)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            server.login(de, 'dxgu xxvg lpbh pcxa')
            server.send_message(mensaje)
            server.quit()

            msgconfirm = 'Se ha enviado el correo para la recuperacion de su contraseña.'


        else: 
            msgconfirm = 'No hay ninguna cuenta asosiada a este email.'        

        return render_template('ResetPass.html', form = create_form, msg = msgconfirm)


@app.route('/restablecer-contraseña', methods=['GET', 'POST'])
def restablecer_contraseña():
    token = request.args.get('token')
    create_form = forms.ResetPassForm(request.form)
    if token == session.get('reset_token'):
        if request.method == 'POST':
            #nueva_contraseña = request.form['nueva_contraseña']
            # usuarios_db[usuario]['contraseña'] = nueva_contraseña
            return 'Tu contraseña ha sido actualizada con éxito.'
        return render_template('passwordRecup.html', form = create_form)
    else:
        return 'El token de restablecimiento de contraseña no es válido.'




#Aqui termina lo de recuperar la contraseña jaja despedi2


# Función para obtener los datos de ventas (deberías reemplazarla con tu propia lógica)
def obtener_datos_para_tabla():
    ventas = [
        {"tipo_venta": "Unidad", "galleta": "Chocolate", "cantidad": 10, "costo_venta": 50.0},
        {"tipo_venta": "Gramos", "galleta": "Vainilla", "cantidad": 200, "costo_venta": 20.0},
        # Agrega más datos de ventas según sea necesario
    ]
    return ventas





if __name__ == '__main__':
    app.run(debug=True)