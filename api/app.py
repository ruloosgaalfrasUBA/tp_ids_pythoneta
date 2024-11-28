from flask import Flask, jsonify, request, render_template

import hotel
import reservas
import servicios

app = Flask(__name__)


################################################################################
# HOTELES                                                                      #
################################################################################


@app.route("/api/v1/hoteles", methods=["GET"])
def get_all_hoteles():
    try:
        result = hotel.all_hoteles()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    response = []
    for row in result:
        response.append({"id_hotel": row[0], "nombre": row[1], "descripcion": row[2], "provincia": row[3], "estrellas": row[4]})

    return jsonify(response), 200


@app.route("/api/v1/hoteles/inicio$<inicio>/fin$<fin>", methods=["GET"])
def get_all_hoteles_fecha_reserva(inicio, fin):
    try:
        indice = 0
        result = hotel.hotel_reservado(inicio, fin)
        hotel = hotel.all_hoteles()
        result = hotel.hotel_reservado(inicio, fin)
        hotel = hotel.all_hoteles()
        for i in hotel:
            for j in result:
                if j[0] == i[0]:
                    del hotel[indice]
            indice += 1
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    response = []
    for row in hotel:
        response.append({"id_hotel": row[0], "nombre": row[1], "descripcion": row[2], "provincia": row[3], "estrellas": row[4]})

    return jsonify(response), 200


@app.route("/api/v1/hoteles/<int:id_hotel>", methods=["GET"])
def get_by_id_hotel(id_hotel):
    try:
        result = hotel.hotel_by_id(id_hotel)
        result = hotel.hotel_by_id(id_hotel)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if len(result) == 0:
        return jsonify({"error": "No se encontró el hotel"}), 404  # Not found

    result = result[0]
    return jsonify({"id_hotel": result[0], "nombre": result[1], "descripcion": result[2], "provincia": result[3], "estrellas": result[4]}), 200


@app.route("/api/v1/hoteles/<provincia>", methods=["GET"])
def get_by_provincia(provincia):
    try:
        result = hotel.hoteles_provincia(provincia)
        result = hotel.hoteles_provincia(provincia)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    response = []
    for row in result:
        response.append({"id_hotel": row[0], "nombre": row[1], "descripcion": row[2], "provincia": row[3], "estrellas": row[4]})

    return jsonify(response), 200


@app.route("/api/v1/hoteles/estrellas:<int:estrellas>", methods=["GET"])
def get_by_estrellas(estrellas):
    try:
        result = hotel.hoteles_estrellas(estrellas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    response = []
    for row in result:
        response.append({"id_hotel": row[0], "nombre": row[1], "descripcion": row[2], "provincia": row[3], "estrellas": row[4]})

    return jsonify(response), 200


@app.route('/api/v1/disponibilidad', methods=['GET'])
def disponibilidad():
    from datetime import datetime
    
    id_hotel = request.args.get('id_hotel')
    inicio_reserva = request.args.get('inicio_reserva')
    fin_reserva = request.args.get('fin_reserva')
    print(id_hotel,inicio_reserva,fin_reserva)
    
    if not all([id_hotel, inicio_reserva, fin_reserva]):
        return jsonify({'error': 'Faltan parámetros en la solicitud'}), 400

    try:
        # Convertir las fechas
        inicio_reserva_date = datetime.strptime(inicio_reserva, '%Y-%m-%d').date()
        fin_reserva_date = datetime.strptime(fin_reserva, '%Y-%m-%d').date()

        # Verificar disponibilidad
        count = hotel.consultar_disponibilidad(id_hotel, inicio_reserva_date, fin_reserva_date)

        if count > 3:
            return jsonify({'disponibilidad': 'No hay lugar'}), 200
        else:
            return jsonify({'disponibilidad': 'Disponible'}), 200

    except Exception as e:
        print(f"Error al verificar disponibilidad: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


################################################################################
# SERVICIOS                                                                    #
################################################################################


@app.route('/api/v1/servicios', methods=['GET'])
def obtener_servicios():
    try:
        result = servicios.obtener_todos_los_servicios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2]})

    return jsonify(response), 200


@app.route('/api/v1/reservas/<id>/servicios', methods=['GET'])
def obtener_servicios_por_reserva(id):
    try:
        id = int(id)
        result = servicios.buscar_servicios_por_reserva(id)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        try:
            servicio = servicios.buscar_servicio_por_id(row[1])
            for s in servicio:
                response.append({'numero_reserva': row[0], 'id_servicio': row[1], 'nombre_servicio': s[1]})

        except Exception as e:
            print(f"Error al buscar servicio por ID: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify(response), 200


@app.route('/api/v1/reservas/<id>/servicios/<id_servicio>', methods=['DELETE'])
def quitar_servicio_de_reserva(id, id_servicio):
    try:
        servicios.cancelar_servicio(id, id_servicio)
        return jsonify({'message': 'Servicio cancelado exitosamente'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/reservas/<id>/servicios/<id_servicio>', methods=['POST'])
def agregar_servicio_a_reserva(id, id_servicio):
    try:
        servicios.contratar_servicio(id, id_servicio)
        return jsonify({'message': 'Servicio contratado exitosamente'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


################################################################################
# RESERVAS                                                                     #
################################################################################


@app.route('/api/v1/reservas', methods=['POST'])
def crear_reserva():
    keys = ("nombre", "apellido", "dni", "inicio_reserva", "fin_reserva", "id_hotel")
    try:
        data = request.get_json()
        for key in keys:
            if key not in data or not data[key]:
                return jsonify({'error': f'Falta el dato {key}'}), 400
        id_hotel = data.pop("id_hotel")
        reservas.crear_reserva(id_hotel)
        reservas.crear_detalles_reserva(data)
        return jsonify({'success': 'Reserva creada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/reservas/<id>', methods=['DELETE'])
def cancelar_reserva(id):
    try:
        reservas.cancelar_reserva(id)
        return jsonify({'message': 'Reserva cancelada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/reservas/<id>', methods=['GET'])
def consultar_reserva(id):
    try:
        result = reservas.consultar_reserva(id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    if len(result) == 0:
        return jsonify({'error': 'No se encontró la reserva'}), 404
    result = result[0]
    response = {
        "nombre": result[0],
        "apellido": result[1],
        "numero_reserva": result[2],
        "dni": result[3],
        "inicio_reserva": result[4],
        "fin_reserva": result[5],
        "nombre_hotel": result[6],
        "provincia": result[7],
    }
    return jsonify(response)


@app.route("/api/v1/reservas/<id>", methods=["PATCH"])
def modificar_reserva(id):
    try:
        data = request.form
        reservas.modificar_reserva(id, data)
        return jsonify({"message": "Reserva actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


################################################################################

if __name__ == "__main__":
    app.run(port="5001", debug=True)
