from flask import render_template, request, redirect, url_for
from models import db, Recetas, RecetaDetalle

def recetas():
    recetas = Recetas.query.all()
    data_recetas = []
    for receta in recetas:
        detalles = RecetaDetalle.query.filter_by(iReceta=receta.id).all()
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

def recetas_detalle(receta_id):
    receta = Recetas.query.get_or_404(receta_id)
    detalles = RecetaDetalle.query.filter_by(iReceta=receta_id).all()
    return render_template('recetasModule/recetas_detalle.html', receta=receta, detalles=detalles, idReceta=receta_id)

def eliminar_ingrediente(detalle_id):
    detalle = RecetaDetalle.query.get(detalle_id)
    if detalle:
        db.session.delete(detalle)
        db.session.commit()

def agregar_ingrediente():
    if request.method == 'POST':
        try:    
            detalle = RecetaDetalle(
                iReceta = int(request.form['iReceta']),
                cantidad = request.form['gramos'], 
                ingrediente = request.form['ingrediente'],
                material = request.form['material']
            )
            db.session.add(detalle)
            db.session.commit()
            return redirect(url_for('recetas_detalle', receta_id=request.form['iReceta']))
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            db.session.rollback()
    return redirect(url_for('recetas_detalle', receta_id=request.form['iReceta']))

    