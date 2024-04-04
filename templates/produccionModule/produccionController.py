from flask import render_template, request, redirect, url_for
from models import db
import forms
from models import Produccion

def produccion():

    print('Si jala jaja.')

    return render_template('produccionModule/produccion.html')