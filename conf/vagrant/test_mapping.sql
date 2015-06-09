DELETE FROM map_device_room;
INSERT INTO map_device_room (device_key, room_key) VALUES ('22hBnpfut3', '1549044333');
INSERT INTO map_device_room (device_key, room_key) VALUES ('csv4LNZko', '1549044331');
INSERT INTO map_device_room (device_key, room_key) VALUES ('y6VzAaCrR', '1549044343');
INSERT INTO map_device_room (device_key, room_key) VALUES ('4jkQdvPYUV', '1549044334');
INSERT INTO map_device_room (device_key, room_key) VALUES ('tyGl4tMlF', '1549044341');
INSERT INTO map_device_room (device_key, room_key) VALUES ('3qCkacNT0K', '1549044336');
INSERT INTO map_device_room (device_key, room_key) VALUES ('5G34dVlbCg', '1549044352');
INSERT INTO map_device_room (device_key, room_key) VALUES ('59SO9rKa7Y', '1549044349');
INSERT INTO map_device_room (device_key, room_key) VALUES ('xutYD5rf5', '1549044347');
INSERT INTO map_device_room (device_key, room_key) VALUES ('4KdDYEyTsZ', '1549044337');
INSERT INTO map_device_room (device_key, room_key) VALUES ('JCj1aWnGX', '1549044339');
INSERT INTO map_device_room (device_key, room_key) VALUES ('2HtVzVqhif', '1549044329');
INSERT INTO map_device_room (device_key, room_key) VALUES ('BNFDJhO80', '1549044330');
INSERT INTO map_device_room (device_key, room_key) VALUES ('2AuFfVWYhu', '1549044338');
INSERT INTO map_device_room (device_key, room_key) VALUES ('2paQUay3fK', '1549044320');
INSERT INTO map_device_room (device_key, room_key) VALUES ('3xqiFKTuUX', '1549044323');
INSERT INTO map_device_room (device_key, room_key) VALUES ('2RgFa5cB7X', '1549044350');
INSERT INTO map_device_room (device_key, room_key) VALUES ('TglwFPpsA', '1549044322');

DELETE FROM power_circuit;
INSERT INTO power_circuit (name) VALUES ('Strømtavle 1'), ('Strømtavle 2'), ('Strømtavle 3'), ('Strømtavle 4');

DELETE FROM map_device_power_circuit;
INSERT INTO map_device_power_circuit (device_key, power_circuit_id) VALUES
    ('1kpteGU0Nw', (select id from power_circuit where name = 'Strømtavle 1')),
    ('1DtLin87nq', (select id from power_circuit where name = 'Strømtavle 2')),
    ('2prom5hj67', (select id from power_circuit where name = 'Strømtavle 3')),
    ('6PavU6On2', (select id from power_circuit where name = 'Strømtavle 4'));