--
-- PostgreSQL database dump
--

\restrict ZXyCzar92GctUFobG7mLq6qp6ITue6SCyUhk9QCyhvrvsCbl7nxA0g7TfTzih6f

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: tblproduk; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblproduk (
    id integer NOT NULL,
    nama character varying
);


ALTER TABLE public.tblproduk OWNER TO postgres;

--
-- Name: tblproduk_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblproduk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblproduk_id_seq OWNER TO postgres;

--
-- Name: tblproduk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblproduk_id_seq OWNED BY public.tblproduk.id;


--
-- Name: tblsupplier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblsupplier (
    id integer NOT NULL,
    nama character varying,
    email character varying,
    alamat text,
    pic character varying,
    kontak character varying(15)
);


ALTER TABLE public.tblsupplier OWNER TO postgres;

--
-- Name: tblsupplier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblsupplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblsupplier_id_seq OWNER TO postgres;

--
-- Name: tblsupplier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblsupplier_id_seq OWNED BY public.tblsupplier.id;


--
-- Name: tbltimbangan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbltimbangan (
    id bigint NOT NULL,
    tanggal date DEFAULT now(),
    waktu time without time zone DEFAULT now(),
    nama_wadah character varying,
    nama_produk character varying,
    berat_kotor numeric,
    berat_tare numeric,
    berat_nett numeric,
    operator character varying,
    supplier character varying,
    driver character varying,
    nopol character varying,
    id_transaksi character varying
);


ALTER TABLE public.tbltimbangan OWNER TO postgres;

--
-- Name: tbltimbangan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbltimbangan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbltimbangan_id_seq OWNER TO postgres;

--
-- Name: tbltimbangan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbltimbangan_id_seq OWNED BY public.tbltimbangan.id;


--
-- Name: tbluser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbluser (
    id integer NOT NULL,
    "user" character varying,
    role character varying,
    password character varying
);


ALTER TABLE public.tbluser OWNER TO postgres;

--
-- Name: tbluser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbluser_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbluser_id_seq OWNER TO postgres;

--
-- Name: tbluser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbluser_id_seq OWNED BY public.tbluser.id;


--
-- Name: tblwadah; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblwadah (
    id integer NOT NULL,
    nama character varying,
    berat numeric
);


ALTER TABLE public.tblwadah OWNER TO postgres;

--
-- Name: tblwadah_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblwadah_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblwadah_id_seq OWNER TO postgres;

--
-- Name: tblwadah_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblwadah_id_seq OWNED BY public.tblwadah.id;


--
-- Name: tblproduk id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblproduk ALTER COLUMN id SET DEFAULT nextval('public.tblproduk_id_seq'::regclass);


--
-- Name: tblsupplier id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblsupplier ALTER COLUMN id SET DEFAULT nextval('public.tblsupplier_id_seq'::regclass);


--
-- Name: tbltimbangan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltimbangan ALTER COLUMN id SET DEFAULT nextval('public.tbltimbangan_id_seq'::regclass);


--
-- Name: tbluser id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbluser ALTER COLUMN id SET DEFAULT nextval('public.tbluser_id_seq'::regclass);


--
-- Name: tblwadah id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblwadah ALTER COLUMN id SET DEFAULT nextval('public.tblwadah_id_seq'::regclass);


--
-- Data for Name: tblproduk; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblproduk (id, nama) FROM stdin;
1	Panci
2	Kaleng
3	Dinamo
6	Plat
\.


--
-- Data for Name: tblsupplier; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblsupplier (id, nama, email, alamat, pic, kontak) FROM stdin;
2	PT. Bintang Utama	bu@mail.co.id	Cikajang, Garut, Jawabarat	Aceng	085987654321
1	PT. Abadi Sejahtera	abadi.sejahtera@mail.co.id	Kawasan Industri ABC, Pasuruan, Jawa Tengah	Wawan	085123456789
4	CV. Andalan Anda	aab@mail.co.id	Cikalong, Tasikmalaya, Jawa Barat	Andi	085321654987
\.


