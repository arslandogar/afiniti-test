--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2 (Ubuntu 12.2-4)
-- Dumped by pg_dump version 12.2 (Ubuntu 12.2-4)

-- Started on 2020-05-15 13:34:22 PKT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 27965)
-- Name: snmpSignals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."snmpSignals" (
    "signalValue" text,
    "signalTime" timestamp without time zone
);


ALTER TABLE public."snmpSignals" OWNER TO postgres;

--
-- TOC entry 2957 (class 0 OID 27965)
-- Dependencies: 202
-- Data for Name: snmpSignals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."snmpSignals" ("signalValue", "signalTime") FROM stdin;
hello	2020-05-15 07:20:39.675992
first enrty	2020-05-15 07:21:26.262842
second enrty	2020-05-15 07:21:33.58466
third enrty	2020-05-15 07:21:40.997379
\.


-- Completed on 2020-05-15 13:34:23 PKT

--
-- PostgreSQL database dump complete
--

