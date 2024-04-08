import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'Clave Unica'
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:InaliQ01_21@127.0.0.1/crispy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False