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


@app.route('/servicios', methods=['GET'])
def obtener_servicios():
    try:
        result = hotel.all_servicios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    response = []
    for row in result:
        response.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2]})
    
    return jsonify(response), 200


@app.route('/servicios/contratar-servicio', methods=['POST'])
def agregar_servicio_a_reserva():
    data = request.get_json()

    keys = ('numero_reserva', 'id_servicio')
    for key in keys:
        if key not in data:
            return jsonify({'error': f'Falta el dato {key}'}), 400
        
    try:
        result = hotel.buscar_servicios_contratados_por_id(data['id'])
        if len(result)>0:
            return jsonify({'error': 'El servicio ya fue contratado anteriormente'}), 400
        
        hotel.contratar_servicio(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data), 201


@app.route('/servicios/cancelar-servicio', methods=['POST'])
def quitar_servicio_de_reserva():
    data = request.get_json()

    keys = ('numero_reserva', 'id_servicio')
    for key in keys:
        if key not in data:
            return jsonify({'error': f'Falta el dato {key}'}), 400
        
    try:
        result = hotel.buscar_servicios_contratados_por_id(data['id'])
        if len(result)==0:
            return jsonify({'error': 'El servicio no está contratado'}), 400
        
        hotel.cancelar_servicio(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data), 201


if __name__ == '__main__':
    app.run(debug=True)
