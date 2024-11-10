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



if __name__ == "__main__":
    app.run(port="5001", debug=True)
