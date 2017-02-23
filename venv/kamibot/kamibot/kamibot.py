# coding = UTF-8

import os, pymongo
from flask import Flask, request, session, redirect, url_for,  render_template, json, jsonify, Response
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , kamibot.py
app.config['MONGO_DBNAME']= 'kamibot'
app.config['MONGO_URI'] = 'mongodb://darrieta:Daralu25@ds161049.mlab.com:61049/kamibot'

mongo = PyMongo(app)

@app.route('/api', methods=['GET'])
def index():
    return "Hola, mi nombre es Kami \n" \
           " para acceder a mi lista de comandos ingresa a  /api/comandos \n" \
           " para ejecutar un comando ingresa a  /api/ejecuta \n" \
           " para agregar un comando nuevo ingresa a /api/agrega \n" \
           " para acceder al Log File ingresa a /api/log"




if __name__ == '__main__':
    app.run(debug=True)

