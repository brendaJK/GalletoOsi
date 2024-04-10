import os
from flask_login import login_required
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
import ssl
import smtplib
import random
import string
from email.message import EmailMessage

bcrypt = Bcrypt()

@login_required
def dashbord():
    
    return render_template('dashbordModule/dashbord.html') 

