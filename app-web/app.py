from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_URI = "http://localhost:5001/api/v1"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hoteles")
def hoteles():
    return render_template("hoteles.html")


@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    if request.method == "POST":
        nro_reserva = request.form.get("numero_reserva")
        dni = request.form.get("dni")

        if not nro_reserva or not dni:
            return render_template("reservas.html", error="Complete los datos requeridos.")

        try:
            respuesta = requests.get(API_URI + f"/reservas/{nro_reserva}")
            respuesta.raise_for_status()
            datos = respuesta.json()

            for reserva in datos:
                error = reserva.get("error")
                if error:
                    return render_template("reservas.html", error=error)
                return render_template("reservas.html", reserva=reserva)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            datos = []

    return render_template("reservas.html")

@app.route("/modificar_reserva", methods=["POST"])
def modificar_reserva():
    reserva = request.form.to_dict()
    return render_template('reservas.html', error="La reserva se modificó")

@app.route("/cancelar_reserva", methods=["POST"])
def cancelar_reserva():
    reserva = request.form.to_dict()
    return render_template('reservas.html', error="La reserva se canceló")


if __name__ == "__main__":
    app.run(debug=True)
