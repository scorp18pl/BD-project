from sqlite3 import connect
import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text

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
    return render_template('index.html', planets=planets)

if __name__ == '__main__':
    app.run()

