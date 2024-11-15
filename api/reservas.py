from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_CREAR_RESERVA = """
INSERT INTO reserva (id_hotel) 
VALUES (:id_hotel)
;
"""

QUERY_CREAR_DETALLES_DE_RESERVA = """
INSERT INTO detalle_reservas (numero_reserva, nombre, apellido, dni, inicio_reserva, fin_reserva)
VALUES (:numero_reserva, :nombre, :apellido, :dni, :inicio_reserva, :fin_reserva)
;
"""

QUERY_CANCELAR_RESERVA = """
UPDATE detalle_reservas
SET activo = 0
WHERE id_reserva = :id_reserva
"""

QUERY_CONSULTAR_RESERVA = """
SELECT dr.nombre, dr.apellido, dr.numero_reserva, dr.inicio_reserva, dr.fin_reserva,
       h.nombre, h.provincia
FROM detalle_reservas dr
INNER JOIN reserva r ON dr.id_reserva = r.id_reserva
INNER JOIN hoteles h ON r.id_hotel = h.id_hotel
WHERE dr.numero_reserva = :numero_reserva AND dr.dni = :dni
;
"""

QUERY_MODIFICAR_RESERVA_INICIO = """
UPDATE detalle_reservas

"""
QUERY_MODIFICAR_RESERVA_FIN = """
WHERE id_reserva = :id_reserva
;
"""


engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/hoteles")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

def crear_reserva(numero_reserva, nombre, apellido, dni, inicio_reserva, fin_reserva, id_hotel): 
    reserva = {
        "numero_reserva": numero_reserva,
        "id_hotel": id_hotel,
    }  
    detalles = {
        "numero_reserva": numero_reserva,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "inicio_reserva": inicio_reserva,
        "fin_reserva": fin_reserva,
    }
    run_query(QUERY_CREAR_RESERVA, reserva)    
    run_query(QUERY_CREAR_DETALLES_DE_RESERVA, detalles)

def cancelar_reserva(id_reserva):
    reserva = {
        "id_reserva": id_reserva,
    }
    run_query(QUERY_CANCELAR_RESERVA, reserva)

def consultar_reserva(numero_reserva, dni):
    reserva = {
        "numero_reserva": numero_reserva,
        "dni": dni
    }
    return run_query(QUERY_CONSULTAR_RESERVA, reserva).fetch_all()

def modificar_reserva(id_reserva, data):
    query = QUERY_MODIFICAR_RESERVA_INICIO
    query += "SET ".join([f"{key} = '{value}' \n" for key, value in data.items()])
    query += QUERY_MODIFICAR_RESERVA_FIN
    run_query(query,{"id_reserva": id_reserva})