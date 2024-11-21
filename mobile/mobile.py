from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import webbrowser

class PatitasPerdidas(App):
    def build(self):
        Builder.load_file('templates/patitasperdidas.kv')  # Carga explícita del archivo .kv
        return BoxLayout()
    
    def open_website(self, *args):
        webbrowser.open("https://patitas-perdidas.vercel.app/")  # URL del sitio web

patitas_perdidas = PatitasPerdidas()
patitas_perdidas.run()
