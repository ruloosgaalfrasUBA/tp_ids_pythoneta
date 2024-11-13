from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("mysql://root:capybara1@localhost:3306/bbdd_pythoneta")


def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters or {})
        conn.commit()
    return result

# Listado de servicios a utilizar:

# Buscar hoteles por estrellas, fechas, ubicación

# Hacer una Reserva
# Consultar Reserva
# Modificar Reserva
# Eliminar Reserva




#Servicios


#todos los servicios()
QUERY_TODOS_LOS_SERVICIOS = "SELECT * FROM servicio"

def obtener_todos_los_servicios():
    return run_query(QUERY_TODOS_LOS_SERVICIOS).fetchall()




QUERY_BUSCAR_SERVICIO_POR_ID = "SELECT * FROM servicio WHERE id_servicio = :id_servicio"

def buscar_servicio_por_id(id_servicio):
    return run_query(QUERY_BUSCAR_SERVICIO_POR_ID, {'id_servicio': id_servicio})




#obtener servicios por num de reserva (num reserva)
QUERY_BUSCAR_SERVICIOS_CONTRATADOS = "SELECT * FROM reserva_servicio WHERE numero_reserva = :numero_reserva"

def buscar_servicios_por_reserva(numero_reserva):
    return run_query(QUERY_BUSCAR_SERVICIOS_CONTRATADOS, {'numero_reserva': numero_reserva})




#cancelar servicio (num reserva, id servicio)
QUERY_CANCELAR_SERVICIO = "DELETE FROM reserva_servicio WHERE numero_reserva = :numero_reserva AND id_servicio = :id_servicio"

def cancelar_servicio(numero_reserva, id_servicio):
    return run_query(QUERY_CANCELAR_SERVICIO, {'numero_reserva': numero_reserva, "id_servicio": id_servicio})



#contratar servicio (num reserva, id servicio) insert into
QUERY_CONTRATAR_SERVICIO = "INSERT INTO reserva_servicio (numero_reserva, id_servicio) VALUES (:numero_reserva, :id_servicio)"

def contratar_servicio(numero_reserva, id_servicio):
    return run_query(QUERY_CONTRATAR_SERVICIO, {"numero_reserva": numero_reserva, "id_servicio": id_servicio})