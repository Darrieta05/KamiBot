# -*- coding: utf-8 -*-
# imports necesarios para el funcionamiento de Kami
import requests
import os, pymongo, datetime
from bson.json_util import dumps
from flask import Flask, request, session, redirect, url_for,  render_template, json, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId



app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , kamibot.py

# Conección a la base de datos mongo mediante mlab.com
app.config['MONGO_DBNAME']= 'kamibot'
app.config['MONGO_URI'] = 'mongodb://darrieta:Daralu25@ds161049.mlab.com:61049/kamibot'

mongo = PyMongo(app)

# Menjo de errores según el status
@app.errorhandler(404)
def handle_bad_request(e):
    return 'Not Found!'

@app.errorhandler(500)
def handle_bad_server(e):
    return 'Bad Server!'

@app.errorhandler(405)
def handle_bad_server(e):
    return 'Metodo incorrecto!'

@app.errorhandler(400)
def handle_bad_request(e):
    return 'Hey! Bad request!'


@app.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        return "Hola, mi nombre es Kami \n" \
           " para acceder a mi lista de comandos ingresa a  /api/comandos \n" \
           " para ejecutar un comando ingresa a  /api/ejecuta \n" \
           " para agregar un comando nuevo ingresa a /api/agrega \n" \
           " para acceder al Log File ingresa a /api/log"
    else:
        return "Solo funciona con metodo GET"

@app.route('/api/comandos', methods=['GET'])
def sh_comandos():
    if request.method == 'GET':
        comandos = mongo.db.comandos

        resultado = []

        for i in comandos.find():
            resultado.append({"nombre" : i["name"], "documentacion" : i["doc"]})
        save_log("muestra comandos")
        return jsonify({"comandos" : resultado})
    else:
        return "Se esperaba un metodo GET"

@app.route('/api/comandos/<nombre>', methods=['GET'])
def find_comando(nombre):
    if request.method == 'GET':
        comandos = mongo.db.comandos

        s = comandos.find_one({"name": nombre})
        if s:
            resultado = {"name": s["name"], "documentacion" : s["doc"]}
            save_log("busca")
        else:
            resultado = "Ningun comando con ese nombre"

        save_log("busca comando")
        return jsonify({"resultado": resultado})
    else:
        return "Se esperaba un metodo GET"


@app.route('/api/agrega', methods=['POST'])
def add_comandos():
    comando = mongo.db.comandos
    if request.method == 'POST':
        name = request.json["nombre"]
        doc = request.json["doc"]
        code = request.json["codigo"]

        comando_id = comando.insert({"name" : name, "doc" : doc, "code": code})
        nuevo_comando = comando.find_one({"_id" : comando_id})

        resultado = {"name" : nuevo_comando["name"], "doc" : nuevo_comando["doc"]}
        save_log("agrega")
        return jsonify({"resultado": resultado})
    else:
        return "Se esperaba un metodo GET con el codigo dentro en formato JSON"


@app.route('/api/ejecuta/<nombre>', methods=['POST'])
def ex_comando(nombre):
    if request.method == 'POST':
        comando = mongo.db.comandos

        sol_json = request.args
        dict_json = dict(sol_json)
        num_par = len(request.args)
        resultado = None
        print(len(dict_json))
        print(dict_json)
        print(request.args)

        if num_par == 3:
            parametro1 = sol_json['parametro1']
            parametro2 = sol_json['parametro2']
            parametro3 = sol_json['parametro3']
        elif num_par == 2:
            parametro1 = sol_json['parametro1']
            parametro2 = sol_json['parametro2']
        elif num_par == 1:
            parametro1 = sol_json['parametro1']
        else:
            return "No hay parametros"

        s = comando.find_one({"name": nombre})
        if s:
            if s["code"]:
                print(s["code"])
                try:
                    exec s["code"]
                    print(resultado)
                except ValueError:
                    resultado = "Hay un problema con el comando"
                except SyntaxError as err:
                    print err.lineno
            else:
                resultado = "No se encuentra el campo \"code\""
        else:
            resultado = "Ningun comando con ese nombre"

        return jsonify({"resultado": resultado})
        save_log("ejecuta")
    else:
        return "Se esperaba un metodo POST"

@app.route('/api/actualiza/<nombre>', methods=['POST', 'GET'])
def upd_comando(nombre):
    if request.method == 'POST' or request.method == 'GET':
        comando = mongo.db.comandos

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
        save_log("actualiza")
        return jsonify({"actualiza": resultado})
    else:
        return "Se esperaba un metodo POST o GET"

@app.route('/api/borrar/<nombre>', methods=['DELETE'])
def del_comando(nombre):
    if request.method == 'DELETE':
        comando = mongo.db.comandos

        s = comando.find_one({"name": nombre})
        if s:
            comando.remove(s)
            resultado = "Eliminado exitosamente" + s["name"]
        else:
            resultado = "Ningun comando con ese nombre"

        save_log("borrar")
        return jsonify({"resultado": resultado})
    else:
        return "Se esperaba un metodo DELETE"


@app.route('/api/log', methods=['GET'])
def sh_log():
    if request.method == 'GET':
        log = mongo.db.log

        resultado = []

        for i in log.find():
            print (i)
            resultado.append({"accion" : i["accion"], "fecha" : i["fecha"]})
        save_log("muestra log")
        return jsonify({"log" : resultado})

    else:
        return "Se esperaba un metodo GET"


def save_log(accion):
    log = mongo.db.log
    now = datetime.datetime.now()
    now_u = unicode(now.replace(microsecond=0))
    log_id = log.insert({"accion": accion, "fecha": now_u})



if __name__ == '__main__':
    app.run(debug=True)
