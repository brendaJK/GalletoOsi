from flask import render_template, request, redirect, url_for
from models import db
from datetime import datetime, timedelta
import forms
from models import Produccion, Usuarios, Recetas, RecetaDetalle, Producto, MermaProduccion
from sqlalchemy import text, or_, update
import re

def produccion():

    optRecetas = db.session.query(Recetas.nombreGalleta).all()
    

    

    registros = Produccion.query.filter(Produccion.Estatus == 'Pendiente').all()
    print(registros)
    
    return render_template('produccionModule/produccion.html', optRecetas = optRecetas, solicitudes = registros )




def rebajarInventarioMP(receta):

        sql = f'''
        SELECT rd.idReceta, mp.tipoPro, r.nombreGalleta, rd.ingrediente, rd.cantidad, CAST(imp.cantidad AS DOUBLE)  AS stock 
        , rd.idMPI FROM recetasdetalle rd
        INNER JOIN inventariomateriaprima imp ON rd.idMPI = imp.idMPI
        INNER JOIN recetas r ON r.idReceta = rd.idReceta 
        INNER JOIN compramateriaprima cmp ON cmp.idCMP = imp.idCMP
        INNER JOIN materiaprima mp ON mp.idMP = cmp.idMP
        WHERE r.nombreGalleta like '{receta}';
        '''
        
        consultaIn = db.session.execute(text(sql))
        ingredientes = consultaIn.fetchall()
        print(ingredientes)


        for ingrediente in ingredientes:
            print('IDReceta: ',ingrediente.idReceta, ' NombreGalleta: ', ingrediente.nombreGalleta, '\n'
            'Ingrediente: ', ingrediente.ingrediente, ' Cantidad en Stock:', ingrediente.stock, 'idIngrediente: ', ingrediente.idMPI,
            'Cantidad actualizada: ',  ingrediente.stock - ingrediente.cantidad, 'tipoProd: ', ingrediente.tipoPro)

            if ingrediente.tipoPro == 'Solido':
                cantidadActualizada = str(ingrediente.stock - ingrediente.cantidad)

                sql = f'''
                UPDATE inventariomateriaprima SET cantidad = "{cantidadActualizada} gramos" 
                WHERE estatus = 'Disponible' AND  idMPI = {ingrediente.idMPI};
               '''

                db.session.execute(text(sql))
                db.session.commit()

            elif ingrediente.tipoPro == 'Liquido':
                cantidadActualizada = str(ingrediente.stock - ingrediente.cantidad)

                sql = f'''
                UPDATE inventariomateriaprima SET cantidad = "{cantidadActualizada} mililitros" 
                WHERE estatus = 'Disponible' AND  idMPI = {ingrediente.idMPI};'''

                db.session.execute(text(sql))
                db.session.commit()


def calcularCostoProduccion():
        
    receta = request.form.get('Receta')
    
    sql = f''' 
          SELECT SUM((cmp.costo/ (CAST(cmp.cantidad AS DOUBLE) * 1000)) * rd.cantidad) as costoProduccion FROM inventariomateriaprima AS imp

          INNER JOIN compramateriaprima AS cmp ON cmp.idCMP = imp.idCMP
          INNER JOIN recetasDetalle as rd ON rd.idMPI = imp.idMPI
          INNER JOIN recetas AS r ON  r.idReceta =rd.idReceta 
          WHERE r.nombreGalleta LIKE '{receta}' group by r.nombreGalleta;
        '''


    consultaCostProd = db.session.execute(text(sql))
    costoProd = consultaCostProd.fetchone()
    print(costoProd[0])
    return render_template('produccionModule/produccion.html', optRecetas = optRecetas)






