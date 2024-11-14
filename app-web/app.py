from flask import Flask, render_template, request

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
