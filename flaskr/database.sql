create table if not exists usuarios(
	id				integer not null primary key autoincrement,
	usuario			varchar(128) unique not null,
	pwd				varchar(128),
	nombres			text,
	apellidos		text,
	email			varchar(128),
	creation_date	datetime
);
create table if not exists tratamientos(
	id					integer not null primary key autoincrement,
	nombre				varchar(256),
	descripcion			text,
	frecuencia			varchar(128),
	creation_date		datetime
);
create table if not exists pacientes(
	id				integer not null primary key autoincrement,
	codigo			varchar(128),
	historial		varchar(128),
	nombres			varchar(128),
	apellido_paterno	varchar(128),
	apellido_materno	varchar(128),
	documento			varchar(64) unique not null,
	sexo				varchar(64),
	fecha_nacimiento	date,
	direccion			text,
	telefono			varchar(64),
	creation_date		datetime
);
create table if not exists diagnosticos(
	id					integer not null primary key autoincrement,
	paciente_id			integer not null,
	tratamiento_id		integer not null,
	nivel				varchar(128),
	diagnostico			text,
	tratamiento			text,
	resultado			text,
	creation_date		datetime
);