def guardarProduccion():

    optRecetas = db.session.query(Recetas.nombreGalleta).all()
    if request.method == 'POST':
        

         receta = request.form.get('Receta')

         sql = f''' 
             SELECT SUM((cmp.costo/ (CAST(cmp.cantidad AS DOUBLE) * 1000)) * rd.cantidad) as costoProduccion FROM inventariomateriaprima AS imp

             INNER JOIN compramateriaprima AS cmp ON cmp.idCMP = imp.idCMP
             INNER JOIN recetasDetalle as rd ON rd.idMPI = imp.idMPI
             INNER JOIN recetas AS r ON  r.idReceta =rd.idReceta 
             WHERE r.nombreGalleta LIKE '{receta}' group by r.nombreGalleta;
            '''


         consultaCostProd = db.session.execute(text(sql))
         costoProd = consultaCostProd.fetchone()

         

         id_producto = db.session.query(Producto.idProducto).filter(Producto.nombreProducto == receta).scalar()
         print(id_producto)
         print(costoProd[0])

         idUs = db.session.query(Usuarios.idUsuario).filter(Usuarios.nombre.like('%Mario%')).scalar()
         fechaSolicitud = datetime.now()
        #fechaCad = request.form.get('fechaCaducidad') 
         cantidadProducida = db.session.query(Recetas.cantidadGalletas).filter(Recetas.nombreGalleta == receta).scalar() 
         prod = Produccion(

            idProducto = id_producto,
           costoProduccion = costoProd[0],
            fechaSolicitud = fechaSolicitud,
            idUsuario = idUs,
            nombreGalleta = receta,
            Estatus = 'Pendiente',
            cantidadProducida = cantidadProducida
         )
         db.session.add(prod)
         db.session.commit()


         print('Operacion realizada.')
         return redirect(url_for('produccion'))

    return render_template('produccionModule/produccion.html', optRecetas = optRecetas)


def cancelarSolicitud():
    
    idProduccion = request.form['idProduccion']
    print(idProduccion)
    sql = f"UPDATE produccion SET Estatus = 'Cancelado' WHERE idProduccion = {idProduccion};"
    db.session.execute(text(sql))
    db.session.commit()
    
    return redirect(url_for('produccion'))


#-------------------------------------------------ProduccionesPendientes--------------------------------------


def produccionesPendientes():

    prodPend = Produccion.query.filter_by(Estatus = 'Pendiente').all()

    prodEProceso = Produccion.query.filter_by(Estatus = 'En Proceso').all()

    return render_template('produccionModule/ProdPendientes.html', pendientes = prodPend, procesos = prodEProceso)


def aceptarSolicitud():

    idProduccion = request.form['idProduccion']

    sql = f"UPDATE produccion SET Estatus = 'En Proceso' WHERE idProduccion = {idProduccion};"

    consultaCostProd = db.session.execute(text(sql))
    db.session.commit()

    return redirect(url_for('produccionesPendientes'))


def terminarSolicitud():

    idProduccion = request.form['idProduccion']
    sql = f"UPDATE produccion SET Estatus = 'Disponible' WHERE idProduccion = {idProduccion};"
    consultaCostProd = db.session.execute(text(sql))
    db.session.commit()

    return redirect(url_for('produccionesPendientes'))


#-------------------------------------MermaProduccion--------------------------------------

def registrarMermaProd():

    if request.method == 'GET':    
        idProduccion = request.args.get('idProduccion')
        infoProduccion = db.session.query(Produccion).filter(Produccion.idProduccion == idProduccion).first()
        nombreGalleta = infoProduccion.nombreGalleta
        idUsuario = infoProduccion.idUsuario
        cantidadProducida = infoProduccion.cantidadProducida
    if request.method == 'POST':

        idProduccion = request.form.get('produccion_id')
        print(idProduccion)
        infoProduccion = db.session.query(Produccion).filter(Produccion.idProduccion == idProduccion).first()
        nombreGalleta = request.form.get('nombreGalleta')
        idUsuario = request.form.get('usuario_id')
        cantidadProducida = request.form.get('cantidadProd')
        descripcion = request.form.get('descripcion')
        merma = MermaProduccion(

            idProduccion = idProduccion,
            idUsuario = idUsuario,
            cantidadMerma = cantidadProducida,
            Descripcion = descripcion,
            EstatusStock = 'Merma'

        )
        db.session.add(merma)
        stmt = update(Produccion).where(Produccion.idProduccion == idProduccion).values(Estatus='Merma')
        db.session.execute(stmt)
        db.session.commit()
        return redirect(url_for('produccionesPendientes'))
        
    return render_template('produccionModule/mermaProd.html', idProduccion = idProduccion, idUsuario = idUsuario , cantidadProducida = cantidadProducida,nombreGalleta = nombreGalleta)

