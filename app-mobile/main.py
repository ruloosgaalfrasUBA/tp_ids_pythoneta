import kivy
import requests

kivy.require("2.2.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

API_URI = "http://localhost:5001/api/v1"

class Inicio(BoxLayout):

    def consultarAPI(self):
        url = f"{API_URI}/reservas/consultar-reserva/{self.input_nro_reserva.text}/{self.input_dni.text}"
        
        url_servicios = f"{API_URI}/servicios-por-reserva/{self.input_nro_reserva.text}"

        payload = {}
        headers = {}

        payload_servicios = {}
        headers_servicios = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.servicios.text = ""
        data = response.json()
        if data.get('nombre') == None:
            self.titulo.text = "LA RESERVA NO EXISTE " + "\n" + "O FUE CANCELADA."
        else: 
            self.titulo.text = f"{data.get('nombre')}\n{data.get('apellido')}\n{data.get('dni')}"
            response_servicios = requests.request("GET", url_servicios, headers=headers_servicios, data=payload_servicios)
            data_servicio = response_servicios.json()
            for i in data_servicio:
                self.servicios.text += f"{i['id_servicio']} - {i['nombre_servicio']} \n"
            

        
        
    def on_button_click(self, instance):
        self.consultarAPI()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        self.titulo = Label(text="Flask Seasons", font_size=20, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.add_widget(self.titulo)

        self.servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.add_widget(self.servicios)

        self.input_dni = TextInput(hint_text="Documento de identidad", size_hint=(1, None), height=50)
        # self.input_dni.text = "12312345"
        self.add_widget(self.input_dni)

        self.input_nro_reserva = TextInput(hint_text="Número de reserva", size_hint=(1, None), height=50)
        # self.input_nro_reserva.text = "100"
        self.add_widget(self.input_nro_reserva)

        self.consult_button = Button(text="Consultar", size_hint=(1, None), height=50, background_color=(0.6, 0.4, 0.8, 1))
        self.consult_button.bind(on_press=self.on_button_click)
        self.add_widget(self.consult_button)

#45659875
class FlaskSeasonsApp(App):

    def configurar_ventana(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (300, 700)

    def build(self):
        self.configurar_ventana()
        return Inicio()


if __name__ == "__main__":
    FlaskSeasonsApp().run()
