import kivy
from kivy.app import App
from kivy.core.text import LabelBase
# from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.colors import new_rgb_color


kivy.require('1.9.0')


# Add custom fonts
LabelBase.register(
    name='Montserrat', 
    fn_regular='assets/fonts/Montserrat-Bold.ttf'
)


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def change_color(self):
        self.main_title.color = new_rgb_color()


class HelloWorld(App):

    # .kv files path
    kv_directory = "templates"

    def build(self):
        # return Label(text="Hello World!")
        return MyRoot()

    
if __name__ == "__main__":
    app = HelloWorld()
    app.run() 
