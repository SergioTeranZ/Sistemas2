--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

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
-- Name: act_posee_campo; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE act_posee_campo (
    id_tipo_act integer NOT NULL,
    id_campo integer NOT NULL
);


ALTER TABLE act_posee_campo OWNER TO "Siradex";

--
-- Name: auth_cas; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE auth_cas (
    id integer NOT NULL,
    user_id integer,
    created_on timestamp without time zone,
    service character varying(512),
    ticket character varying(512),
    renew character(1)
);


ALTER TABLE auth_cas OWNER TO "Siradex";

--
-- Name: auth_cas_id_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE auth_cas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_cas_id_seq OWNER TO "Siradex";

--
-- Name: auth_cas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE auth_cas_id_seq OWNED BY auth_cas.id;


--
-- Name: auth_event; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE auth_event (
    id integer NOT NULL,
    time_stamp timestamp without time zone,
    client_ip character varying(512),
    user_id integer,
    origin character varying(512),
    description text
);


ALTER TABLE auth_event OWNER TO "Siradex";

--
-- Name: auth_event_id_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE auth_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_event_id_seq OWNER TO "Siradex";

--
-- Name: auth_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE auth_event_id_seq OWNED BY auth_event.id;


--
-- Name: auth_membership; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE auth_membership (
    id integer NOT NULL,
    user_id integer,
    group_id integer
);


ALTER TABLE auth_membership OWNER TO "Siradex";

--
-- Name: auth_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE auth_membership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_membership_id_seq OWNER TO "Siradex";

--
-- Name: auth_membership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE auth_membership_id_seq OWNED BY auth_membership.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    group_id integer,
    name character varying(512),
    table_name character varying(512),
    record_id integer
);


ALTER TABLE auth_permission OWNER TO "Siradex";

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO "Siradex";

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: backup; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE backup (
    id_backup integer NOT NULL,
    descripcion character varying(256),
    fecha date
);


ALTER TABLE backup OWNER TO "Siradex";

--
-- Name: backup_id_backup_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE backup_id_backup_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE backup_id_backup_seq OWNER TO "Siradex";

--
-- Name: backup_id_backup_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE backup_id_backup_seq OWNED BY backup.id_backup;


--
-- Name: campo; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE campo (
    id_campo integer NOT NULL,
    id_catalogo integer,
    nombre character varying(256),
    tipo_campo character varying(64),
    obligatorio boolean DEFAULT false
);


ALTER TABLE campo OWNER TO "Siradex";

--
-- Name: campo_catalogo; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE campo_catalogo (
    id_campo_cat integer NOT NULL,
    id_catalogo integer,
    nombre character varying(256),
    tipo_campo character varying(64),
    obligatorio boolean DEFAULT false
);


ALTER TABLE campo_catalogo OWNER TO "Siradex";

--
-- Name: campo_catalogo_id_campo_cat_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE campo_catalogo_id_campo_cat_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE campo_catalogo_id_campo_cat_seq OWNER TO "Siradex";

--
-- Name: campo_catalogo_id_campo_cat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE campo_catalogo_id_campo_cat_seq OWNED BY campo_catalogo.id_campo_cat;


--
-- Name: campo_id_campo_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE campo_id_campo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE campo_id_campo_seq OWNER TO "Siradex";

--
-- Name: campo_id_campo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE campo_id_campo_seq OWNED BY campo.id_campo;


--
-- Name: catalogo; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE catalogo (
    id_catalogo integer NOT NULL,
    nro_campos integer,
    nombre character varying(128)
);


ALTER TABLE catalogo OWNER TO "Siradex";

--
-- Name: catalogo_id_catalogo_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE catalogo_id_catalogo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catalogo_id_catalogo_seq OWNER TO "Siradex";

--
-- Name: catalogo_id_catalogo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE catalogo_id_catalogo_seq OWNED BY catalogo.id_catalogo;


--
-- Name: comprobante; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE comprobante (
    id_comprobante integer NOT NULL,
    archivo character varying(256) NOT NULL,
    descripcion character varying(100),
    producto integer
);


ALTER TABLE comprobante OWNER TO "Siradex";

