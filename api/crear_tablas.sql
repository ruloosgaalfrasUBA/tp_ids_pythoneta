USE IDS_API

create table hoteles
(    
    id_hotel bigint,
    nombre varchar,
    descripcion varchar,
    provincia varchar
);

create table reserva
(
    id_reserva bigint
    id_hotel bigint
);

create table detalle_reservas
(
    id_reserva bigint
    numero_reserva bigint
    nombre varchar
    apellido varchar
    dni bigint
    inicio_reserva date
    fin_reserva date
    activo boolean
);

create table reserva_servicio
(
    numero_reserva bigint
    id_servicio bigint 
);

create table servicio
(
    id_servicio bigint
    nombre varchar
    descripcion varchar
);