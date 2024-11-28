import kivy
import requests

kivy.require("2.2.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox

API_URI = "http://localhost:5001/api/v1"

class Servicios(BoxLayout, Screen):

    def volver_a_inicio(self, instance=None):
        inicio = self.manager.get_screen("inicio")
        inicio.texto_exito.text = self.texto_exito
        inicio.texto_error.text = ""
        self.manager.current = "inicio"

    def contratar_servicio(self, id_servicio):
        url = f"{API_URI}/servicios/contratar-servicio/{self.nro_reserva}/{id_servicio}"

        try:
            requests.request("POST", url)
            self.texto_exito = "Guardado exitosamente"
            self.hubo_cambios = True

        except:
            self.texto_error.text = "Error al contratar servicios"

    def cancelar_servicio(self, id_servicio):
        url = f"{API_URI}/reservas/{self.nro_reserva}/servicios/{id_servicio}"

        try:
            requests.request("DELETE", url)
            self.texto_exito = "Guardado exitosamente"
            self.hubo_cambios = True
        except:
            self.texto_error.text = "Error al cancelar servicios"

    def guardar_click(self, instance):

        self.hubo_cambios = False

        for i in self.datos_todos_los_servicios:

            ya_contratado = True if i.get("ya_contratado") else False
            activo = True if i.get("activo") else False

            if not ya_contratado:
                if activo:
                    self.contratar_servicio(i["id"])
            else:
                if not activo:
                    self.cancelar_servicio(i["id"])

        if self.hubo_cambios:
            self.volver_a_inicio()

    def click_en_checkbox(self, checkbox, valor, indice_servicio):
        self.datos_todos_los_servicios[indice_servicio]["activo"] = valor

    def on_pre_enter(self, *args):
        self.clear_widgets()
        self.texto_exito = ""

        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        self.titulo = Label(
            text="Servicios Disponibles",
            font_size=20,
            size_hint=(1, 1),
            color=(0, 0, 0, 1),
        )
        self.add_widget(self.titulo)

        for indice, item in enumerate(self.datos_todos_los_servicios):
            fila = BoxLayout(orientation="horizontal", size_hint=(1, None), height=20)

            checkbox = CheckBox(size_hint_x=0.1, active=True if item.get("activo") else False)

            label = Label(text=f"{item["nombre"]}", size_hint_x=0.9, halign="left", valign="middle", color=(0, 0, 0, 1))
            label.bind(size=label.setter("text_size"))

            checkbox.bind(active=lambda checkbox, valor, indice_servicio=indice: self.click_en_checkbox(checkbox, valor, indice_servicio))

            fila.add_widget(checkbox)
            fila.add_widget(label)
            self.add_widget(fila)

        self.bloque = BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.add_widget(self.bloque)

        self.texto_error = Label(text="", font_size=12, size_hint=(1, None), color="red", height=50)
        self.bloque.add_widget(self.texto_error)

        self.boton_volver_a_inicio = Button(text="Volver", size_hint=(1, None), height=50, background_color=(0.961, 0.961, 0.961, 0.5))
        self.boton_volver_a_inicio.bind(on_press=self.volver_a_inicio)
        self.bloque.add_widget(self.boton_volver_a_inicio)

        self.boton_guardar_servicios = Button(text="Guardar", size_hint=(1, None), height=50, background_color=(0.6, 0.4, 0.8, 1))
        self.boton_guardar_servicios.bind(on_press=self.guardar_click)
        self.bloque.add_widget(self.boton_guardar_servicios)


class Inicio(BoxLayout, Screen):

    def ir_a_servicios(self):
        servicios = self.manager.get_screen("servicios")
        servicios.datos_todos_los_servicios = self.datos_todos_los_servicios
        servicios.datos_servicios_contratados = self.datos_servicios_contratados
        servicios.nro_reserva = self.input_nro_reserva.text

        self.manager.current = "servicios"

    def conseguir_servicios_contratados(self):
        url = f"{API_URI}/reservas/{self.input_nro_reserva.text}/servicios"

        try:
            respuesta = requests.get(url)
            datos = respuesta.json()
            return datos
        except:
            print("aca")
            return None

    def conseguir_todos_los_servicios(self):
        url = f"{API_URI}/servicios"

        try:
            respuesta = requests.get(url)
            datos = respuesta.json()
            return datos
        except:
            return None

    def consultar_reserva(self):
        nro_reserva = self.input_nro_reserva.text

        url = f"{API_URI}/reservas/{nro_reserva}"

        try:
            respuesta = requests.get(url)
            datos = respuesta.json()

            error = datos.get("error")

            if error:
                self.texto_error.text = "No se encontró la reserva"
                return None

            self.datos_todos_los_servicios = self.conseguir_todos_los_servicios()
            self.datos_servicios_contratados = self.conseguir_servicios_contratados()

            if (self.datos_servicios_contratados is None) or (self.datos_todos_los_servicios is None):
                self.texto_error.text = "Error interno"
                return None

            for index, i in enumerate(self.datos_todos_los_servicios):
                for j in self.datos_servicios_contratados:
                    if i["id"] == j["id_servicio"]:
                        self.datos_todos_los_servicios[index]["ya_contratado"] = True
                        self.datos_todos_los_servicios[index]["activo"] = True
            
            self.ir_a_servicios()

        except:
            self.texto_error.text = "Error interno"
            return None

    def consultar_click(self, instance):
        if (len(self.input_dni.text) != 8) | (len(self.input_nro_reserva.text) < 3):
            self.texto_error.text = "Datos Inválidos"
        else:
            self.consultar_reserva()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        self.titulo = Label(text="Flask Seasons", font_size=26, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.add_widget(self.titulo)

        self.texto_error = Label(text="", font_size=12, size_hint=(1, None), color="red", height=50)
        self.add_widget(self.texto_error)

        self.texto_exito = Label(text="", font_size=12, size_hint=(1, None), color="green", height=50)
        self.add_widget(self.texto_exito)

        self.input_dni = TextInput(hint_text="Documento de identidad", size_hint=(1, None), height=50)
        self.input_dni.text = "12312345"
        self.add_widget(self.input_dni)

        self.input_nro_reserva = TextInput(hint_text="Número de reserva", size_hint=(1, None), height=50)
        self.input_nro_reserva.text = "100"
        self.add_widget(self.input_nro_reserva)

        self.consultar_boton = Button(
            text="Consultar",
            size_hint=(1, None),
            height=50,
            background_color=(0.6, 0.4, 0.8, 1),
        )
        self.consultar_boton.bind(on_press=self.consultar_click)
        self.add_widget(self.consultar_boton)


class FlaskSeasonsApp(App):

    def configurar_ventana(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (400, 700)

    def configurar_screen_manager(self):
        sm = ScreenManager()
        sm.add_widget(Inicio(name="inicio"))
        sm.add_widget(Servicios(name="servicios"))
        return sm

    def build(self):
        self.configurar_ventana()
        sm = self.configurar_screen_manager()
        return sm


if __name__ == "__main__":
    FlaskSeasonsApp().run()
