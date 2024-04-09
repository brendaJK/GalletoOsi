import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
import ssl
import smtplib
import random
import string
from email.message import EmailMessage
from models import Login
from models import db
bcrypt = Bcrypt()

def dashbord():
    return render_template('dashbordModule/dashbord.html') 

