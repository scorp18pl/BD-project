-- WITH sel_race AS (SELECT * FROM race WHERE id = race_id), -- this line is dynamic therefore located in the app.py file
planets_params_added AS (
    SELECT id,
    COALESCE(1.0 - alien_aggression_level, 1.0) AS hermit_level,
    atmosphere,
    (
        SELECT (star.luminosity * 2.55 * POWER(10, 4) / planet.star_distance) 
        FROM star
        WHERE star.id = planet.star
    ) ^ 0.25 * 100 AS temperature,
    mass * 24.8 / (radius ^ 2) AS grav_acc,
    (
        SELECT stability 
        FROM solarsystem
        WHERE solarsystem.id = (
            SELECT solar_system
            FROM star
            WHERE star.id = planet.star
        )
    ) AS peacefulness,
    planet_type
    FROM planet
),
best_ids AS (
    SELECT planets_params_added.id
    FROM planets_params_added, sel_race
    ORDER BY ( -- calculate score
            ABS(planets_params_added.temperature - sel_race.temperature) / 20000 +
            ABS(planets_params_added.hermit_level - sel_race.hermit_level) +
        ABS(planets_params_added.peacefulness - sel_race.peacefulness) +
        ABS(planets_params_added.grav_acc - sel_race.grav_acc) / 100 +
        CASE WHEN planets_params_added.planet_type = sel_race.planet_type THEN 0 ELSE 1 END +
        ( -- concentration without the favourite element
            SELECT 1.0 - COALESCE(SUM(concentration),0)
            FROM composition
            WHERE composition.atmosphere = planets_params_added.atmosphere
                AND composition.element = favourite_element
        )
    )
    LIMIT 10
)

SELECT planet.*
FROM planet JOIN best_ids
ON planet.id = best_ids.id;
