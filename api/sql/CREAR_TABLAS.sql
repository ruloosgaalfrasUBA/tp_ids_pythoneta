CREATE DATABASE bbdd_pythoneta
    DEFAULT CHARACTER SET utf8;

USE bbdd_pythoneta;

CREATE TABLE bbdd_pythoneta.hoteles (    
    id_hotel BIGINT UNIQUE AUTO_INCREMENT,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    provincia VARCHAR(255),
    estrellas BIGINT,
    PRIMARY KEY(id_hotel)
);

CREATE TABLE bbdd_pythoneta.reserva (
    id_reserva BIGINT AUTO_INCREMENT,
    id_hotel BIGINT,
    CONSTRAINT PK_reserva PRIMARY KEY (id_reserva, id_hotel)
);

CREATE TABLE bbdd_pythoneta.detalle_reservas (
    id_reserva BIGINT,
    numero_reserva BIGINT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    dni BIGINT,
    inicio_reserva DATE,
    fin_reserva DATE,
    activo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_reserva) REFERENCES bbdd_pythoneta.reserva(id_reserva)
    );

CREATE TABLE bbdd_pythoneta.reserva_servicio (
    numero_reserva BIGINT,
    id_servicio BIGINT,
    CONSTRAINT PK_reserva_servicio PRIMARY KEY (numero_reserva, id_servicio)
);

CREATE TABLE bbdd_pythoneta.servicio (
    id_servicio BIGINT AUTO_INCREMENT,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    PRIMARY KEY (id_servicio)
);