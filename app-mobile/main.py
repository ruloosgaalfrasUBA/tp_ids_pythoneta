import kivy
import requests
import json

kivy.require("2.2.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox

API_URI = "http://localhost:5001/api/v1"


class Servicios(BoxLayout, Screen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        self.datos_todos_los_servicios = self.lista_todos_los_servicios

        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        self.titulo = Label(text="Servicios Disponibles", font_size=20, size_hint=(1, 1), color=(0, 0, 0, 1))
        self.add_widget(self.titulo)

        for item in self.datos_todos_los_servicios:
            fila = BoxLayout(orientation="horizontal", size_hint=(1, None), height=20)

            checkbox = CheckBox(size_hint_x=0.1, active=True if item.get("activo") else False)
            label = Label(text=f"{item["nombre"]}", size_hint_x=0.9, halign="left", valign="middle", color=(0, 0, 0, 1))
            label.bind(size=label.setter("text_size"))

            fila.add_widget(checkbox)
            fila.add_widget(label)
            self.add_widget(fila)

        self.bloque = BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.add_widget(self.bloque)

        self.boton_volver_a_inicio = Button(text="Volver", size_hint=(1, None), height=50, background_color=(0.961, 0.961, 0.961, 0.5))
        self.boton_volver_a_inicio.bind(on_press=self.volver_a_inicio)
        self.bloque.add_widget(self.boton_volver_a_inicio)

        self.boton_guardar_servicios = Button(text="Guardar", size_hint=(1, None), height=50, background_color=(0.6, 0.4, 0.8, 1))

        self.bloque.add_widget(self.boton_guardar_servicios)

    def volver_a_inicio(self, instance):
        self.manager.current = 'inicio'

class Inicio(BoxLayout, Screen):

    def quitarAPI(self):
        url = f"{API_URI}/servicios/cancelar-servicio/{self.input_nro_reserva.text}/{self.input_agregar_quitar.text}"
        headers = []
        payload = []
        if self.input_agregar_quitar.text not in self.lista_contratados:
            print("No lo tenes")
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
        self.consultarAPI()
        return

    def agregarAPI(self):
        url = f"{API_URI}/servicios/contratar-servicio/{self.input_nro_reserva.text}/{self.input_agregar_quitar.text}"
        headers = []
        payload = []
        if self.input_agregar_quitar.text in self.lista_contratados:
            print("Ya lo tenes")
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
        self.consultarAPI()
        return

    def conseguir_servicios_contratados(self):
        url_servicios_contratados = f"{API_URI}/servicios-por-reserva/{self.input_nro_reserva.text}"

        try:
            respuesta = requests.get(url_servicios_contratados)
            datos = respuesta.json()
            return datos
        except:
            return None

    def conseguir_todos_los_servicios(self):
        url_todos_los_servicios = f"{API_URI}/servicios"

        try:
            respuesta = requests.get(url_todos_los_servicios)
            datos = respuesta.json()
            return datos
        except:
            return None

    def consultar_reserva(self):
        nro_reserva = self.input_nro_reserva.text
        dni = self.input_dni.text

        url = f"{API_URI}/reservas/consultar-reserva/{nro_reserva}/{dni}"

        try:
            respuesta = requests.get(url)
            datos = respuesta.json()

            error = datos.get("error")

            if error:
                self.texto_error.text = "No se encontró la reserva"
                return None

            datos_todos_los_servicios = self.conseguir_todos_los_servicios()
            datos_servicios_contratados = self.conseguir_servicios_contratados()

            if not datos_servicios_contratados or not datos_todos_los_servicios:
                self.texto_error.text = "Error interno"
                return None
            
            for index, i in enumerate(datos_todos_los_servicios):
                for j in datos_servicios_contratados:
                    if (i["id"] == j["id_servicio"]):
                        datos_todos_los_servicios[index]["activo"] = True


            self.manager.get_screen("servicios").lista_todos_los_servicios = datos_todos_los_servicios
            
            self.manager.current = "servicios"

        except:
            self.texto_error.text = "Error interno"
            return None

        # url_servicios = f"{API_URI}/servicios-por-reserva/{self.input_nro_reserva.text}"

        # url_todos_los_servicios = f"{API_URI}/servicios"

        # payload = {}
        # headers = {}

        # self.lista_contratados = []
        # self.lista_no_contratados = []
        # self.lista_servicios = []

        # if self.input_dni.text.replace(" ", "") == "" or self.input_nro_reserva.text.replace(" ", "") == "":
        #     self.titulo.text = "DATOS INVALIDOS"
        # else:
        #     response = requests.request("GET", url, headers=headers, data=payload)
        #     self.servicios.text = ""
        #     self.todos_servicios.text = ""
        #     data = response.json()
        #     if data.get("nombre") == None:
        #         self.titulo.text = "LA RESERVA NO EXISTE " + "\n" + "O FUE CANCELADA."
        #         self.servicios = ""
        #         self.todos_servicios = ""
        #     else:
        #         servicios = []
        #         self.titulo.text = f"{data.get('nombre')}\n{data.get('apellido')}\n{data.get('dni')}"
        #         response = requests.request("GET", url_servicios, headers=headers, data=payload)
        #         data_servicio = response.json()

        #         for i in data_servicio:
        #             self.lista_contratados.append(str(i["id_servicio"]))
        #             self.servicios.text += f"{i['id_servicio']} - {i['nombre_servicio']} \n"

        #         response_servicios = requests.request("GET", url_todos_los_servicios, headers=headers, data=payload)
        #         data_lista_servicio = response_servicios.json()
        #         for j in data_lista_servicio:
        #             self.lista_servicios.append(str(j["id"]))
        #             self.todos_servicios.text += f"{j['id']} - {j['nombre']} \n"

        #         for k in self.lista_servicios:
        #             if k not in self.lista_contratados:
        #                 self.lista_no_contratados.append(k)

    def quitar_servicio(self, instance):
        self.quitarAPI()

    def agregar_servicio(self, instance):
        self.agregarAPI()

    def on_consultar_click(self, instance):
        if (len(self.input_dni.text) != 8) | (len(self.input_nro_reserva.text) < 3):
            self.texto_error.text = "Datos Inválidos"
        else:
            self.consultar_reserva()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        self.titulo = Label(text="Flask Seasons", font_size=20, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.add_widget(self.titulo)

        # self.grid_lista = GridLayout(cols=2)

        # self.servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        # self.grid_lista.add_widget(self.servicios)

        # self.todos_servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        # self.grid_lista.add_widget(self.todos_servicios)

        # self.add_widget(self.grid_lista)

        # self.input_agregar_quitar = TextInput(hint_text="Servicio", size_hint=(1, None), height=40)
        # # self.input_dni.text = "12312345"
        # self.add_widget(self.input_agregar_quitar)

        # self.grid = GridLayout(cols=2)

        # self.quitar_button = Button(text="Quitar", size_hint=(1, None), height=20, background_color=(0.6, 0.4, 0.8, 1))
        # self.quitar_button.bind(on_press=self.quitar_servicio)
        # self.grid.add_widget(self.quitar_button)

        # self.agregar_button = Button(text="Agregar", size_hint=(1, None), height=20, background_color=(0.6, 0.4, 0.8, 1))
        # self.agregar_button.bind(on_press=self.agregar_servicio)
        # self.grid.add_widget(self.agregar_button)

        # self.servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        # self.add_widget(self.servicios)

        self.texto_error = Label(text="", font_size=12, size_hint=(1, None), color="red", height=50)
        self.add_widget(self.texto_error)

        self.input_dni = TextInput(hint_text="Documento de identidad", size_hint=(1, None), height=50)
        self.input_dni.text = "12312345"
        self.add_widget(self.input_dni)

        self.input_nro_reserva = TextInput(hint_text="Número de reserva", size_hint=(1, None), height=50)
        self.input_nro_reserva.text = "100"
        self.add_widget(self.input_nro_reserva)

        self.consultar_boton = Button(text="Consultar", size_hint=(1, None), height=50, background_color=(0.6, 0.4, 0.8, 1))
        self.consultar_boton.bind(on_press=self.on_consultar_click)
        self.add_widget(self.consultar_boton)

        # self.add_widget(self.grid)


# 45659875
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
