from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import db

QUERY_SELECT_HOTELES = "SELECT * FROM hotel ORDER BY id_hotel"

QUERY_SELECT_HOTELES_ID = "SELECT * FROM hotel WHERE id_hotel = :id_hotel ORDER BY id_hotel "

QUERY_HOTELES_RESERVADOS = """
SELECT DISTINCT h.id_hotel FROM hotel h 
INNER JOIN reserva r ON r.id_hotel = h.id_hotel
INNER JOIN detalle_reservas dr ON dr.id_reserva = r.id_reserva
WHERE (dr.inicio_reserva < :inicio AND :inicio < dr.fin_reserva)
OR (:fin < dr.fin_reserva AND :fin > dr.inicio_reserva)
OR (dr.inicio_reserva BETWEEN :inicio AND :fin AND dr.fin_reserva BETWEEN '2023-01-13' AND '2023-01-18')

"""
QUERY_DISPONIBILIDAD = """
    SELECT COUNT(*) as count
    FROM hotel h 
    INNER JOIN reserva r ON r.id_hotel = h.id_hotel
    INNER JOIN detalle_reservas dr ON dr.id_reserva = r.id_reserva
    WHERE h.id_hotel = :id_hotel
      AND dr.activo = 1 
      AND (
        (dr.inicio_reserva < :inicio_reserva AND :inicio_reserva < dr.fin_reserva)
        OR (:fin_reserva < dr.fin_reserva AND :fin_reserva > dr.inicio_reserva)
        OR (dr.inicio_reserva BETWEEN :inicio_reserva AND :fin_reserva 
            AND dr.fin_reserva BETWEEN :inicio_reserva AND :fin_reserva)
      );
"""


QUERY_CONSULTA_RESERVA_POR_ID = """
SELECT h.id_hotel, r.id_reserva, dr.id_numero_reserva, dr.nombre 
FROM hotel h 
INNER JOIN reserva r ON h.id_hotel = r.id_hotel 
INNER JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva 
WHERE dr.id_numero_reserva = :numero_reserva
"""

QUERY_CANCELAR_RESERVA = """
UPDATE detalle_reserva 
SET activo = 0 
WHERE id_numero_reserva = :numero_reserva
"""

QUERY_SELECT_POR_ID_RESERVA = """
SELECT nombre, apellido, dni, inicio_reserva, fin_reserva
FROM detalle_reserva
WHERE id_numero_reserva = :numero_reserva
"""

QUERY_SELECT_HOTEL_POR_ESTRELLAS = """
SELECT *
FROM hotel h
WHERE h.estrellas = :estrellas
"""

QUERY_SELECT_HOTEL_POR_UBICACION = """
SELECT * 
FROM hotel h
WHERE h.provincia = :provincia
"""


def all_hoteles():
    return db.run_query(QUERY_SELECT_HOTELES).fetchall()


def hotel_by_id(id_hotel):
    return db.run_query(QUERY_SELECT_HOTELES_ID, {'id_hotel': id_hotel}).fetchall()

def hotel_reservado(inicio, fin):
    return db.run_query(QUERY_HOTELES_RESERVADOS, {'inicio': inicio, 'fin': fin}).fetchall()

def hoteles_estrellas(estrellas):
    return db.run_query(QUERY_SELECT_HOTEL_POR_ESTRELLAS, {'estrellas': estrellas}).fetchall()

def hoteles_provincia(provincia):
    return db.run_query(QUERY_SELECT_HOTEL_POR_UBICACION, {'provincia': provincia}).fetchall()
def consultar_disponibilidad(id_hotel, inicio_reserva, fin_reserva):
    result = db.run_query(
        QUERY_DISPONIBILIDAD, 
        {'id_hotel': id_hotel, 'inicio_reserva': inicio_reserva, 'fin_reserva': fin_reserva}
    ).fetchone()
    
  
    return result['count'] if result and 'count' in result else 0