--
-- Data for Name: tbltimbangan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbltimbangan (id, tanggal, waktu, nama_wadah, nama_produk, berat_kotor, berat_tare, berat_nett, operator, supplier, driver, nopol, id_transaksi) FROM stdin;
1	2025-11-18	13:24:13.029196	pallet	produk1	18.02	18.02	\N	\N	\N	\N	\N	\N
2	2025-11-20	18:54:35.66303	200	Panci	32.37	200	-167.63	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
3	2025-11-20	19:14:33.66012	2	Panci	9.59	2	7.59	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
4	2025-11-20	19:21:41.673643	200	Panci	43.16	200	-156.84	admin	-- Pilih Supplier --PT. Abadi SejahteraPT. Bintang UtamaCV. Andalan Anda	Endang	B 1234 XYZ	\N
5	2025-11-20	19:26:00.402676	200	Panci	55.46	200	-144.54	admin	-- Pilih Supplier --PT. Abadi SejahteraPT. Bintang UtamaCV. Andalan Anda	Endang	B 1234 XYZ	\N
6	2025-11-20	19:40:06.784525	200	Panci	22.99	200	-177.01	admin	PanciBox BesiPT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
7	2025-11-20	19:40:47.618998	200	Panci	48.7	200	-151.30	admin	PanciBox BesiPT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
8	2025-11-20	19:49:56.142871	200	Panci	22.49	200	-177.51	admin	PanciBox BesiPT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
9	2025-11-20	19:52:41.988413	200	Panci	45.21	200	-154.79	admin	PanciBox BesiPT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
10	2025-11-20	19:56:40.325377	200	Panci	75.09	200	-124.91	admin	PanciBox BesiPT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
11	2025-11-20	20:06:30.974784	200	Panci	39.77	200	-160.23	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
12	2025-11-20	20:21:06.059835	200	Panci	86.73	200	-113.27	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
13	2025-11-20	20:22:01.494399	200	Panci	77.1	200	-122.90	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
14	2025-11-20	20:22:04.801811	200	Panci	96.85	200	-103.15	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
15	2025-11-20	20:22:06.656748	200	Panci	15.09	200	-184.91	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
16	2025-11-20	20:22:08.335784	200	Panci	77.59	200	-122.41	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
17	2025-11-20	20:22:10.131532	200	Panci	70.43	200	-129.57	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
18	2025-11-20	20:22:12.24127	200	Panci	78.59	200	-121.41	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
19	2025-11-20	20:22:20.108326	200	Kaleng	79.17	200	-120.83	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
20	2025-11-20	20:22:22.367126	200	Kaleng	11.43	200	-188.57	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
21	2025-11-20	20:22:24.036338	200	Kaleng	79.99	200	-120.01	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
22	2025-11-20	20:22:25.912108	200	Kaleng	86.67	200	-113.33	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
23	2025-11-20	20:25:39.427469	200	Kaleng	24.88	200	-175.12	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
24	2025-11-20	20:31:27.297092	KalengBox BesiPT. Abadi Sejahtera	Kaleng	42.87	200	-157.13	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
25	2025-11-20	20:49:12.380435	Box Besi	Panci	54.1	200	-145.90	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
26	2025-11-20	20:50:46.8513	Box Besi	Panci	68.06	200	-131.94	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
27	2025-11-20	20:50:50.532044	Box Besi	Panci	93.75	200	-106.25	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
28	2025-11-20	20:50:53.569819	Box Besi	Panci	45.07	200	-154.93	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
29	2025-11-20	20:50:55.275273	Box Besi	Panci	65.63	200	-134.37	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
30	2025-11-20	20:50:56.662367	Box Besi	Panci	63.65	200	-136.35	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
31	2025-11-20	20:50:58.154945	Box Besi	Panci	10.79	200	-189.21	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
32	2025-11-20	20:50:59.6464	Box Besi	Panci	10.25	200	-189.75	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
33	2025-11-20	20:51:01.269462	Box Besi	Panci	57.58	200	-142.42	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
34	2025-11-20	20:51:02.679054	Box Besi	Panci	35.35	200	-164.65	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
35	2025-11-20	20:51:04.232602	Box Besi	Panci	15.05	200	-184.95	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
36	2025-11-20	20:51:05.877602	Box Besi	Panci	31.67	200	-168.33	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
37	2025-11-20	20:51:07.916545	Box Besi	Panci	63.95	200	-136.05	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
38	2025-11-20	20:52:41.976846	Pallet	Panci	91.32	10	81.32	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
39	2025-11-20	20:56:12.246224	Box Besi	Panci	79.39	200	-120.61	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
40	2025-11-20	20:56:21.558375	Pallet	Panci	98.11	10	88.11	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
41	2025-11-20	20:56:24.126715	Pallet	Panci	84.08	10	74.08	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
42	2025-11-20	20:56:24.590806	Pallet	Panci	84.08	10	74.08	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
43	2025-11-20	20:56:25.072159	Pallet	Panci	86.33	10	76.33	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
44	2025-11-20	20:56:26.347592	Pallet	Panci	25.73	10	15.73	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
45	2025-11-20	20:56:28.040171	Pallet	Panci	47.77	10	37.77	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
48	2025-11-20	21:12:53.718145	-- Pilih Wadah --	\N	24.42	0.00	24.42	admin	\N			\N
49	2025-11-20	21:37:01.830181	Pallet	Panci	24.65	10	14.65	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
52	2025-11-20	21:46:01.609138	Box Besi	Panci	51.64	200	-148.36	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
53	2025-11-21	06:44:38.335637	Box Besi	Panci	38.26	200	-161.74	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
81	2025-11-22	11:20:19.749472	Jumbo Bag	Panci	89.26	2	87.26	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
82	2025-11-22	11:20:21.812831	Jumbo Bag	Panci	69.74	2	67.74	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
83	2025-11-22	11:20:23.074648	Jumbo Bag	Panci	35.67	2	33.67	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
84	2025-11-22	11:20:24.369698	Jumbo Bag	Panci	18.08	2	16.08	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
85	2025-11-22	11:20:25.068787	Jumbo Bag	Panci	18.08	2	16.08	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
86	2025-11-22	11:20:25.714	Jumbo Bag	Panci	23.33	2	21.33	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
87	2025-11-22	11:20:26.361392	Jumbo Bag	Panci	60.26	2	58.26	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
88	2025-11-22	11:20:27.099471	Jumbo Bag	Panci	60.26	2	58.26	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
89	2025-11-22	11:20:28.039203	Jumbo Bag	Panci	66.61	2	64.61	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
90	2025-11-22	11:31:21.057674	Jumbo Bag	Panci	8.35	2	6.35	admin	PT. Abadi Sejahtera	Endang	B 1234 XYZ	\N
\.


