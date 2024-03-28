

from flask import Flask, render_template,request,redirect, url_for
from flask import  g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from datetime import datetime
from models import db
from sqlalchemy import func

app = Flask (__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
         db.create_all()
    app.run()