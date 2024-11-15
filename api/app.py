from flask import Flask, jsonify, request
import json
import hoteles

app = Flask(__name__)

@app.route('/api/v1/hoteles', methods=['GET'])
def get_all_hoteles():
    try:
        result = hoteles.all_hoteles()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'id_hotel': row[0], 'nombre': row[1], 'descripcion': row[2], 'provincia': row[3], 'estrellas':row[4]})

    return jsonify(response), 200

@app.route('/api/v1/hoteles/inicio$<inicio>/fin$<fin>', methods=['GET'])
def get_all_hoteles_fecha_reserva(inicio, fin):
    try:
        indice = 0
        result = hoteles.hotel_reservado(inicio, fin)
        hotel = hoteles.all_hoteles()
        for i in hotel:
            for j in result:
                if j[0] == i[0]:
                    del hotel[indice]
            indice += 1
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in hotel:
        response.append({'id_hotel': row[0], 'nombre': row[1], 'descripcion': row[2], 'provincia': row[3], 'estrellas': row[4]})


    return jsonify(response), 200

@app.route('/api/v1/hoteles/<int:id_hotel>', methods=['GET'])
def get_by_id_hotel(id_hotel):
    try:
        result = hoteles.hotel_by_id(id_hotel)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if len(result) == 0:
        return jsonify({'error': 'No se encontró el hotel'}), 404 # Not found

    result = result[0]
    return jsonify({'id_hotel': result[0], 'nombre': result[1], 'descripcion': result[2], 'provincia': result[3], 'estrellas': result[4]}), 200

@app.route('/api/v1/hoteles/<provincia>', methods=['GET'])
def get_by_provincia(provincia):
    try:
        result = hoteles.hoteles_provincia(provincia)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'id_hotel': row[0], 'nombre': row[1], 'descripcion': row[2], 'provincia': row[3], 'estrellas':row[4]})

    return jsonify(response), 200

@app.route('/api/v1/hoteles/estrellas:<int:estrellas>', methods=['GET'])
def get_by_estrellas(estrellas):
    try:
        result = hoteles.hoteles_estrellas(estrellas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'id_hotel': row[0], 'nombre': row[1], 'descripcion': row[2], 'provincia': row[3], 'estrellas':row[4]})

    return jsonify(response), 200

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)