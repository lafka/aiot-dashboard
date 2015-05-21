--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: device; Type: TABLE; Schema: public; Owner: aiot; Tablespace: 
--

CREATE TABLE device (
    key text NOT NULL,
    room text
);


ALTER TABLE public.device OWNER TO aiot;

--
-- Name: room; Type: TABLE; Schema: public; Owner: aiot; Tablespace: 
--

CREATE TABLE room (
    key text NOT NULL,
    name text
);


ALTER TABLE public.room OWNER TO aiot;

--
-- Name: room_state; Type: TABLE; Schema: public; Owner: aiot; Tablespace: 
--

CREATE TABLE room_state (
    guid uuid NOT NULL,
    datetime timestamp without time zone,
    room text,
    s_co2 integer,
    s_db integer,
    s_movement boolean,
    s_temperature integer,
    s_moist integer,
    s_light integer
);


ALTER TABLE public.room_state OWNER TO aiot;

--
-- Data for Name: device; Type: TABLE DATA; Schema: public; Owner: aiot
--

COPY device (key, room) FROM stdin;
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: aiot
--

COPY room (key, name) FROM stdin;
\.


--
-- Data for Name: room_state; Type: TABLE DATA; Schema: public; Owner: aiot
--

COPY room_state (guid, datetime, room, s_co2, s_db, s_movement, s_temperature, s_moist, s_light) FROM stdin;
\.


--
-- Name: pk; Type: CONSTRAINT; Schema: public; Owner: aiot; Tablespace: 
--

ALTER TABLE ONLY device
    ADD CONSTRAINT pk PRIMARY KEY (key);


--
-- Name: room_pkey; Type: CONSTRAINT; Schema: public; Owner: aiot; Tablespace: 
--

ALTER TABLE ONLY room
    ADD CONSTRAINT room_pkey PRIMARY KEY (key);


--
-- Name: room_state_pkey; Type: CONSTRAINT; Schema: public; Owner: aiot; Tablespace: 
--

ALTER TABLE ONLY room_state
    ADD CONSTRAINT room_state_pkey PRIMARY KEY (guid);


--
-- Name: fk; Type: FK CONSTRAINT; Schema: public; Owner: aiot
--

ALTER TABLE ONLY room_state
    ADD CONSTRAINT fk FOREIGN KEY (room) REFERENCES room(key);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

