DELETE FROM map_device_room;
INSERT INTO map_device_room (device_key, room_key) VALUES ('csv4LNZko', (select key from room where name = 'A2-205'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('BNFDJhO80', (select key from room where name = 'A2-209'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('y6VzAaCrR', (select key from room where name = 'A2-210'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('tyGl4tMlF', (select key from room where name = 'A2-214'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('JCj1aWnGX', (select key from room where name = 'A2-218'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('xutYD5rf5', (select key from room where name = 'A2-221'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('22hBnpfut3', (select key from room where name = 'A2-201'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('3xqiFKTuUX', (select key from room where name = 'A2-206'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('2HtVzVqhif', (select key from room where name = 'A2-207'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('4jkQdvPYUV', (select key from room where name = 'A2-211'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('5G34dVlbCg', (select key from room where name = 'A2-220'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('2RgFa5cB7X', (select key from room where name = 'A2-224'));
INSERT INTO map_device_room (device_key, room_key) VALUES ('59SO9rKa7Y', (select key from room where name = 'A2-225'));

DELETE FROM power_circuit;
INSERT INTO power_circuit (name) VALUES ('Strømtavle 1'), ('Strømtavle 2'), ('Strømtavle 3'), ('Strømtavle 4');

DELETE FROM map_device_power_circuit;
INSERT INTO map_device_power_circuit (device_key, power_circuit_id) VALUES
    ('1kpteGU0Nw', (select id from power_circuit where name = 'Strømtavle 1')),
    ('1DtLin87nq', (select id from power_circuit where name = 'Strømtavle 2')),
    ('2prom5hj67', (select id from power_circuit where name = 'Strømtavle 3')),
    ('6PavU6On2', (select id from power_circuit where name = 'Strømtavle 4'));