--
-- Name: comprobante_id_comprobante_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE comprobante_id_comprobante_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comprobante_id_comprobante_seq OWNER TO "Siradex";

--
-- Name: comprobante_id_comprobante_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE comprobante_id_comprobante_seq OWNED BY comprobante.id_comprobante;


--
-- Name: gestiona_catalogo; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE gestiona_catalogo (
    id_jefe integer NOT NULL,
    id_catalogo integer NOT NULL
);


ALTER TABLE gestiona_catalogo OWNER TO "Siradex";

--
-- Name: gestiona_tipo_act; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE gestiona_tipo_act (
    id_jefe integer NOT NULL,
    id_tipo_act integer NOT NULL
);


ALTER TABLE gestiona_tipo_act OWNER TO "Siradex";

--
-- Name: jefe_dependencia; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE jefe_dependencia (
    id_jefe integer NOT NULL,
    usbid_usuario character varying(20) NOT NULL
);


ALTER TABLE jefe_dependencia OWNER TO "Siradex";

--
-- Name: jefe_dependencia_id_jefe_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE jefe_dependencia_id_jefe_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE jefe_dependencia_id_jefe_seq OWNER TO "Siradex";

--
-- Name: jefe_dependencia_id_jefe_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE jefe_dependencia_id_jefe_seq OWNED BY jefe_dependencia.id_jefe;


--
-- Name: log_siradex; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE log_siradex (
    accion text NOT NULL,
    accion_fecha date NOT NULL,
    accion_ip character varying(256) NOT NULL,
    descripcion text,
    usbid_usuario character varying(20)
);


ALTER TABLE log_siradex OWNER TO "Siradex";

--
-- Name: participa_producto; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE participa_producto (
    usbid_usuario character varying(20) NOT NULL,
    id_producto integer NOT NULL
);


ALTER TABLE participa_producto OWNER TO "Siradex";

--
-- Name: permisos_tipo_act; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE permisos_tipo_act (
    permiso character varying(256) NOT NULL,
    id_tipo integer NOT NULL
);


ALTER TABLE permisos_tipo_act OWNER TO "Siradex";

--
-- Name: producto; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE producto (
    id_producto integer NOT NULL,
    id_tipo integer,
    nombre character varying(128),
    descripcion character varying(256),
    estado character varying DEFAULT 'En Espera'::character varying,
    evaluacion_criterio character varying(256),
    evaluacion_valor character varying(256),
    fecha_realizacion date,
    fecha_modificacion date,
    lugar character varying(50),
    usbid_usu_modificador character varying(20),
    usbid_usu_creador character varying(20)
);


ALTER TABLE producto OWNER TO "Siradex";

--
-- Name: producto_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE producto_id_producto_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE producto_id_producto_seq OWNER TO "Siradex";

--
-- Name: producto_id_producto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE producto_id_producto_seq OWNED BY producto.id_producto;


--
-- Name: producto_tiene_campo; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE producto_tiene_campo (
    id_prod integer NOT NULL,
    id_campo integer NOT NULL,
    valor_campo character varying(512)
);


ALTER TABLE producto_tiene_campo OWNER TO "Siradex";

--
-- Name: programa; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE programa (
    id_programa integer NOT NULL,
    nombre character varying(256) NOT NULL,
    abreviacion character varying(10) NOT NULL,
    descripcion character varying(2048) NOT NULL,
    papelera boolean DEFAULT false NOT NULL,
    modif_fecha date,
    usbid_usu_modificador character varying(20)
);


ALTER TABLE programa OWNER TO "Siradex";

--
-- Name: programa_id_programa_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE programa_id_programa_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE programa_id_programa_seq OWNER TO "Siradex";

--
-- Name: programa_id_programa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE programa_id_programa_seq OWNED BY programa.id_programa;


--
-- Name: tipo_actividad; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE tipo_actividad (
    id_tipo integer NOT NULL,
    nombre character varying(128) NOT NULL,
    tipo_p_r character varying(1) NOT NULL,
    descripcion character varying(2048) NOT NULL,
    id_programa integer NOT NULL,
    validacion character varying(128) NOT NULL,
    producto character varying(256),
    nro_campos integer,
    id_jefe_creador integer,
    usbid_usuario_propone character varying(20),
    papelera boolean DEFAULT false NOT NULL,
    modif_fecha date
);


