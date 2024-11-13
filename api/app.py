#from flask import Flask, render_template , request , redirect ,url_for
#from sqlalchemy import create_engine, text
#from sqlalchemy.orm import sessionmaker, scoped_session


from flask import Flask, jsonify, request, render_template

import hotel


#engine = create_engine("mysql://root:root@localhost:(puerto en el que esta la base de datos/nombre ")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/servicios', methods=['GET'])
def obtener_servicios():
    try:
        result = hotel.obtener_todos_los_servicios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    response = []
    for row in result:
        response.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2]})

    return jsonify(response), 200


@app.route('/api/servicos-por-reserva/<numero_reserva>', methods=['GET'])
def obtener_servicios_por_reserva(numero_reserva):
    try:
        numero_reserva = int(numero_reserva)
        result = hotel.buscar_servicios_por_reserva(numero_reserva)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
    response = []
    for row in result:
        try:
            servicio = hotel.buscar_servicio_por_id(row[1])
            for s in servicio:
                response.append({'numero_reserva': row[0], 'id_servicio': row[1], 'nombre_servicio': s[1]})
                
        except Exception as e:
            print(f"Error al buscar servicio por ID: {e}")
            return jsonify({'error': str(e)}), 500
        
    return jsonify(response), 200
        
@app.route('/api/servicios/cancelar-servicio/<numero_reserva>/<id_servicio>', methods=['POST'])
def quitar_servicio_de_reserva(numero_reserva, id_servicio):
    try:
        hotel.cancelar_servicio(numero_reserva, id_servicio)
        return jsonify({'message': 'Servicio cancelado exitosamente'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/servicios/contratar-servicio/<numero_reserva>/<id_servicio>', methods=['POST'])
def agregar_servicio_a_reserva(numero_reserva, id_servicio):
    try:
        hotel.contratar_servicio(numero_reserva, id_servicio)
        return jsonify({'message': 'Servicio contratado exitosamente'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port="5000", debug=True)
