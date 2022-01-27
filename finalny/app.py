import os
import psycopg2
from flask import Flask, render_template, request, redirect
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
    cursor.execute("SELECT * FROM race")
    races = cursor.fetchall()

    races_obj = []
    for race in races:
        races_obj.append(Race(race[0], race[1], race[2], race[3], race[4], race[5], race[6], race[7]))

    return render_template('index.html', races=races_obj)

def get_race(race_id):
    cursor.execute("SELECT * FROM race WHERE id=" + str(race_id))
    race = cursor.fetchall()[0]
    race_obj = Race(race[0], race[1], race[2], race[3], race[4], race[5], race[6], race[7])
    return race_obj

@app.route("/races/<int:race_id>")
def show_race(race_id):
    return render_template('race.html', race=get_race(race_id))

def get_next_free_id():
    cursor.execute("SELECT MAX(id) FROM race")
    id = cursor.fetchall()
    return 1 + id[0][0]

def race_insert(name, temperature, grav_acc, hermit_lvl, peace_lvl, planet_type, fav_elem):
    id = get_next_free_id()
    sql = "INSERT INTO Race(id,identif,temperature,grav_acc,hermit_level,peacefulness,planet_type,favourite_element) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
    params = (id, name, temperature, grav_acc, hermit_lvl, peace_lvl, planet_type, fav_elem)
    cursor.execute(sql, params)
    con.commit()

@app.route("/races/create", methods=["POST", "GET"])
def race_create():
    if request.method == "POST":
        name = request.form["name"]
        temperature = request.form["temperature"]
        grav_acc = request.form["grav_acc"]
        hermit_lvl = request.form["hermit_lvl"]
        peace_lvl = request.form["peace_lvl"]
        planet_type = request.form["planet_type"]

        if planet_type == 0:
            planet_type = "rocky"
        else:
            planet_type = "gaseous"

        race_insert(name, int(temperature), float(grav_acc) / 100.0, float(hermit_lvl) / 100.0, float(peace_lvl) / 100.0, planet_type, 1)
        return redirect("/")
    else:
        return render_template('race_creation.html')

# returns 10 best planets
def find_best_planets(race_id):
    file = open(os.getcwd() + "/finalny/data/sort_planets.sql", "rt")

    query = "WITH sel_race AS (SELECT * FROM race WHERE id = "\
    + str(race_id) + ")," + file.read()

    cursor.execute(query)
    planets = cursor.fetchall()
    planets_obj = []
    for planet in planets:
        planets_obj.append(Planet(planet[0], planet[1], planet[2], planet[3], planet[4], planet[5], planet[6], planet[7], planet[8]))

    return planets_obj

@app.route("/planet_search/<int:race_id>")
def race_best_planets(race_id):
    planets = find_best_planets(race_id)

    return render_template('planet_search.html', planets=planets)

def get_planet(planet_id):
    cursor.execute("SELECT * FROM planet WHERE id=" + str(planet_id))
    planet = cursor.fetchall()[0]
    planet_obj = Planet(planet[0], planet[1], planet[2], planet[3], planet[4], planet[5], planet[6], planet[7], planet[8])
    return planet_obj

@app.route("/planets/<int:planet_id>")
def show_planet(planet_id):
    return render_template('planet.html', planet = get_planet(planet_id))


if __name__ == '__main__':
    app.run()
