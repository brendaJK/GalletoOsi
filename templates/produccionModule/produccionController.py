from flask import render_template, request, redirect, url_for
from models import db
from datetime import datetime, timedelta
import forms
from models import Produccion, Usuarios, Recetas, RecetaDetalle
from sqlalchemy import text
import re

def produccion():

    optRecetas = db.session.query(Recetas.nombreGalleta).all()
    # print(optRecetas)

    # receta = request.form.get('Receta')

    # sql = f''' 
    #         SELECT SUM((cmp.costo/ CAST(imp.cantidad AS DOUBLE)) * rd.cantidad) as costoProduccion FROM inventariomateriaprima AS imp

    #         INNER JOIN compramateriaprima AS cmp ON cmp.idCMP = imp.idCMP
    #         INNER JOIN recetasDetalle as rd ON rd.idMPI = imp.idMPI
    #         INNER JOIN recetas AS r ON  r.idReceta =rd.idReceta 
    #         WHERE r.nombreGalleta LIKE '{receta}' group by r.nombreGalleta;
    #     '''


    # consultaCostProd = db.session.execute(text(sql))
    # costoProd = consultaCostProd.fetchone()
    # db.session.commit()
    # cp = costoProd[0]
    # print(costoProd[0])
    

    return render_template('produccionModule/produccion.html', optRecetas = optRecetas )




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







def guardarProduccion():

    create_form = forms.produccionForm(request.form)
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
        print(costoProd[0])

        idUs = db.session.query(Usuarios.idUsuario).filter(Usuarios.nombre.like('%Mario%')).scalar()
        fechaProd = datetime.now()
        fechaCad = request.form.get('fechaCaducidad')   

        prod = Produccion(
            #costoProduccion = costoProd,
            #fechaProduccion = fechaProd,
            #fechaCaducidad = fechaCad
            costoProduccion = costoProd[0],
            fechaProduccion = fechaProd,
            fechaCaducidad = fechaCad,
            idUsuario = idUs
        )
        db.session.add(prod)
        db.session.commit()





        rebajarInventarioMP(receta)




        print('Operacion realizada.')


    return render_template('produccionModule/produccion.html', costoProduccion = costoProd[0], optRecetas = optRecetas)





    