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
            return render_template(
                "reservas.html", error="Complete los datos requeridos."
            )

        try:
            respuesta = requests.get(API_URI + f"/reservas/{nro_reserva}/{dni}")
            respuesta.raise_for_status()
            datos: dict | list[dict] = respuesta.json()

            if type(datos) == dict:
                error = datos.get("error")
                return render_template("reservas.html", error=error)

            for reserva in datos:
                return render_template("reservas.html", reserva=reserva)

        except requests.exceptions.RequestException:
            return render_template("reservas.html", error="Error interno.")

    return render_template("reservas.html")


@app.route("/modificar_reserva", methods=["POST"])
def modificar_reserva():
    # No se implementó la query todavía.
    id_reserva = request.form.get("id_reserva")
    fecha_inicio = request.form.get("fecha_inicio")
    fecha_fin = request.form.get("fecha_fin")

    if not id_reserva or not fecha_inicio or not fecha_fin:
        return render_template(
            "reservas.html", error="Error en los datos para modificar."
        )

    try:
        respuesta = requests.post(
            API_URI + f"/modificar_reserva/{id_reserva}",
            data={
                "id_reserva": id_reserva,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
            },
        )
        respuesta.raise_for_status()
        resultado: dict = respuesta.json()

        error = resultado.get("error")
        success = resultado.get("message")

        if error:
            return render_template("reservas.html", error=error)

        return render_template("reservas.html", success=success)

    except requests.exceptions.RequestException:
        return render_template("reservas.html", error="Error interno.")


@app.route("/cancelar_reserva", methods=["POST"])
def cancelar_reserva():
    id_reserva = request.form.get("id_reserva")

    if not id_reserva:
        return render_template(
            "reservas.html", error="Error en los datos para modificar."
        )

    try:
        respuesta = requests.post(
            API_URI + f"/cancelar_reserva/{id_reserva}",
            data={
                "id_reserva": id_reserva,
            },
        )
        respuesta.raise_for_status()
        resultado: dict = respuesta.json()

        error = resultado.get("error")
        success = resultado.get("message")

        if error:
            return render_template("reservas.html", error=error)

        return render_template("reservas.html", success=success)

    except requests.exceptions.RequestException as e:
        return render_template("reservas.html", error="Error interno.")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
