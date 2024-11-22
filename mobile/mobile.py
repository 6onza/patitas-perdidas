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
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
import webbrowser
import requests

from kivy.network.urlrequest import UrlRequest 
API_URL = 'http://localhost:5000/api/v1/pets'

# Definir las pantallas
class HomeScreen(Screen):
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


class RegistrarMascotaScreen(Screen):  
    def show_file_chooser(self):
        filechooser = FileChooserIconView()
        filechooser.bind(on_selection=lambda *x: self.on_file_select(filechooser.selection))

        popup = Popup(title="Seleccionar Imagen", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()

    def on_file_select(self, selection):
        if selection:
            self.ids.image.text = selection[0]  # Suponiendo que 'image' es un TextInput

    def register_pet(self):
        name = self.ids.name.text
        animal_type = 'Gato' if self.ids.animal_type_gato.active else 'Perro'
        sex = 'Macho' if self.ids.sex_macho.active else 'Hembra'
        has_tag = 'Sí' if self.ids.has_tag_yes.active else 'No'
        color = self.ids.color.text
        city = self.ids.city.text
        address = self.ids.address.text
        image = self.ids.file_label.text  
    
        # Validar los datos
        if not name or not color or not city or not address or not image:
            return  
    
        if not animal_type:
            return  
    
        if not sex:
            return 

        if not has_tag:
            return  
    
        

class SobreNosotrosScreen(Screen):
    def open_website(self):
        webbrowser.open("https://patitas-perdidas.vercel.app/")  
    
class ContactoScreen(Screen):
    def send_contact_data(self):
        # Esto es para obtener los datos de cada field
        name = self.ids.name.text.strip()
        email = self.ids.email.text.strip()
        message = self.ids.message.text.strip()
        
        # Validar que los campos no estén vacíos
        if not all([name, email, message]):
            print("Por favor, completa todos los campos")
            return
        
        # Le mandamos al endpoint la data que fue ingresada en el form de la app
        data = {
            "name": name,
            "email": email,
            "message": message
        }
        
        # Endpoint local
        endpoint = "http://localhost:5000/send_email"
        
        try:
            response = requests.post(endpoint, data=data)
            
            if response.status_code == 200:
                print("Mensaje enviado exitosamente")
                # Limpia los fields despues de enviar el formulario
                self.ids.name.text = ""
                self.ids.email.text = ""
                self.ids.message.text = ""
            else:
                print(f"Error al enviar el mensaje: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            
        except Exception as e:
            print(f"Error inesperado: {e}")

class MascotaCard(MDCard):
    def __init__(self, mascota_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "12dp"
        self.spacing = "12dp"
        self.size_hint_y = "12dp"
        self.height = "320dp"  
        self.elevation = 2
        
        # Nombre de la mascota
        self.add_widget(MDLabel(
            text=mascota_data.get('pet_name', ''),
            font_style="H5",
            halign="center"
        ))
        
        # Tipo de mascota 
        tipo = "Perro" if mascota_data.get('type') == 'dog' else "Gato"
        self.add_widget(MDLabel(
            text=tipo,
            font_style="Subtitle1",
            halign="center"
        ))
        
        # Raza
        self.add_widget(MDLabel(
            text=mascota_data.get('breed', ''),
            font_style="Subtitle1",
            halign="center"
        ))
        
        # Color
        self.add_widget(MDLabel(
            text=mascota_data.get('color', ''),
            font_style="Subtitle1",
            halign="center"
        ))
        
        # Ubicación
        self.add_widget(MDLabel(
            text=mascota_data.get('lost_location', ''),
            font_style="Subtitle1",
            halign="center"
        ))
        
        self.add_widget(MDFillRoundFlatButton(
            text="Saber más",
            pos_hint={"center_x": 0.5}
        ))

class MascotasPerdidasScreen(Screen):
    def on_pre_enter(self, *args):
        UrlRequest(
            API_URL,
            on_success=self.on_mascotas_cargadas,
            verify=False
        )
    
    def on_mascotas_cargadas(self, request, result):
        container = self.ids.container
        container.clear_widgets()
        
        for mascota in result:
            card = MascotaCard(mascota)
            container.add_widget(card)


if __name__ == "__main__":
    PatitasPerdidasApp().run()