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
        print(nro_reserva)
        try:
            response = requests.get(API_URI + f"/reservas/{nro_reserva}")
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            data = []

    return render_template("reservas.html")


if __name__ == "__main__":
    app.run(debug=True)
