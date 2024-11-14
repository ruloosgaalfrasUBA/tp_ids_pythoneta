from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_CREAR_RESERVA = """
INSERT INTO reserva (numero_reserva, id_hotel) 
VALUES (:numero_reserva, :id_hotel)
;
"""

QUERY_CREAR_DETALLES_DE_RESERVA = """
INSERT INTO detalle_reservas (numero_reserva, nombre, apellido, dni, inicio_reserva, fin_reserva)
VALUES (:numero_reserva, :nombre, :apellido, :dni, :inicio_reserva, :fin_reserva)
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
