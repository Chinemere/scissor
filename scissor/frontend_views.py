from flask_restx import Namespace, Resource
from flask import render_template
from scissor import app


home_namespace= Namespace('home',  description=' The home page')



@app.route('/home/')
def home():
    return render_template('index.html')
