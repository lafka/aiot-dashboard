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
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_decibel (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_movement (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value BOOLEAN NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_temperature (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_moist (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_light (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    packet_number INTEGER NOT NULL
);

CREATE TABLE ts_pulses (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value INTEGER NOT NULL,
    packet_number INTEGER NOT NULL
);

-- Other time series (that is calculated based on sensor data "in the
-- background")

-- Calculated from `ts_pulses`
CREATE TABLE ts_kwm (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

-- Calculated from `ts_kwm`
CREATE TABLE ts_kwh (
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device (key) NOT NULL,
    value DOUBLE PRECISION NOT NULL
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

-- Deviations
CREATE TABLE deviations (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE,
    device_key TEXT REFERENCES device(key),
    deviation_type TEXT NOT NULL
);