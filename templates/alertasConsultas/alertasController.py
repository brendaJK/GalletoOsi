from flask import render_template, request, redirect, url_for, current_app, jsonify
from models import db
from sqlalchemy import text, update 


def alertaCatidadStock():
    try:
        consulta = """
        SELECT * 
        FROM inventario_galletas 
        WHERE cantidadStock <= 40 AND Estatus = 'En stock'
        """
        cursor = db.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        return resultados

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        return None

    finally:
        cursor.close()
