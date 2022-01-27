# CREATE TABLE Element (
#     element_name VARCHAR(16) NOT NULL,
#     atomic_number NUMERIC(3) PRIMARY KEY,
#     mass_number NUMERIC(6, 3) NOT NULL
# );

class Element:
    def __init__(self, element_name, atomic_number, mass_number):
        self.element_name = element_name
        self.atomic_number = atomic_number
        self.mass_number = mass_number

# CREATE TABLE Atmosphere (
#     id NUMERIC(6) PRIMARY KEY,
#     pressure NUMERIC(9, 3) NOT NULL
# );

class Atmosphere:
    def __init__(self, id, pressure):
        self.id = id
        self.pressure = pressure

# CREATE TABLE Composition (
#     id NUMERIC(6) PRIMARY KEY,
#     atmosphere NUMERIC(6) NOT NULL REFERENCES Atmosphere,
#     concentration NUMERIC(3, 2) NOT NULL,
#     element NUMERIC(3) NOT NULL REFERENCES Element,
#     CONSTRAINT concentration_check CHECK ((0.00 <= concentration) AND (concentration <= 1.00))
# );

class Composition:
    def __init__(self, id, atmosphere, concentration, element):
        self.id = id
        self.atmosphere = atmosphere
        self.concentration = concentration
        self.element = element

# CREATE TABLE Race (
#     id NUMERIC(6) PRIMARY KEY,
#     identif VARCHAR(16),

#     temperature NUMERIC(4),
#     grav_acc NUMERIC(4, 2),
#     hermit_level NUMERIC(3, 2),
#     peacefulness NUMERIC(3,2),
#     planet_type VARCHAR(16),
#     atmosphere NUMERIC(6) NOT NULL REFERENCES Atmosphere,
#     CONSTRAINT type_check CHECK (planet_type IN ('rocky', 'gaseous')),
#     CONSTRAINT h_level_check CHECK ((0.00 <= hermit_level) AND (hermit_level <= 1.00)),
#     CONSTRAINT peacefulness_check CHECK ((0.00 <= peacefulness) AND (peacefulness <= 1.00))
# );

class Race:
    def __init__(self, id, identif, temperature, grav_acc, hermit_level, peacefulness, planet_type, favourite_element):
        self.id = id
        self.identif = identif
        self.temperature = temperature
        self.grav_acc = grav_acc
        self.hermit_level = hermit_level
        self.peacefulness = peacefulness
        self.planet_type = planet_type
        self.favourite_element = favourite_element

# CREATE TABLE Galaxy (
#     id NUMERIC(6) PRIMARY KEY,
#     identif VARCHAR(16) NOT NULL,
#     distance NUMERIC(8) NOT NULL
# );

class Galaxy:
    def __init__(self, id, identif, distance):
        self.id = id
        self.identif = identif
        self.distance = distance

# CREATE TABLE SolarSystem (
#     id NUMERIC(6) PRIMARY KEY,
#     identif VARCHAR(16) NOT NULL,
#     stability NUMERIC(3, 2) NOT NULL,
#     galaxy NUMERIC(6) NOT NULL REFERENCES Galaxy,
#     CONSTRAINT stabilnosc_check CHECK ((0.00 <= stability) AND (stability <= 1.00))
# );

class SolarSystem:
    def __init__(self, id, identif, stability, galaxy):
        self.id = id
        self.identif = identif
        self.stability = stability
        self.galaxy = galaxy

# CREATE TABLE Star (
#     id NUMERIC(6) PRIMARY KEY,
#     identif VARCHAR(16) NOT NULL,
#     luminosity NUMERIC(9, 2) NOT NULL, -- measured in Sun Luminosities
#     mass NUMERIC(6, 3) NOT NULL, -- measured in Sun masses
#     solar_system NUMERIC(6) NOT NULL REFERENCES SolarSystem
# );

class Star:
    def __init__(self, id, identif, luminosity, mass, solar_system):
        self.id = id
        self.identif = identif
        self.luminosity = luminosity
        self.mass = mass
        self.solar_system = solar_system

# CREATE TABLE Planet (
#     id NUMERIC(6) PRIMARY KEY,
#     identif VARCHAR(16) NOT NULL,

#     planet_type VARCHAR(16) NOT NULL,
#     mass NUMERIC(6, 4) NOT NULL, -- measured in Jupiter masses
#     radius NUMERIC(6, 4) NOT NULL, -- measured in Jupiter radii
#     atmosphere NUMERIC(6) NOT NULL REFERENCES Atmosphere,

#     star NUMERIC(6) NOT NULL REFERENCES Star,
#     star_distance NUMERIC(6,3) NOT NULL, -- measured in AU
#     alien_aggression_level NUMERIC(3, 2), -- NULL if not inhibited
#     CONSTRAINT type_check CHECK (planet_type IN ('rocky', 'gaseous')),
#     CONSTRAINT level_check CHECK ((0.00 <= alien_aggression_level) AND (alien_aggression_level <= 1.00))
# );

class Planet:
    def __init__(self, id, identif, planet_type, mass, radius, atmosphere, star, star_distance, alien_aggression_level):
        self.id = id
        self.identif = identif
        self.planet_type = planet_type
        self.mass = mass
        self.radius = radius
        self.atmosphere = atmosphere
        self.star = star
        self.star_distance = star_distance
        self.alien_aggression_level = alien_aggression_level
