#!/usr/bin/env python
'''
API Personas
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las personas registradas.

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
NOTA: Si es la primera vez que se lanza este programa crear la base de datos
entrando a la siguiente URL
http://127.0.0.1:5000/reset

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.0"

# Realizar HTTP POST --> https://www.codepunker.com/tools/http-requests

import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect
import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

import heart

app = Flask(__name__)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /user/{id}/titles --> informa cuantos titulos completó el usuario cuyo id es el pasado como parámetro en la URL estática</h3>"
        result += "<h3>[GET] /user/graph --> informa el reporte y la comparativa de cuantos títulos completó cada usuario en un gráfico</h3>"
        result += "<h3>[GET] /user/table --> informa cuantos títulos completó cada usuario en una tabla JSON</h3>"
        
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/user/<id>/titles")
def user_id_title(id):
    try:
        completed_titles = heart.nationality_review(id)
        response = f"<h1>El usuario {id} ha completado {completed_titles} titulos/h1>"
        return response
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/user/graph")
def user_graph():
    try:        
        data = heart.fetch_data()

        fig, ax = plt.subplots(figsize=(16, 9))

        height = data['title']
        bars = [f'Usuario {i}' for i in data['user']]
        y_pos = np.arange(len(bars))

        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)

        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/user/table")
def user_table():
    try:
        data = heart.fetch_data()
        response = f"<h1>LISTADO DE TITULOS COMPLETADOS x USUARIO: </h1>"
        for i, data in zip(data['user'], data['title']):
            response += f"<h2>  - Usuario {i}: {data} titulos </h2>"
        return response
    except:
        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':

    # Borrar DB
    heart.clear()

    # Completar la DB con el JSON request
    heart.fill()

    print('Servidor arriba!')
    app.run(host=heart.server['host'],
            port=heart.server['port'],
            debug=True)