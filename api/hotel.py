from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("mysql://root:root@localhost:(puerto en el que esta la base de datos/nombre ")


QUERY_TODOS_LOS_SERVICIOS = "SELECT * FROM servicio"

QUERY_BUSCAR_SERVICIOS_CONTRATADOS_POR_ID = "SELECT * FROM alumnos WHERE id = :id"

QUERY_CONTRATAR_SERVICIO = "INSERT INTO reserva_servicio (numero_reserva, id_servicio) VALUES (:numero_reserva, :id_servicio)"

QUERY_CANCELAR_SERVICIO = "DELETE FROM reserva_servicio WHERE numero_reserva = :numero_reserva AND id_servicio = :id_servicio"


def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

# Listado de servicios a utilizar:

# Buscar hoteles por estrellas, fechas, ubicación

# Hacer una Reserva
# Consultar Reserva
# Modificar Reserva
# Eliminar Reserva




# Listar Servicios
def all_servicios():
    return run_query(QUERY_TODOS_LOS_SERVICIOS).fetchall()

# Buscar servicio contratado por ID
def buscar_servicios_contratados_por_id(id):
    return run_query(QUERY_BUSCAR_SERVICIOS_CONTRATADOS_POR_ID, {'id': id}).fetchall()

# Contratar Servicio
def contratar_servicio(numero_reserva, id_servicio):
    return run_query(QUERY_CONTRATAR_SERVICIO), {"numero_reserva":numero_reserva, "id_servicio": id_servicio}

# Cancelar Servicio
def cancelar_servicio(numero_reserva, id_servicio):
    return run_query(QUERY_CANCELAR_SERVICIO), {'numero_reserva': numero_reserva, "id_servicio": id_servicio}