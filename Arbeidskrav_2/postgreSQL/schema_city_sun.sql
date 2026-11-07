CREATE TABLE city (
    id SERIAL PRIMARY KEY,
    city_name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    UNIQUE (city_name, lat, lon)
);


CREATE TABLE solar_day(
    id SERIAL PRIMARY KEY, 
    city_id INTEGER NOT NULL REFERENCES city(id),
    date DATE NOT NULL,
    sunrise TIMESTAMPTZ,
    sunset TIMESTAMPTZ,
    day_length_seconds INTEGER,
    sunrise_azimuth DOUBLE PRECISION,
    solar_noon_altitude DOUBLE PRECISION,
    moon_illumination DOUBLE PRECISION NOT NULL CHECK (moon_illumination BETWEEN 0 AND 100),
    UNIQUE(city_id, date)
);