from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import db

QUERY_CONTRATAR_SERVICIO = "INSERT INTO reserva_servicio (numero_reserva, id_servicio) VALUES (:numero_reserva, :id_servicio)"

QUERY_CANCELAR_SERVICIO = "DELETE FROM reserva_servicio WHERE numero_reserva = :numero_reserva AND id_servicio = :id_servicio"

QUERY_BUSCAR_SERVICIOS_CONTRATADOS = "SELECT * FROM reserva_servicio WHERE numero_reserva = :numero_reserva"

QUERY_BUSCAR_SERVICIO_POR_ID = "SELECT * FROM servicio WHERE id_servicio = :id_servicio"

QUERY_TODOS_LOS_SERVICIOS = "SELECT * FROM servicio"

def obtener_todos_los_servicios():
    return db.run_query(QUERY_TODOS_LOS_SERVICIOS).fetchall()

def buscar_servicio_por_id(id_servicio):
    return db.run_query(QUERY_BUSCAR_SERVICIO_POR_ID, {'id_servicio': id_servicio})

def buscar_servicios_por_reserva(numero_reserva):
    return db.run_query(QUERY_BUSCAR_SERVICIOS_CONTRATADOS, {'numero_reserva': numero_reserva})

def cancelar_servicio(numero_reserva, id_servicio):
    return db.run_query(QUERY_CANCELAR_SERVICIO, {'numero_reserva': numero_reserva, "id_servicio": id_servicio})

def contratar_servicio(numero_reserva, id_servicio):
    return db.run_query(QUERY_CONTRATAR_SERVICIO, {"numero_reserva": numero_reserva, "id_servicio": id_servicio})
