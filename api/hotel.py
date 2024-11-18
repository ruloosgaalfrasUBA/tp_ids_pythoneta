from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_SELECT_HOTELES = "SELECT * FROM hotel ORDER BY id_hotel"

QUERY_SELECT_HOTELES_ID = "SELECT * FROM hotel WHERE id_hotel = :id_hotel ORDER BY id_hotel "

QUERY_HOTELES_RESERVADOS = """
SELECT DISTINCT h.id_hotel FROM hotel h 
INNER JOIN reserva r ON r.id_hotel = h.id_hotel
INNER JOIN detalle_reserva dr ON dr.id_reserva = r.id_reserva
WHERE (dr.inicio_reserva < :inicio AND :inicio < dr.fin_reserva)
OR (:fin < dr.fin_reserva AND :fin > dr.inicio_reserva)
OR (dr.inicio_reserva BETWEEN :inicio AND :fin AND dr.fin_reserva BETWEEN '2023-01-13' AND '2023-01-18')

"""
QUERY_DISPONIBILIDAD ="""
    SELECT COUNT(*) 
    FROM hotel h 
    INNER JOIN reserva r ON r.id_hotel = h.id_hotel
    INNER JOIN detalle_reserva dr ON dr.id_reserva = r.id_reserva
    WHERE h.id_hotel = :hotel_id
      AND dr.activo = 1 
      AND (
        (dr.inicio_reserva < :inicio AND :inicio < dr.fin_reserva)
        OR (:fin < dr.fin_reserva AND :fin > dr.inicio_reserva)
        OR (dr.inicio_reserva BETWEEN :inicio AND :fin AND dr.fin_reserva BETWEEN :inicio AND :fin)
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

QUERY_CONTRATAR_SERVICIO = "INSERT INTO reserva_servicio (numero_reserva, id_servicio) VALUES (:numero_reserva, :id_servicio)"

QUERY_CANCELAR_SERVICIO = "DELETE FROM reserva_servicio WHERE numero_reserva = :numero_reserva AND id_servicio = :id_servicio"

QUERY_BUSCAR_SERVICIOS_CONTRATADOS = "SELECT * FROM reserva_servicio WHERE numero_reserva = :numero_reserva"

QUERY_BUSCAR_SERVICIO_POR_ID = "SELECT * FROM servicio WHERE id_servicio = :id_servicio"

QUERY_TODOS_LOS_SERVICIOS = "SELECT * FROM servicio"

engine = create_engine("mysql+mysqlconnector://root:1234@localhost:3306/bbdd_pythoneta")


def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

def all_hoteles():
    return run_query(QUERY_SELECT_HOTELES).fetchall()

def hoteles_fechas(id_hotel, inicio, fin):
    return run_query(QUERY_DISPONIBILIDAD, {'hotel_id': id_hotel,'inicio': inicio,'fin': fin}).fetchone()[0]



def hotel_by_id(id_hotel):
    return run_query(QUERY_SELECT_HOTELES_ID, {'id_hotel': id_hotel}).fetchall()

def hotel_reservado(inicio, fin):
    return run_query(QUERY_HOTELES_RESERVADOS, {'inicio': inicio, 'fin': fin}).fetchall()


def hoteles_estrellas(estrellas):
    return run_query(QUERY_SELECT_HOTEL_POR_ESTRELLAS, {'estrellas': estrellas}).fetchall()

def hoteles_provincia(provincia):
    return run_query(QUERY_SELECT_HOTEL_POR_UBICACION, {'provincia': provincia}).fetchall()

def obtener_todos_los_servicios():
    return run_query(QUERY_TODOS_LOS_SERVICIOS).fetchall()

def buscar_servicio_por_id(id_servicio):
    return run_query(QUERY_BUSCAR_SERVICIO_POR_ID, {'id_servicio': id_servicio})

def buscar_servicios_por_reserva(numero_reserva):
    return run_query(QUERY_BUSCAR_SERVICIOS_CONTRATADOS, {'numero_reserva': numero_reserva})

def cancelar_servicio(numero_reserva, id_servicio):
    return run_query(QUERY_CANCELAR_SERVICIO, {'numero_reserva': numero_reserva, "id_servicio": id_servicio})

def contratar_servicio(numero_reserva, id_servicio):
    return run_query(QUERY_CONTRATAR_SERVICIO, {"numero_reserva": numero_reserva, "id_servicio": id_servicio})
