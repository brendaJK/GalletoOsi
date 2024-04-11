from flask import render_template, request, redirect, url_for
from models import db, Recetas, RecetasDetalle
from flask_login import login_required
import base64
import json
detalles_receta_temporal = []

@login_required
def recetas():
    recetas = Recetas.query.all()
    data_recetas = []
    for receta in recetas:
        detalles = RecetasDetalle.query.filter_by(iReceta=receta.id).all()
        ingredientes = []
        materiales = []
        for detalle in detalles:
            if detalle.ingrediente:
                ingredientes.append(detalle)
            if detalle.material:
                materiales.append(detalle.material)
        data_recetas.append({
            'id': receta.id,
            'nombre': receta.nombre,
            'descripcion': receta.descripcion,
            'ingredientes': ingredientes,
            'materiales': materiales
        })
    return render_template('recetasModule/recetas.html', recetas=data_recetas)

@login_required
def guardar_recetas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidadGalletas = request.form['cantidadGalletas']
        pesoGalletas = request.form['pesoGalletas']
        imagen = request.files['imagen']
        imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
        
        nueva_receta = {
            'nombre': nombre,
            'descripcion': descripcion,
            'cantidadGalletas': cantidadGalletas,
            'pesoGalletas': pesoGalletas,
            'imagen': imagen_base64,
            'detalles': []
        }
        
        detalles_json = request.form['detalles']
        detalles = json.loads(detalles_json)
        
        for detalle in detalles:
            cantidad = detalle['cantidad']
            ingrediente = detalle['ingrediente']
            material = detalle['material']
            nueva_receta['detalles'].append({'cantidad': cantidad, 'ingrediente': ingrediente, 'material': material})
        
        detalles_receta_temporal.append(nueva_receta)
        
    return render_template('loginModule/recetas.html', detalles_receta_temporal=detalles_receta_temporal)

    