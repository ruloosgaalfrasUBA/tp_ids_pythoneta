-- Active: 1731177583885@@127.0.0.1@3306

CREATE DATABASE bbdd_pythoneta
    DEFAULT CHARACTER SET utf8;

USE bbdd_pythoneta;

CREATE TABLE bbdd_pythoneta.hoteles (    
    id_hotel BIGINT UNIQUE AUTO_INCREMENT,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    provincia VARCHAR(255)
    PRIMARY KEY(id_hotel)
);

CREATE TABLE bbdd_pythoneta.reserva (
    id_reserva BIGINT,
    id_hotel BIGINT
    CONSTRAINT PK_reserva PRIMARY KEY (id_reserva, id_hotel)
);

CREATE TABLE bbdd_pythoneta.detalle_reservas (
    id_reserva BIGINT AUTO_INCREMENT,
    numero_reserva BIGINT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    dni BIGINT,
    inicio_reserva DATE,
    fin_reserva DATE,
    activo BOOLEAN DEFAULT TRUE
    PRIMARY KEY (id_reserva)
);

CREATE TABLE bbdd_pythoneta.reserva_servicio (
    numero_reserva BIGINT,
    id_servicio BIGINT 
    CONSTRAINT PK_reserva_servicio PRIMARY KEY (numero_reserva, id_servicio)
);

CREATE TABLE bbdd_pythoneta.servicio (
    id_servicio BIGINT AUTO_INCREMENT,
    nombre VARCHAR(255),
    descripcion VARCHAR(255)
    PRIMARY KEY (id_servicio)
);