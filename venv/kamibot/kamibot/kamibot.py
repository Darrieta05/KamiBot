# coding = UTF-8

import os, pymongo
from flask import Flask, request, session, redirect, url_for,  render_template, json, jsonify, Response
from flask_pymongo import PyMongo


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


@app.route('/api/comandos')
def sh_comandos():
    comandos = mongo.db.commandos

    resultado = []

    for i in comandos.find():
        resultado.append({"documentacion" : i["doc"], "nombre" : i["name"]})

    return jsonify({"comandos" : resultado})

@app.route('/api/agrega', methods=['POST'])
def add_comandos():
    comando = mongo.db.commandos

    name = request.json["name"]
    doc = request.json["doc"]
    base = request.json["base"]
    param1 = request.json["param1"]
    param2 = request.json["param2"]
    param3 = request.json["param3"]

    comando_id = comando.insert({"name" : name, "doc" : doc, "base" : base, "param1" : param1, "param2" : param2, "param3" : param3})
    nuevo_comando = comando.find_one({"_id" : comando_id})

    resultado = {"name" : nuevo_comando["name"], "doc" : nuevo_comando["doc"]}

    return jsonify({"resultado": resultado})

@app.route('/api/comandos/<nombre>', methods=['GET'])
def find_comando(nombre):
    comandos = mongo.db.commandos

    s = comandos.find_one({"name": nombre})
    if s:
        resultado = {"name": s["name"], "documentacion" : s["doc"]}
    else:
        resultado = "Ningun comando con ese nombre"

    return jsonify({"resultado": resultado})

@app.route('/api/ejecuta/<nombre>', methods=['POST'])
def ex_comando(nombre):
    comando = mongo.db.commandos
    base = param1 = param2 = param3 = ""

    s = comando.find_one({"name": nombre})
    if s:
        in_args = request.args
        base = s["base"]
        param1 = in_args["param1"]
        param3 = in_args["param3"]
        param2 = in_args["param2"]

        resultado = "" + base + " " + param1 + " " + param2 + " " + param3
    else:
        resultado = "Ningun comando con ese nombre"

    return jsonify({"resultado": resultado})

@app.route('/api/actualiza/<nombre>', methods=['POST', 'GET'])
def upd_comando(nombre):
    comando  = mongo.db.commandos

    s = comando.find_one({"name": nombre})

    if s:
        in_args = request.args
        nombre_dato = in_args["param1"]
        nombre_nuevo = in_args["param2"]

        s[nombre_dato] = nombre_nuevo
        comando.save(s)

        resultado = {"name": s["name"], "documentacion" : s["doc"]}
    else:
        resultado = "Ningun comando con ese nombre"

    return jsonify({"actualiza": resultado})

@app.route('/api/borrar/<nombre>')
def del_comando(nombre):
    comando = mongo.db.commandos

    s = comando.find_one({"name": nombre})
    if s:
        comando.remove(s)
        resultado = "Eliminado exitosamente" + s["name"]
    else:
        resultado = "Ningún comando con ese nombre"


    return jsonify("resultado": resultado)


if __name__ == '__main__':
    app.run(debug=True)

