DROP TABLE IF EXISTS Planet;
DROP TABLE IF EXISTS Star;
DROP TABLE IF EXISTS SolarSystem;
DROP TABLE IF EXISTS Galaxy;
DROP TABLE IF EXISTS Race;
DROP TABLE IF EXISTS Composition;
DROP TABLE IF EXISTS Atmosphere;
DROP TABLE IF EXISTS Element;

DROP FUNCTION IF EXISTS composition_check();

CREATE TABLE Element (
    element_name VARCHAR(16) NOT NULL,
    atomic_number NUMERIC(3) PRIMARY KEY,
    mass_number NUMERIC(6, 3) NOT NULL
);

CREATE TABLE Atmosphere (
    id NUMERIC(6) PRIMARY KEY,
    pressure NUMERIC(9, 3) NOT NULL
);

CREATE TABLE Composition (
    id NUMERIC(6) PRIMARY KEY,
    atmosphere NUMERIC(6) NOT NULL REFERENCES Atmosphere,
    concentration NUMERIC(3, 2) NOT NULL,
    element NUMERIC(8) NOT NULL REFERENCES Element,
    CONSTRAINT concentration_check CHECK ((0.00 <= concentration) AND (concentration <= 1.00))
);

CREATE FUNCTION composition_check() RETURNS trigger AS $$
BEGIN
    -- For each atmosphere perform a percentage check
    IF EXISTS (
        SELECT SUM(concentration) concentration_sum
        FROM Composition
        GROUP BY atmosphere
        HAVING concentration_sum > 1.00
    ) THEN
        RAISE EXCEPTION 'Atmosphere overall composition cannot exceed 1.0';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER composition_check AFTER INSERT OR UPDATE ON Composition
    EXECUTE PROCEDURE composition_check();

CREATE TABLE Race (
    id NUMERIC(6) PRIMARY KEY,
    identif VARCHAR(8),

    temperature NUMERIC(4)L,
    grav_acc NUMERIC(4, 2),
    hermit_level NUMERIC(3, 2),
    peacefulness NUMERIC(3,2),
    planet_type VARCHAR(8),
    atmosphere NUMERIC(6) NOT NULL REFERENCES Atmosphere,
    CONSTRAINT type_check CHECK (planet_type IN ('rocky', 'gaseous')),
    CONSTRAINT h_level_check CHECK ((0.00 <= hermit_level) AND (hermit_level <= 1.00)),
    CONSTRAINT peacefulness_check CHECK ((0.00 <= peacefulness) AND (peacefulness <= 1.00))
);

CREATE TABLE Galaxy (
    id NUMERIC(6) PRIMARY KEY,
    identif VARCHAR(8) NOT NULL,
    distance NUMERIC(8) NOT NULL
);

CREATE TABLE SolarSystem (
    id NUMERIC(6) PRIMARY KEY,
    identif VARCHAR(8) NOT NULL,
    stability NUMERIC(3, 2) NOT NULL,
    galaxy NUMERIC(6) NOT NULL REFERENCES Galaxy,
    CONSTRAINT stabilnosc_check CHECK ((0.00 <= stability) AND (stability <= 1.00))
);

CREATE TABLE Star (
    id NUMERIC(6) PRIMARY KEY,
    identif VARCHAR(8) NOT NULL,
    luminosity NUMERIC(9, 2) NOT NULL, -- measured in Sun Luminosities
    mass NUMERIC(6, 3) NOT NULL, -- measured in Sun masses
    solar_system NUMERIC(6) NOT NULL REFERENCES SolarSystem
);

CREATE TABLE Planet (
    id NUMERIC(6) PRIMARY KEY,
    identif VARCHAR(16) NOT NULL,

    planet_type VARCHAR(16) NOT NULL,
    mass NUMERIC(6, 4) NOT NULL, -- measured in Jupiter masses
    radius NUMERIC(6, 4) NOT NULL, -- measured in Jupiter radii
    atmosphere NUMERIC(6) NOT NULL REFERENCES Atmosphere,

    star NUMERIC(6) NOT NULL REFERENCES Star,
    star_distance NUMERIC(6,3) NOT NULL, -- measured in AU
    alien_aggression_level NUMERIC(3, 2), -- NULL if not inhibited
    CONSTRAINT type_check CHECK (planet_type IN ('rocky', 'gaseous')),
    CONSTRAINT level_check CHECK ((0.00 <= alien_agression_level) AND (alien_agression_level <= 1.00))
);