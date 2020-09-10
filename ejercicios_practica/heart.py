#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

from myTinymongoLibrary import *
from config import config

import os
import requests
import json

script_path = os.path.dirname(os.path.realpath(__file__))
config_path_name = os.path.join(script_path, 'config.ini')

db = config('db', config_path_name)
server = config('server', config_path_name)

@connect(db['database'])
def clear(db=None):
    db.titulo.remove({})


@connect(db['database'])
def fill(db=None):
    url = 'https://jsonplaceholder.typicode.com/todos'
    response = requests.get(url)
    dataset = response.json()
    db.titulo.insert_many(dataset)


@connect(db['database'])
def fetch_data(db=None):
    users = [1, 2, 3, 4, 5, 6 ,7 ,8 , 9, 10]
    titles = [db.titulo.find({"userId": i, "completed": True}).count() for i in users]
    data = {'user': users, 'title': titles}
    return data


@connect(db['database'])
def nationality_review(userId, db=None):
    return db.titulo.find({"userId": int(userId), "completed": True}).count()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def report(limit=0, offset=0):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    query = 'SELECT name, age, nationality FROM persona'

    if limit > 0:
        query += ' LIMIT {}'.format(limit)
        if offset > 0:
            query += ' OFFSET {}'.format(offset)

    query += ';'

    c.execute(query)
    query_results = c.fetchall()

    # Cerrar la conexión con la base de datos
    conn.close()
    return query_results


