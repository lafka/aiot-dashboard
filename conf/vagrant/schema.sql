-- Main entities
CREATE TABLE room_type (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    manminutes_capacity INTEGER NOT NULL
);

CREATE TABLE room (
    key TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    room_type_id INTEGER REFERENCES room_type(id),
    area numeric(6, 2) DEFAULT 0
);

CREATE TABLE device (
    key TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL
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

CREATE TABLE ts_decibel (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_movement (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value BOOLEAN NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_temperature (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_moist (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_light (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_pulses (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value INTEGER NOT NULL,
    packet_number INTEGER NOT NULL
);

-- Other time series (that is calculated based on sensor data "in the
-- background")

-- Calculated from `ts_pulses`
CREATE TABLE ts_kwm (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

-- Calculated from `ts_kwm`
CREATE TABLE ts_kwh (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    UNIQUE(datetime, device_key)
);

-- Calculated from sensor data
CREATE TABLE ts_persons_inside (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    value DOUBLE PRECISION NOT NULL
);

-- Calculated from `ts_persons_inside` and `ts_kwm`.
CREATE TABLE ts_energy_productivity (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    value DOUBLE PRECISION NOT NULL
);

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
        ts_persons_inside.datetime, ts_persons_inside.device_key, (ts_persons_inside.value / room_type.manminutes_capacity) AS value
    FROM
        ts_persons_inside
    INNER JOIN
        map_device_room
    ON
        ts_persons_inside.device_key = map_device_room.device_key
    INNER JOIN
        room
    ON
        room.key = map_device_room.room_key
    INNER JOIN
        room_type
    ON
        room.room_type_id = room_type.id;


-- Deviations
CREATE TABLE deviations (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    deviation_type TEXT NOT NULL
);