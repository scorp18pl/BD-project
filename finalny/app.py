import psycopg2
from sqlite3 import connect
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from tablenames import *

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://scorp2:1234@localhost/planet_search'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
con = psycopg2.connect(database="planet_search", user="scorp2", password="1234", host="127.0.0.1", port="5432")
cursor = con.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM planet")
    planets = cursor.fetchall()

    planets_obj = []
    for planet in planets:
        planets_obj.append(Planet(planet[0], planet[1], planet[2], 
                                    planet[3], planet[3], planet[4], 
                                    planet[5], planet[6], planet[7]))

    return render_template('index.html', planets=planets_obj)

if __name__ == '__main__':
    app.run()

