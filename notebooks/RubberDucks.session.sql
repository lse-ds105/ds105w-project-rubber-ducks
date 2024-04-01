CREATE TABLE new_weather (
    date DATE,
    city VARCHAR(18),
    temperature_2m_max DECIMAL(7,4),
    temperature_2m_min DECIMAL(7,4),
    temperature_2m_mean DECIMAL(7,4),
    daylight_duration DECIMAL(9,3),
    sunshine_duration DECIMAL(9,3),
    precipitation_sum DECIMAL(8,5),
    rain_sum DECIMAL(8,5),
    precipitation_hours TINYINT UNSIGNED
);

INSERT INTO new_weather (date, city, temperature_2m_max, temperature_2m_min, temperature_2m_mean,
                         daylight_duration, sunshine_duration, precipitation_sum, rain_sum, precipitation_hours)
SELECT date, city, temperature_2m_max, temperature_2m_min, temperature_2m_mean,
       daylight_duration, sunshine_duration, precipitation_sum, rain_sum, precipitation_hours
FROM weather;

DROP TABLE weather;

ALTER TABLE new_weather RENAME TO weather;

CREATE TABLE new_perception (
    Year YEAR,
    Perception DECIMAL(18,16)
);

INSERT INTO new_perception (Year, Perception) SELECT Year, Perception FROM perception;

DROP TABLE perception;

ALTER TABLE new_perception RENAME TO perception;