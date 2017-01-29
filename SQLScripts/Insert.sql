/*Insercion de Programas*/

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Educación Permanente','EP','Encargada de los programas de formación no conducentes a grado académico, mediante cursos, diplomados, talleres, foros, seminarios y otras actividades complementarias de actualización, perfeccionamiento y capacitación para el trabajo productivo, dirigidos tanto a profesionales y técnicos como a la comunidad y al público en general.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Acción Social y Desarrollo Comunitario','SC','Actividad que deben desarrollar en las comunidades los estudiantes de educación superior, aplicando los conocimientos científicos, técnicos, culturales, deportivos y humanísticos adquiridos durante su formación académica, en beneficio de una comunidad.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Cooperación Técnica','CT','Unidad encargada de planificar, supervisar, asesorar y controlar el Programa de Pasantías Empresariales que ofrece a sus estudiantes la Universidad Simón Bolívar.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Fomento y proyección artística, cultural y deportiva','CD','Este programa tiene como objetivo impulsar la participacion de la comunidad universitaria en la organización de eventos recreacionales, en las actividades culturales y/o artisticas, en la organización de agrupaciones culturales, artisticas y deportivas en representación de la USB.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Divulgación y promoción del quehacer universitario','QU','Este programa tiene como objetivo promover la participación de la comunidad universitaria en comites y comisiones de carácter cientifico, humanistico, cultural, artistico, educativo o deportivo. Además de la publicación de articulos, libros o material audiovisual de divulgacion del quehacer universitario.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Igualdad de Oportunidades','IO','Este progarma tiene como objetivo brindar oportunidades para el ingreso a la USB a todos aquellos estudiantes cursantes del último año de la Educación Media Diversificadadel sector oficial, que rtengan dentro de sus aspiraciones vocacionales estudiar alguna carrera que ofrece la institucion.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Emprendimiento y seguimiento de Egresados','EGMLEMUE','Este programa tiene como objetivo contribuir a la formacion integral del estudiante y recien egresado, y apoyar el desarrollo de futuros líderes y empresarios competentes, creativos y emprendedores.','f');

/*Insercion de tipos de actividad*/

/*Tipos de actividad del programa 1*/

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-C1','Diseño de talleres y cursos de extensión','R','Diseño curricular del Programa del taller o curso(incluye talleres y cursos de Desarrollo Profesoral)','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-C2','Dictado de talleres y cursos de extensión finalizados, por cohorte','R','Listado final del curso con registro de asistencia o calificaciones (por cohorte).Incluye talleres y cursos de Desarrollo Profesoral.','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-P1','Diseño de Programas de cursos de extensión','R','Diseño curricular del programa','1','True');

/*Tipos de actividad del programa 2*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'SCR-P1','Formulación de proyectos del BPDEx de AS/DC','R','Proyecto del BPDEx de AS/DC','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'SCP-P2','Participación en la ejecución de proyectos del BPDEx de AS/DC','P','Informe parcial o final de ejecución del proyecto del BPDEx','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'SCP-P3','Responsable en la ejecución de proyectos del BPDEx de AS/DC','P','Informe parcial o final de ejecución del proyecto del BPDEx','2','True');

/*Tipos de actividad del programa 3*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CTP-P1','Responsable de proyecto de cooperación técnica (asesorías, consultorías, apoyo tecnológico, etc.)','P','Informe final de Proyecto','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CTP-P2','Participación en ejecución de proyectos de cooperación técnica (asesorías, consultorías, apoyo tecnológico, etc.)','P','Informe parcial de proyecto (por cada autor o co-autor).','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CTR-T1','Tutorías de pasantías cortas profesionales (6 semanas)','R','Informe de pasantía corta del estudiante y acta de evaluación','3','True');

/*Tipos de actividad del programa 4*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O1','Participación en la organización de eventos culturales y/o artísticos en representación de la USB','P','Informe de gestión de la organización','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-O1','Participación en la organización de eventos culturales y/o artísticos en representación de la USB','R','Validación o constancia impresa o electrónica de la Unidad organizadora del evento','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O2','Participación en la organización de eventos deportivos en representación de la USB','P','Informe de gestión de la organización','4','True');

/*Tipos de actividad del programa 5*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUP-D4','Publicación de libro de divulgación del quehacer universitario en medios impresos o digitales','P','Libro publicado','5','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D5','Presentación en conferencia, intervención en seminarios, foros y mesas de trabajo vinculados con la extensión universitaria','R','Trabajo, ponencia, poster, artículo','5','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D7','Trabajo editorial o de arbitraje de publicaciones, tanto internas en la USB como externas en representación de la USB','R','Informe de arbitraje o de evaluación','5','True');

/*Tipos de actividad del programa 6*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOP-A1','Diseño de programas de formación y nivelación académica preuniversitaria en representación de la USB','P','Diseño curricular de los programas','6','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A2','Responsable académico de la ejecución de programas de nivelación académica preuniversitaria en representación de la USB','R','Informe de gestión del programa','6','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A3','Diseño de cursos de nivelación académica preuniversitaria en representación de la USB','R','Diseño curricular de cursos','6','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A5','Organización de actividades de apoyo a programas y cursos de nivelación académica preuniversitaria en representación de la USB','R','del evento','6','True');

/*Tipos de actividad del programa 7*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'EGR-R1','Organización de actividades y eventos de apoyo al Seguimiento de los Egresados de la USB','P','Informe de gestión de la organización','7','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'EMR-P2','Participación en la creación e incubación de empresas desde la USB','P','Documento de registro mercantil de la empresa creada o en incubación','7','True');


/*INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'','','R','','1','True');*/

