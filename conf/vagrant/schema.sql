-- Main entities
CREATE TABLE room_type (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE room (
    key TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    room_type_id INTEGER REFERENCES room_type(id),
    manminutes_capacity INTEGER NOT NULL,
    area numeric(6, 2) DEFAULT 0,
    floor INTEGER default 0
);

CREATE TABLE device (
    key TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    uid INTEGER UNIQUE NOT NULL
);

CREATE TABLE power_circuit (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Many-to-many
CREATE TABLE map_device_room (
    id SERIAL PRIMARY KEY,
    device_key TEXT REFERENCES device (key) NOT NULL,
    room_key TEXT REFERENCES room (key) NOT NULL
);
CREATE UNIQUE INDEX
    map_device_room_keys_unique_idx
ON
    map_device_room (device_key, room_key);

CREATE TABLE map_device_power_circuit (
    id SERIAL PRIMARY KEY,
    device_key TEXT REFERENCES device (key) NOT NULL,
    power_circuit_id INTEGER REFERENCES power_circuit (id) NOT NULL
);
CREATE UNIQUE INDEX
    map_device_power_circuit_keys_unique_idx
ON
    map_device_power_circuit (device_key, power_circuit_id);

-- "Raw" time series
CREATE TABLE ts_co2 (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_co2_datetime_idx ON ts_co2(datetime);

CREATE TABLE ts_decibel (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_decibel_datetime_idx ON ts_decibel(datetime);

CREATE TABLE ts_movement (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value BOOLEAN NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_movement_datetime_idx ON ts_movement(datetime);

CREATE TABLE ts_temperature (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_temperature_datetime_idx ON ts_temperature(datetime);

CREATE TABLE ts_moist (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_moist_datetime_idx ON ts_moist(datetime);

CREATE TABLE ts_light (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_light_datetime_idx ON ts_light(datetime);

CREATE TABLE ts_pulses (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value INTEGER NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_pulses_datetime_idx ON ts_pulses(datetime);

-- Other time series (that is calculated based on sensor data "in the
-- background")

-- Calculated from `ts_pulses`
CREATE TABLE ts_kwm (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL
);
CREATE INDEX ts_kwm_datetime_idx ON ts_kwm(datetime);

-- Calculated from `ts_kwm`
CREATE TABLE ts_kwh (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    UNIQUE(datetime, device_key)
);
CREATE INDEX ts_kwh_datetime_idx ON ts_kwh(datetime);

-- Calculated from sensor data
CREATE TABLE ts_persons_inside (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    value DOUBLE PRECISION NOT NULL
);
CREATE INDEX ts_persons_inside_datetime_idx ON ts_persons_inside(datetime);

-- Calculated from `ts_persons_inside` and `ts_kwm`.
CREATE TABLE ts_energy_productivity (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    value DOUBLE PRECISION NOT NULL
);
CREATE INDEX ts_energy_productivity_datetime_idx ON ts_energy_productivity(datetime);

-- Subjective evaluation
CREATE TABLE ts_subjective_evaluation (
    id SERIAL PRIMARY KEY,
    datetime timestamp with time zone NOT NULL,
    value integer NOT NULL,
    device_key text REFERENCES device(key)
);
CREATE INDEX ts_subjective_evaluation_datetime_idx ON ts_subjective_evaluation(datetime);

-- View for summed kwh for each power circuit
CREATE VIEW
    ts_kwh_network
AS
    SELECT
        datetime, SUM(value) AS value
    FROM
        ts_kwh
    GROUP BY
        datetime
    HAVING
        count(*) = (SELECT COUNT(*) FROM power_circuit);

-- View for room productivity calculations
CREATE VIEW
    ts_room_productivity
AS  
    SELECT
        ts_persons_inside.datetime, ts_persons_inside.device_key, (ts_persons_inside.value / room.manminutes_capacity) AS value
    FROM
        ts_persons_inside
    INNER JOIN
        map_device_room
    ON  
        ts_persons_inside.device_key = map_device_room.device_key
    INNER JOIN
        room
    ON  
        room.key = map_device_room.room_key;

-- Deviations
CREATE TABLE deviations (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    deviation_type TEXT NOT NULL
);
CREATE INDEX deviations_datetime_idx ON deviations(datetime);
CREATE INDEX deviations_deviation_type_idx ON deviations(deviation_type);

-- Wristbands
CREATE TABLE ts_wristband_location (
    id SERIAL PRIMARY KEY,
    device_key TEXT REFERENCES device(key) NOT NULL,
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    nearest_device_key TEXT REFERENCES device(key) NOT NULL,
    rssi INTEGER NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_wristband_location_datetime_idx ON ts_wristband_location(datetime);

CREATE TABLE ts_wristband_button_push (
    id SERIAL PRIMARY KEY,
    device_key TEXT REFERENCES device(key) NOT NULL,
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    packet_number INTEGER NOT NULL
);
CREATE INDEX ts_wristband_button_push_datetime_idx ON ts_wristband_button_push(datetime);
