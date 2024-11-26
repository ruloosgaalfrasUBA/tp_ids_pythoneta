from flask import Flask, render_template, request ,redirect ,url_for
import requests

app = Flask(__name__)


API_URI = "http://localhost:5001/api/v1"

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        response = requests.get(API_URI + '/hoteles')
        response.raise_for_status()
        hoteles = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener información de hoteles: {e}")
        hoteles = []
        return render_template("index.html", hoteles=hoteles, error="No se pudieron cargar los hoteles.")

    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        dni = request.form.get("dni")
        inicio_reserva = request.form.get("inicio_reserva")
        fin_reserva = request.form.get("fin_reserva")
        id_hotel = request.form.get("id_hotel")
       # print(nombre,apellido,dni,inicio_reserva,fin_reserva,id_hotel)

        if not nombre or not apellido or not dni or not inicio_reserva or not fin_reserva or not id_hotel:
            return render_template("index.html", hoteles=hoteles, error="Complete todos los campos del formulario.")

        try:
          
           # response = requests.get( API_URI + f"/disponibilidad?id_hotel={id_hotel}&inicio={inicio_reserva}&fin={fin_reserva}")
            #response.raise_for_status()
           # data = response.json()

            #if not data['disponibilidad']:
               # return render_template("index.html", hoteles=hoteles, error="No hay disponibilidad en el hotel para las fechas seleccionadas.")

            data = {
                "nombre": nombre,
                "apellido": apellido,
                "dni": dni,
                "inicio_reserva": inicio_reserva,
                "fin_reserva": fin_reserva,
                "id_hotel": id_hotel
            }
            respuesta = requests.post(API_URI + f"/reservas/crear-reserva", json=data)
            respuesta.raise_for_status()
            resultdo: dict = respuesta.json()

            error =resultdo.get("error")
            success =resultdo.get("message")

            return render_template("index.html", hoteles=hoteles, success="Reserva creada exitosamente")

        except requests.exceptions.RequestException as e:
            return render_template("index.html", hoteles=hoteles, error=f"Error al crear la reserva: {e}")

    return render_template("index.html", hoteles=hoteles)


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
            respuesta = requests.get(API_URI + f"/reservas/consultar-reserva/{nro_reserva}/{dni}")
            datos: dict | list[dict] = respuesta.json()

            error = datos.get("error")
            if error:
                return render_template("reservas.html", error=error)

            return render_template("reservas.html", reserva=datos)

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
        return render_template("reservas.html", error="Error en los datos para modificar.")

    try:
        respuesta = requests.post(
            API_URI + f"/reservas/modificar_reserva/{id_reserva}",
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
    numero_reserva = request.form.get("numero_reserva")
    if not numero_reserva:
        return render_template("reservas.html", error="Error en los datos para modificar.")

    try:
        respuesta = requests.post(
            API_URI + f"/reservas/cancelar-reserva/{numero_reserva}",
            data={
                "numero_reserva": numero_reserva,
            },
        )
        resultado: dict = respuesta.json()


        error = resultado.get("error")
        success = resultado.get("message")

        if error:
            return render_template("reservas.html", error=error)
        return render_template("reservas.html", success=success)

    except requests.exceptions.RequestException as e:
        return render_template("reservas.html")
    

@app.route("/disponibilidad", methods=["GET", "POST"])
def disponibilidad():
    try:
        response = requests.get(API_URI + '/hoteles')
        response.raise_for_status()
        hoteles = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener información de hoteles: {e}")
        hoteles = []
        return render_template("disponibilidad.html", hoteles=hoteles, error="No se pudieron cargar los hoteles.")
    
    if request.method == "POST":
        inicio_reserva = request.form.get("inicio_reserva")
        fin_reserva = request.form.get("fin_reserva")
        id_hotel = request.form.get("id_hotel")
        print(inicio_reserva,fin_reserva,id_hotel)
        if not inicio_reserva or not fin_reserva or not id_hotel:
            return render_template("disponibilidad.html", hoteles=hoteles, error="Complete todos los campos del formulario.")

        try:
            
            response = requests.get( API_URI + f"/disponibilidad?id_hotel={id_hotel}&inicio_reserva={inicio_reserva}&fin_reserva={fin_reserva}")
            response.raise_for_status()
            data = response.json()
        
        except requests.exceptions.RequestException as e:
                return render_template("disponibilidad.html", hoteles=hoteles, error=f"Error al consultar disponibilidad: {e}")
        
    return render_template("disponibilidad.html", hoteles=hoteles)

def todos_los_servicios():
    try:
        response = requests.get(API_URI+'servicios')
        response.raise_for_status()
        servicios = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        servicios = []

    return render_template('pruebasServicio.html', servicios=servicios)

@app.route("/servicios-contratados/reserva:<numero_reserva>")
def servicios_contratados(numero_reserva):
    try:
        response = requests.get(API_URI+'servicios-por-reserva/'+numero_reserva)
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
        response = requests.post(API_URI + 'servicios/cancelar-servicio/'+numero_reserva+'/'+id_servicio)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")

    return servicios_contratados(numero_reserva)


@app.route("/contratar-servicio/<numero_reserva>/<id_servicio>")
def contratar_servicio(numero_reserva, id_servicio):
    try:
        response = requests.post(API_URI+'servicios/contratar-servicio/'+numero_reserva+'/'+id_servicio)
        response.raise_for_status()
    except Exception as e:
        print(f"el error esta acaError: {e}")

    return servicios_contratados(numero_reserva)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
