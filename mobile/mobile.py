from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.utils import get_color_from_hex  # Correcta importación de get_color_from_hex
from kivymd.app import MDApp
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.snackbar import Snackbar
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton

import webbrowser
import requests

# Definir las pantallas
class HomeScreen(Screen):
    pass

class MascotasPerdidasScreen(Screen):
    pass

class BuscarMascotasScreen(Screen):
    pass

# Clase principal de la app
class PatitasPerdidasApp(MDApp):
    primary_color = ListProperty(get_color_from_hex("#2f2e41"))  # Convertir hexadecimal a RGBA
    secondary_color = ListProperty(get_color_from_hex("#675F91"))  # Convertir hexadecimal a RGBA

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_file("templates/patitasperdidas.kv")

    def change_screen(self, screen_name):
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = screen_name


class RegistrarMascotaScreen(Screen):  #
    def show_file_chooser(self):
        filechooser = FileChooserIconView()
        filechooser.bind(on_selection=lambda *x: self.on_file_select(filechooser.selection))

        popup = Popup(title="Seleccionar Imagen", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()

    def on_file_select(self, selection):
        if selection:
            self.ids.image.text = selection[0]  # Suponiendo que 'image' es un TextInput
            Snackbar(text="Imagen seleccionada").open()

    def register_pet(self):
        name = self.ids.name.text
        animal_type = 'Gato' if self.ids.animal_type_gato.active else 'Perro'
        sex = 'Macho' if self.ids.sex_macho.active else 'Hembra'
        has_tag = 'Sí' if self.ids.has_tag_yes.active else 'No'
        color = self.ids.color.text
        city = self.ids.city.text
        address = self.ids.address.text
        image = self.ids.file_label.text  
    
        # Rama, deje encaminada la logica de validacion de campos (para evitar que crashee la app al tocar el boton ademas), pero falta el tema snackbar, asi que
        # crashea igual xd
        if not name or not color or not city or not address or not image:
            Snackbar(text="Por favor, completa todos los campos").open()
            return  
    
        if not animal_type:
            Snackbar(text="Por favor, selecciona el tipo de animal").open()
            return  # Detener la ejecución si no se seleccionó el tipo de animal
    
        if not sex:
            Snackbar(text="Por favor, selecciona el sexo de la mascota").open()
            return  # Detener la ejecución si no se seleccionó el sexo

        if not has_tag:
            Snackbar(text="Por favor, selecciona si tiene chapa").open()
            return  # Detener la ejecución si no se seleccionó si tiene chapa
    
        # Si todos los campos están completos, se realiza el registro
        Snackbar(text="Mascota registrada exitosamente!").open()

class SobreNosotrosScreen(Screen):
    def open_website(self):
        webbrowser.open("https://patitas-perdidas.vercel.app/")  
    
class ContactoScreen(Screen):
    def send_contact_data(self):
        name = self.ids.name.text
        email = self.ids.email.text
        message = self.ids.message.text

        # Las keys del diccionario tienen que coincidir con lo que espera el endpoint enviar_email y los valores con la info de kivy
        data = {
            "name": name,
            "email": email,
            "message": message
        }

        endpoint = "https://localhost:5001/enviar_email" 

        try:
            response = requests.post(endpoint, data=data)
            if response.status_code == 200:
                print("Data send successfully")
            else:
                print(f"Error sending data: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")

if __name__ == "__main__":
    PatitasPerdidasApp().run()