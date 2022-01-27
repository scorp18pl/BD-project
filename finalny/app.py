import os
import psycopg2
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from tablenames import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

def get_element(atomic_number):
    cursor.execute("SELECT * FROM element WHERE atomic_number=" + str(atomic_number))
    element = cursor.fetchall()[0]
    element_obj = Element(element[0], element[1], element[2])
    return element_obj

@app.route("/races/<int:race_id>")
def show_race(race_id):
    race = get_race(race_id)
    return render_template('race.html', race=get_race(race_id), element=get_element(race.favourite_element))

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
        fav_elem = request.form["fav_elem"]

        if len(name) > 16:
            error = "name length cannot exceed 16 characters"
            return render_template('race_creation.html', error_msg = error)

        if planet_type == 0:
            planet_type = "rocky"
        else:
            planet_type = "gaseous"

        race_insert(name, int(temperature), float(grav_acc) / 100.0, float(hermit_lvl) / 100.0, float(peace_lvl) / 100.0, planet_type, fav_elem)
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

def get_atmosphere(atmosphere_id):
    cursor.execute("SELECT * FROM atmosphere WHERE id=" + str(atmosphere_id))
    atmosphere = cursor.fetchall()[0]
    atmosphere_obj = Atmosphere(atmosphere[0], atmosphere[1])
    return atmosphere_obj

def get_compositions(atmosphere_id):
    cursor.execute("SELECT * FROM composition WHERE atmosphere=" + str(atmosphere_id))
    compositions = cursor.fetchall()
    compositions_obj = []
    for comp in compositions:
        compositions_obj.append(Composition(comp[0], comp[1], comp[2], comp[3]))
    return compositions_obj

def get_star(star_id):
    cursor.execute("SELECT * FROM star WHERE id=" + str(star_id))
    star = cursor.fetchall()[0]
    star_obj = Star(star[0], star[1], star[2], star[3], star[4])
    return star_obj

def get_system(system_id):
    cursor.execute("SELECT * FROM solarsystem WHERE id=" + str(system_id))
    system = cursor.fetchall()[0]
    system_obj = SolarSystem(system[0], system[1], system[2], system[3])
    return system_obj

def get_galaxy(galaxy_id):
    cursor.execute("SELECT * FROM galaxy WHERE id=" + str(galaxy_id))
    galaxy = cursor.fetchall()[0]
    galaxy_obj = Galaxy(galaxy[0], galaxy[1], galaxy[2])
    return galaxy_obj

@app.route("/planets/<int:planet_id>")
def show_planet(planet_id):
    planet = get_planet(planet_id)
    star = get_star(planet.star)
    system = get_system(star.solar_system)
    galaxy = get_galaxy(system.galaxy)
    atmosphere = get_atmosphere(planet.atmosphere)
    compositions = get_compositions(planet.atmosphere)
    return render_template('planet.html', planet = planet, star = star,\
             system = system, galaxy = galaxy, atmosphere = atmosphere,\
                 compositions = compositions)


if __name__ == '__main__':
    app.run()
