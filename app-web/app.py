from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_URL = 'http://localhost:5000/api/'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hoteles")
def hoteles():
    return render_template("hoteles.html")


@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    if request.method == "POST":
        #  Llamada a la api y cosas del back...
        error = "La reserva no existe. Verificar los datos ingresados."  # Para probar.
        if error:
            return render_template("reservas.html", error=error)

    return render_template("reservas.html")



@app.route("/todos-los-servicios")
def todos_los_servicios():
    try:
        response = requests.get(API_URL+'servicios')
        response.raise_for_status()
        servicios = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        servicios = []

    return render_template('pruebasServicio.html', servicios=servicios)

@app.route("/servicios-contratados/reserva:<numero_reserva>")
def servicios_contratados(numero_reserva):
    try:
        response = requests.get(API_URL+'servicos-por-reserva/'+numero_reserva)
        response.raise_for_status()
        servicios_contratados = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        servicios_contratados = []
    
    return render_template('pruebaServiciosContratados.html', servicios_contratados=servicios_contratados)
 

@app.route('/buscar-servicios', methods=['POST'])
def buscar_servicios():
    numero_reserva = request.form['buscar_servicios_reserva']
    return servicios_contratados(numero_reserva)


@app.route('/agregar-servicios', methods=['POST'])
def agregar_servicios():
    numero_reserva = request.form['numero_reserva']
    id_servicio = request.form['id_servicio']
    return contratar_servicio(numero_reserva, id_servicio)


@app.route("/cancelar-servicio/<numero_reserva>/<id_servicio>")
def cancelar_servicio(numero_reserva, id_servicio):

    try:
        response = requests.post(API_URL + 'servicios/cancelar-servicio/'+numero_reserva+'/'+id_servicio)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")

    return servicios_contratados(numero_reserva)


@app.route("/contratar-servicio/<numero_reserva>/<id_servicio>")
def contratar_servicio(numero_reserva, id_servicio):
    try:
        response = requests.post(API_URL+'servicios/contratar-servicio/'+numero_reserva+'/'+id_servicio)
        response.raise_for_status()
    except Exception as e:
        print(f"el error esta acaError: {e}")

    return servicios_contratados(numero_reserva)


if __name__ == "__main__":
    app.run(port="5001", debug=True)
