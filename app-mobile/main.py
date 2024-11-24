import kivy
import requests

kivy.require("2.2.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

API_URI = "http://localhost:5001/api/v1"

class Inicio(BoxLayout):

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

    def consultarAPI(self):
        url = f"{API_URI}/reservas/consultar-reserva/{self.input_nro_reserva.text}/{self.input_dni.text}"
        
        url_servicios = f"{API_URI}/servicios-por-reserva/{self.input_nro_reserva.text}"
<<<<<<< HEAD

        url_todos_los_servicios = f"{API_URI}/servicios"

        payload = {}
        headers = {}
        
        self.lista_contratados = []
        self.lista_no_contratados = []
        self.lista_servicios = []

        if self.input_dni.text.replace(" ", "") == "" or self.input_nro_reserva.text.replace(" ", "") == "":
            self.titulo.text = "DATOS INVALIDOS"
        else:
            response = requests.request("GET", url, headers=headers, data=payload)
            self.servicios.text = ""
            self.todos_servicios.text = ""
            data = response.json()
            if data.get('nombre') == None:
                self.titulo.text = "LA RESERVA NO EXISTE " + "\n" + "O FUE CANCELADA."
                self.servicios = ""
                self.todos_servicios = ""
            else:
                servicios = []
                self.titulo.text = f"{data.get('nombre')}\n{data.get('apellido')}\n{data.get('dni')}"
                response = requests.request("GET", url_servicios, headers=headers, data=payload)
                data_servicio = response.json()

                for i in data_servicio:
                   self.lista_contratados.append(str(i['id_servicio']))
                   self.servicios.text += f"{i['id_servicio']} - {i['nombre_servicio']} \n"

                response_servicios = requests.request("GET", url_todos_los_servicios, headers=headers, data=payload)
                data_lista_servicio = response_servicios.json()
                for j in data_lista_servicio:
                    self.lista_servicios.append(str(j['id']))
                    self.todos_servicios.text += f"{j['id']} - {j['nombre']} \n"
                
                for k in self.lista_servicios:
                    if k not in self.lista_contratados:
                        self.lista_no_contratados.append(k)
            

    def quitar_servicio(self, instance):
        self.quitarAPI()

    def agregar_servicio(self, instance):
        self.agregarAPI()

=======

        payload = {}
        headers = {}
<<<<<<< HEAD
        
        if self.input_dni.text.replace(" ", "") == "" or self.input_nro_reserva.text.replace(" ", "") == "":
            self.titulo.text = "DATOS INVALIDOS"
        else:
            response = requests.request("GET", url, headers=headers, data=payload)
            self.servicios.text = ""
            data = response.json()
            if data.get('nombre') == None:
                self.titulo.text = "LA RESERVA NO EXISTE " + "\n" + "O FUE CANCELADA."
            else:
                servicios = []
                self.titulo.text = f"{data.get('nombre')}\n{data.get('apellido')}\n{data.get('dni')}"
                response = requests.request("GET", url_servicios, headers=headers, data=payload)
                data_servicio = response.json()
                for i in data_servicio:
                   self.servicios.text += f"{i['id_servicio']} - {i['nombre_servicio']} \n"
=======

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
>>>>>>> 3014eff24165a4cc83ec65fa13eba58f66b88f50
            

        
        
>>>>>>> aed2c0264edeecda44d595d792c94ba05020eb38
    def on_button_click(self, instance):
        self.consultarAPI()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        self.titulo = Label(text="Flask Seasons", font_size=20, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.add_widget(self.titulo)

<<<<<<< HEAD
        

        

        self.grid_lista = GridLayout(cols=2)        

        self.servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.grid_lista.add_widget(self.servicios)

        self.todos_servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.grid_lista.add_widget(self.todos_servicios)

        self.add_widget(self.grid_lista)

        self.input_agregar_quitar = TextInput(hint_text="Servicio", size_hint=(1, None), height=40)
        # self.input_dni.text = "12312345"
        self.add_widget(self.input_agregar_quitar)

        self.grid = GridLayout(cols=2)

        self.quitar_button = Button(text="Quitar", size_hint=(1, None), height=20, background_color=(0.6, 0.4, 0.8, 1))
        self.quitar_button.bind(on_press=self.quitar_servicio)
        self.grid.add_widget(self.quitar_button)

        self.agregar_button = Button(text="Agregar", size_hint=(1, None), height=20, background_color=(0.6, 0.4, 0.8, 1))
        self.agregar_button.bind(on_press=self.agregar_servicio)
        self.grid.add_widget(self.agregar_button)

        
=======
<<<<<<< HEAD
        

=======
>>>>>>> 3014eff24165a4cc83ec65fa13eba58f66b88f50
        self.servicios = Label(text="", font_size=19, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        self.add_widget(self.servicios)
>>>>>>> aed2c0264edeecda44d595d792c94ba05020eb38

        self.input_dni = TextInput(hint_text="Documento de identidad", size_hint=(1, None), height=50)
        # self.input_dni.text = "12312345"
        self.grid.add_widget(self.input_dni)

        self.input_nro_reserva = TextInput(hint_text="Número de reserva", size_hint=(1, None), height=50)
        # self.input_nro_reserva.text = "100"
        self.grid.add_widget(self.input_nro_reserva)

        self.consult_button = Button(text="Consultar", size_hint=(1, None), height=50, background_color=(0.6, 0.4, 0.8, 1))
        self.consult_button.bind(on_press=self.on_button_click)
        self.grid.add_widget(self.consult_button)

<<<<<<< HEAD

        self.add_widget(self.grid)

=======
>>>>>>> aed2c0264edeecda44d595d792c94ba05020eb38
#45659875
class FlaskSeasonsApp(App):

    def configurar_ventana(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (400, 700)

    def build(self):
        self.configurar_ventana()
        return Inicio()


if __name__ == "__main__":
    FlaskSeasonsApp().run()
