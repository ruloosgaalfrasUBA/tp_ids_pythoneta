from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import db

QUERY_CREAR_RESERVA = """
INSERT INTO reserva (id_hotel) 
VALUES (:id_hotel)
;
"""

QUERY_CREAR_DETALLES_DE_RESERVA = """
INSERT INTO detalle_reservas (id_reserva,
                              nombre, 
                              apellido, 
                              dni, 
                              inicio_reserva, 
                              fin_reserva)
VALUES ((SELECT MAX(id_reserva) as id_reserva FROM reserva),
        :nombre, 
        :apellido, 
        :dni, 
        :inicio_reserva, 
        :fin_reserva)
;
"""

QUERY_CANCELAR_RESERVA = """
UPDATE detalle_reservas
SET activo = 0
WHERE numero_reserva = :numero_reserva
;
"""

QUERY_CONSULTAR_RESERVA = """
SELECT dr.nombre, 
       dr.apellido, 
       dr.numero_reserva,
       dr.dni,
       DATE_FORMAT(dr.inicio_reserva, '%Y-%m-%d'), 
       DATE_FORMAT(dr.fin_reserva, '%Y-%m-%d'),
       h.nombre, 
       h.provincia
FROM detalle_reservas dr
INNER JOIN reserva r ON dr.id_reserva = r.id_reserva
INNER JOIN hotel h ON r.id_hotel = h.id_hotel
WHERE dr.numero_reserva = :numero_reserva 
  AND dr.dni = :dni
  AND dr.activo = 1
;
"""

QUERY_MODIFICAR_RESERVA_INICIO = """
UPDATE detalle_reservas

"""
QUERY_MODIFICAR_RESERVA_FIN = """
WHERE numero_reserva = :numero_reserva
;
"""

def crear_reserva(id_hotel):
    db.run_query(QUERY_CREAR_RESERVA, {"id_hotel": id_hotel})

def crear_detalles_reserva(data):
    db.run_query(QUERY_CREAR_DETALLES_DE_RESERVA, data)

def cancelar_reserva(numero_reserva):
    db.run_query(QUERY_CANCELAR_RESERVA, {"numero_reserva": numero_reserva})

def consultar_reserva(numero_reserva, dni):
    datos = {"numero_reserva": numero_reserva, "dni": dni}
    return db.run_query(QUERY_CONSULTAR_RESERVA, datos).fetchall()

def modificar_reserva(numero_reserva, data):
    query = QUERY_MODIFICAR_RESERVA_INICIO
    query += "SET ".join([f"{key} = '{value}' \n" for key, value in data.items()])
    query += QUERY_MODIFICAR_RESERVA_FIN
    db.run_query(query,{"numero_reserva": numero_reserva})