--
-- Data for Name: tbluser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbluser (id, "user", role, password) FROM stdin;
2	admin	admin	21232f297a57a5a743894a0e4a801fc3
3	Indra	operator	827ccb0eea8a706c4c34a16891f84e7b
\.


--
-- Data for Name: tblwadah; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblwadah (id, nama, berat) FROM stdin;
4	Pallet	10
6	Box Besi	200
3	Jumbo Bag	5
\.


--
-- Name: tblproduk_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblproduk_id_seq', 6, true);


--
-- Name: tblsupplier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblsupplier_id_seq', 4, true);


--
-- Name: tbltimbangan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbltimbangan_id_seq', 90, true);


--
-- Name: tbluser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbluser_id_seq', 6, true);


--
-- Name: tblwadah_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblwadah_id_seq', 11, true);


--
-- Name: tblproduk tblproduk_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblproduk
    ADD CONSTRAINT tblproduk_pkey PRIMARY KEY (id);


--
-- Name: tblsupplier tblsupplier_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblsupplier
    ADD CONSTRAINT tblsupplier_pkey PRIMARY KEY (id);


--
-- Name: tbltimbangan tbltimbangan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltimbangan
    ADD CONSTRAINT tbltimbangan_pkey PRIMARY KEY (id);


--
-- Name: tbluser tbluser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbluser
    ADD CONSTRAINT tbluser_pkey PRIMARY KEY (id);


--
-- Name: tblwadah tblwadah_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblwadah
    ADD CONSTRAINT tblwadah_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict ZXyCzar92GctUFobG7mLq6qp6ITue6SCyUhk9QCyhvrvsCbl7nxA0g7TfTzih6f