ALTER TABLE tipo_actividad OWNER TO "Siradex";

--
-- Name: tipo_actividad_id_tipo_seq; Type: SEQUENCE; Schema: public; Owner: Siradex
--

CREATE SEQUENCE tipo_actividad_id_tipo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tipo_actividad_id_tipo_seq OWNER TO "Siradex";

--
-- Name: tipo_actividad_id_tipo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Siradex
--

ALTER SEQUENCE tipo_actividad_id_tipo_seq OWNED BY tipo_actividad.id_tipo;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: Siradex
--

CREATE TABLE usuario (
    ci character varying(10) NOT NULL,
    usbid character varying(20) NOT NULL,
    nombres character varying(50),
    apellidos character varying(50),
    telefono character varying(15),
    correo_inst character varying(50),
    correo_alter character varying(50),
    tipo character varying(15)
);


ALTER TABLE usuario OWNER TO "Siradex";

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_cas ALTER COLUMN id SET DEFAULT nextval('auth_cas_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_event ALTER COLUMN id SET DEFAULT nextval('auth_event_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_membership ALTER COLUMN id SET DEFAULT nextval('auth_membership_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id_backup; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY backup ALTER COLUMN id_backup SET DEFAULT nextval('backup_id_backup_seq'::regclass);


--
-- Name: id_campo; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY campo ALTER COLUMN id_campo SET DEFAULT nextval('campo_id_campo_seq'::regclass);


--
-- Name: id_campo_cat; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY campo_catalogo ALTER COLUMN id_campo_cat SET DEFAULT nextval('campo_catalogo_id_campo_cat_seq'::regclass);


--
-- Name: id_catalogo; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY catalogo ALTER COLUMN id_catalogo SET DEFAULT nextval('catalogo_id_catalogo_seq'::regclass);


--
-- Name: id_comprobante; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY comprobante ALTER COLUMN id_comprobante SET DEFAULT nextval('comprobante_id_comprobante_seq'::regclass);


--
-- Name: id_jefe; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY jefe_dependencia ALTER COLUMN id_jefe SET DEFAULT nextval('jefe_dependencia_id_jefe_seq'::regclass);


--
-- Name: id_producto; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto ALTER COLUMN id_producto SET DEFAULT nextval('producto_id_producto_seq'::regclass);


--
-- Name: id_programa; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY programa ALTER COLUMN id_programa SET DEFAULT nextval('programa_id_programa_seq'::regclass);


--
-- Name: id_tipo; Type: DEFAULT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY tipo_actividad ALTER COLUMN id_tipo SET DEFAULT nextval('tipo_actividad_id_tipo_seq'::regclass);


--
-- Data for Name: act_posee_campo; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY act_posee_campo (id_tipo_act, id_campo) FROM stdin;
\.


--
-- Data for Name: auth_cas; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY auth_cas (id, user_id, created_on, service, ticket, renew) FROM stdin;
\.


--
-- Name: auth_cas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('auth_cas_id_seq', 1, false);


--
-- Data for Name: auth_event; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY auth_event (id, time_stamp, client_ip, user_id, origin, description) FROM stdin;
\.


--
-- Name: auth_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('auth_event_id_seq', 1, false);


--
-- Data for Name: auth_membership; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY auth_membership (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('auth_membership_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY auth_permission (id, group_id, name, table_name, record_id) FROM stdin;
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('auth_permission_id_seq', 1, false);


--
-- Data for Name: backup; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY backup (id_backup, descripcion, fecha) FROM stdin;
11	fassdsa	2016-11-09
12	asa	2016-11-09
13	aassd	2016-11-09
14	asad	2016-11-09
15	sasa	2016-11-09
16	sdcdass	2016-11-09
17	asdsadas	2016-11-09
18	dadadaad	2016-11-09
19	dsssd	2016-11-09
20	holk	2016-11-10
\.


--
-- Name: backup_id_backup_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('backup_id_backup_seq', 20, true);


--
-- Data for Name: campo; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY campo (id_campo, id_catalogo, nombre, tipo_campo, obligatorio) FROM stdin;
\.


--
-- Data for Name: campo_catalogo; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY campo_catalogo (id_campo_cat, id_catalogo, nombre, tipo_campo, obligatorio) FROM stdin;
\.


--
-- Name: campo_catalogo_id_campo_cat_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('campo_catalogo_id_campo_cat_seq', 1, false);


--
-- Name: campo_id_campo_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('campo_id_campo_seq', 1, false);


--
-- Data for Name: catalogo; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY catalogo (id_catalogo, nro_campos, nombre) FROM stdin;
\.


--
-- Name: catalogo_id_catalogo_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('catalogo_id_catalogo_seq', 1, false);


--
-- Data for Name: comprobante; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY comprobante (id_comprobante, archivo, descripcion, producto) FROM stdin;
\.


--
-- Name: comprobante_id_comprobante_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('comprobante_id_comprobante_seq', 1, false);


--
-- Data for Name: gestiona_catalogo; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY gestiona_catalogo (id_jefe, id_catalogo) FROM stdin;
\.


--
-- Data for Name: gestiona_tipo_act; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY gestiona_tipo_act (id_jefe, id_tipo_act) FROM stdin;
\.


--
-- Data for Name: jefe_dependencia; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY jefe_dependencia (id_jefe, usbid_usuario) FROM stdin;
\.


--
-- Name: jefe_dependencia_id_jefe_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('jefe_dependencia_id_jefe_seq', 1, false);


--
-- Data for Name: log_siradex; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY log_siradex (accion, accion_fecha, accion_ip, descripcion, usbid_usuario) FROM stdin;
\.


--
-- Data for Name: participa_producto; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY participa_producto (usbid_usuario, id_producto) FROM stdin;
\.


--
-- Data for Name: permisos_tipo_act; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY permisos_tipo_act (permiso, id_tipo) FROM stdin;
\.


--
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY producto (id_producto, id_tipo, nombre, descripcion, estado, evaluacion_criterio, evaluacion_valor, fecha_realizacion, fecha_modificacion, lugar, usbid_usu_modificador, usbid_usu_creador) FROM stdin;
\.


--
-- Name: producto_id_producto_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('producto_id_producto_seq', 1, false);


--
-- Data for Name: producto_tiene_campo; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY producto_tiene_campo (id_prod, id_campo, valor_campo) FROM stdin;
\.


--
-- Data for Name: programa; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY programa (id_programa, nombre, abreviacion, descripcion, papelera, modif_fecha, usbid_usu_modificador) FROM stdin;
\.


--
-- Name: programa_id_programa_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('programa_id_programa_seq', 1, false);


--
-- Data for Name: tipo_actividad; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY tipo_actividad (id_tipo, nombre, tipo_p_r, descripcion, id_programa, validacion, producto, nro_campos, id_jefe_creador, usbid_usuario_propone, papelera, modif_fecha) FROM stdin;
\.


--
-- Name: tipo_actividad_id_tipo_seq; Type: SEQUENCE SET; Schema: public; Owner: Siradex
--

SELECT pg_catalog.setval('tipo_actividad_id_tipo_seq', 1, false);


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: Siradex
--

COPY usuario (ci, usbid, nombres, apellidos, telefono, correo_inst, correo_alter, tipo) FROM stdin;
20975940	11-11020	Sergio Alejandro	Teran Zambrano	\N	11-11020@usb.ve	\N	Administrador
\.


--
-- Name: auth_cas_pkey; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_cas
    ADD CONSTRAINT auth_cas_pkey PRIMARY KEY (id);


--
-- Name: auth_event_pkey; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_event
    ADD CONSTRAINT auth_event_pkey PRIMARY KEY (id);


--
-- Name: auth_membership_pkey; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_membership
    ADD CONSTRAINT auth_membership_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: pk_act_posee_campo; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY act_posee_campo
    ADD CONSTRAINT pk_act_posee_campo PRIMARY KEY (id_tipo_act, id_campo);


--
-- Name: pk_backup; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY backup
    ADD CONSTRAINT pk_backup PRIMARY KEY (id_backup);


--
-- Name: pk_campo; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY campo
    ADD CONSTRAINT pk_campo PRIMARY KEY (id_campo);


--
-- Name: pk_campo_catalago; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY campo_catalogo
    ADD CONSTRAINT pk_campo_catalago PRIMARY KEY (id_campo_cat);


--
-- Name: pk_catalogo; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY catalogo
    ADD CONSTRAINT pk_catalogo PRIMARY KEY (id_catalogo);


--
-- Name: pk_comprobante; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY comprobante
    ADD CONSTRAINT pk_comprobante PRIMARY KEY (id_comprobante);


--
-- Name: pk_gestiona_catalogo; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY gestiona_catalogo
    ADD CONSTRAINT pk_gestiona_catalogo PRIMARY KEY (id_jefe, id_catalogo);


--
-- Name: pk_gestiona_tipo_act; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY gestiona_tipo_act
    ADD CONSTRAINT pk_gestiona_tipo_act PRIMARY KEY (id_jefe, id_tipo_act);


--
-- Name: pk_jefe_dependencia; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY jefe_dependencia
    ADD CONSTRAINT pk_jefe_dependencia PRIMARY KEY (id_jefe);


--
-- Name: pk_log; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY log_siradex
    ADD CONSTRAINT pk_log PRIMARY KEY (accion, accion_fecha, accion_ip);


--
-- Name: pk_participa_act; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY participa_producto
    ADD CONSTRAINT pk_participa_act PRIMARY KEY (usbid_usuario, id_producto);


--
-- Name: pk_permisos_tipo_act; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY permisos_tipo_act
    ADD CONSTRAINT pk_permisos_tipo_act PRIMARY KEY (permiso, id_tipo);


--
-- Name: pk_producto; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT pk_producto PRIMARY KEY (id_producto);


--
-- Name: pk_programa; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY programa
    ADD CONSTRAINT pk_programa PRIMARY KEY (id_programa);


--
-- Name: pk_tiene_campo; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto_tiene_campo
    ADD CONSTRAINT pk_tiene_campo PRIMARY KEY (id_prod, id_campo);


--
-- Name: pk_tipo_actividad; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY tipo_actividad
    ADD CONSTRAINT pk_tipo_actividad PRIMARY KEY (id_tipo);


--
-- Name: pk_usuario; Type: CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY usuario
    ADD CONSTRAINT pk_usuario PRIMARY KEY (usbid);


--
-- Name: fk_act_posee_campo_id_campo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY act_posee_campo
    ADD CONSTRAINT fk_act_posee_campo_id_campo FOREIGN KEY (id_campo) REFERENCES campo(id_campo);


--
-- Name: fk_act_posee_campo_id_tipo_act; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY act_posee_campo
    ADD CONSTRAINT fk_act_posee_campo_id_tipo_act FOREIGN KEY (id_tipo_act) REFERENCES tipo_actividad(id_tipo);


--
-- Name: fk_campo_catalogo_id_catalogo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY campo_catalogo
    ADD CONSTRAINT fk_campo_catalogo_id_catalogo FOREIGN KEY (id_catalogo) REFERENCES catalogo(id_catalogo);


--
-- Name: fk_campo_id_catalogo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY campo
    ADD CONSTRAINT fk_campo_id_catalogo FOREIGN KEY (id_catalogo) REFERENCES catalogo(id_catalogo);


--
-- Name: fk_gestiona_catalogo_id_catalogo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY gestiona_catalogo
    ADD CONSTRAINT fk_gestiona_catalogo_id_catalogo FOREIGN KEY (id_catalogo) REFERENCES catalogo(id_catalogo);


--
-- Name: fk_gestiona_catalogo_id_jefe; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY gestiona_catalogo
    ADD CONSTRAINT fk_gestiona_catalogo_id_jefe FOREIGN KEY (id_jefe) REFERENCES jefe_dependencia(id_jefe);


--
-- Name: fk_gestiona_tipo_act_id_jefe; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY gestiona_tipo_act
    ADD CONSTRAINT fk_gestiona_tipo_act_id_jefe FOREIGN KEY (id_jefe) REFERENCES jefe_dependencia(id_jefe);


--
-- Name: fk_gestiona_tipo_act_id_tipo_act; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY gestiona_tipo_act
    ADD CONSTRAINT fk_gestiona_tipo_act_id_tipo_act FOREIGN KEY (id_tipo_act) REFERENCES tipo_actividad(id_tipo);


--
-- Name: fk_jefe_dependencia_usbid_usuario; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY jefe_dependencia
    ADD CONSTRAINT fk_jefe_dependencia_usbid_usuario FOREIGN KEY (usbid_usuario) REFERENCES usuario(usbid);


--
-- Name: fk_log_usbid_usuario; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY log_siradex
    ADD CONSTRAINT fk_log_usbid_usuario FOREIGN KEY (usbid_usuario) REFERENCES usuario(usbid);


--
-- Name: fk_participa_act_id_producto; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY participa_producto
    ADD CONSTRAINT fk_participa_act_id_producto FOREIGN KEY (id_producto) REFERENCES producto(id_producto);


--
-- Name: fk_participa_act_usbid_usuario; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY participa_producto
    ADD CONSTRAINT fk_participa_act_usbid_usuario FOREIGN KEY (usbid_usuario) REFERENCES usuario(usbid);


--
-- Name: fk_permisos_tipo_act_id_tipo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY permisos_tipo_act
    ADD CONSTRAINT fk_permisos_tipo_act_id_tipo FOREIGN KEY (id_tipo) REFERENCES tipo_actividad(id_tipo);


--
-- Name: fk_producto_id_tipo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT fk_producto_id_tipo FOREIGN KEY (id_tipo) REFERENCES tipo_actividad(id_tipo);


--
-- Name: fk_producto_producto; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY comprobante
    ADD CONSTRAINT fk_producto_producto FOREIGN KEY (producto) REFERENCES producto(id_producto) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fk_producto_usbid_usu_creador; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT fk_producto_usbid_usu_creador FOREIGN KEY (usbid_usu_creador) REFERENCES usuario(usbid);


--
-- Name: fk_producto_usbid_usu_modificador; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT fk_producto_usbid_usu_modificador FOREIGN KEY (usbid_usu_modificador) REFERENCES usuario(usbid);


--
-- Name: fk_programa_usbid_usu_modificador; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY programa
    ADD CONSTRAINT fk_programa_usbid_usu_modificador FOREIGN KEY (usbid_usu_modificador) REFERENCES usuario(usbid);


--
-- Name: fk_tiene_campo_id_campo; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto_tiene_campo
    ADD CONSTRAINT fk_tiene_campo_id_campo FOREIGN KEY (id_campo) REFERENCES campo(id_campo);


--
-- Name: fk_tiene_campo_id_producto; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY producto_tiene_campo
    ADD CONSTRAINT fk_tiene_campo_id_producto FOREIGN KEY (id_prod) REFERENCES producto(id_producto);


--
-- Name: fk_tipo_actividad_id_jefe_creador; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY tipo_actividad
    ADD CONSTRAINT fk_tipo_actividad_id_jefe_creador FOREIGN KEY (id_jefe_creador) REFERENCES jefe_dependencia(id_jefe);


--
-- Name: fk_tipo_actividad_id_programa; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY tipo_actividad
    ADD CONSTRAINT fk_tipo_actividad_id_programa FOREIGN KEY (id_programa) REFERENCES programa(id_programa);


--
-- Name: fk_tipo_actividad_usbid_usuario_propone; Type: FK CONSTRAINT; Schema: public; Owner: Siradex
--

ALTER TABLE ONLY tipo_actividad
    ADD CONSTRAINT fk_tipo_actividad_usbid_usuario_propone FOREIGN KEY (usbid_usuario_propone) REFERENCES usuario(usbid);


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

