from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.snackbar import Snackbar
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import requests
import hashlib
from kivy.storage.jsonstore import JsonStore
import webbrowser
from kivy.network.urlrequest import UrlRequest 

API_URL = 'http://localhost:5000/api/v1/pets'

class HomeScreen(Screen):
    pass
class BuscarMascotasScreen(Screen):
    pass

class PatitasPerdidasApp(MDApp):
    primary_color = ListProperty(get_color_from_hex("#2f2e41"))
    secondary_color = ListProperty(get_color_from_hex("#675F91"))

    def build(self):
        self.auth_service = AuthService()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        
        screen = Builder.load_file("templates/patitasperdidas.kv")
        
        # Asignar auth_service a las pantallas después de cargarlas
        screen.ids.screen_manager.get_screen('login').auth_service = self.auth_service
        screen.ids.screen_manager.get_screen('register').auth_service = self.auth_service
        
        return screen

    def change_screen(self, screen_name):
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = screen_name
        
    def logout(self):
        # Cerrar la sesión usando el auth_service
        self.auth_service.logout()
        
        # Cerrar el drawer
        self.root.ids.nav_drawer.set_state("close")
        
        # Mostrar mensaje de confirmación
        Snackbar(
            text="Sesión cerrada exitosamente",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.7
        ).open()
        
        # Redirigir a la pantalla de login
        self.change_screen("login")

class RegistrarMascotaScreen(Screen):  
    def show_file_chooser(self):
        filechooser = FileChooserIconView()
        filechooser.bind(on_selection=lambda *x: self.on_file_select(filechooser.selection))

        popup = Popup(title="Seleccionar Imagen", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()

    def on_file_select(self, selection):
        if selection:
            self.ids.image.text = selection[0]

    def register_pet(self):
        name = self.ids.name.text
        animal_type = 'Gato' if self.ids.animal_type_gato.active else 'Perro'
        sex = 'Macho' if self.ids.sex_macho.active else 'Hembra'
        has_tag = 'Sí' if self.ids.has_tag_yes.active else 'No'
        color = self.ids.color.text
        city = self.ids.city.text
        address = self.ids.address.text
        image = self.ids.file_label.text  
    
        if not all([name, color, city, address, image, animal_type, sex, has_tag]):
            return

class AuthService:
    def __init__(self):
        self.api_url = 'http://localhost:5000/api/v1'
        self.storage = JsonStore('user_data.json')
    
    def login(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            
            response = requests.post(
                f"{self.api_url}/login",
                json={
                    "username": username,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.storage.put('user_session', 
                    token=data['access_token'],
                    username=username
                )
                return True, "Login exitoso"
            else:
                return False, response.json().get('error', 'Error en el login')
                
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def register(self, username, password, name, phone):
        try:
            response = requests.post(
                f"{self.api_url}/register",
                json={
                    "username": username,
                    "password": password,
                    "name": name,
                    "phone": phone
                }
            )
            
            if response.status_code == 201:
                return True, "Registro exitoso"
            else:
                return False, response.json().get('error', 'Error en el registro')
                
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"
    
    def logout(self):
        if 'user_session' in self.storage:
            self.storage.delete('user_session')
    
    def is_logged_in(self):
        return 'user_session' in self.storage
    
    def get_current_user(self):
        if self.is_logged_in():
            return self.storage.get('user_session')
        return None
    
    def get_auth_header(self):
        user_data = self.get_current_user()
        if user_data and 'token' in user_data:
            return {'Authorization': f'Bearer {user_data["token"]}'}
        return {}

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = None
    
    def go_to_register(self, *args):
        self.manager.current = "register"
    
    def do_login(self, *args):
        username = self.username.text.strip()
        password = self.password.text
        
        if not username or not password:
            self.message.text = 'Por favor completa todos los campos'
            return
        
        success, message = self.auth_service.login(username, password)
        if success:
            self.manager.current = 'home'
        else:
            self.message.text = message


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = None

    def go_to_login(self, *args):
        self.manager.current = "login"
    
    def do_register(self, *args):
        username = self.username_field.text.strip()
        password = self.password_field.text
        name = self.fullname_field.text.strip()
        phone = self.phone_field.text.strip()
        
        if not all([username, password, name, phone]):
            self.message.text = 'Por favor completa todos los campos'
            return
        
        success, message = self.auth_service.register(username, password, name, phone)
        if success:
            self.manager.current = 'login'
        else:
            self.message.text = message
    

class SobreNosotrosScreen(Screen):
    def open_website(self):
        webbrowser.open("https://patitas-perdidas.vercel.app/")

class ContactoScreen(Screen):
    def send_contact_data(self):
        name = self.ids.name.text.strip()
        email = self.ids.email.text.strip()
        message = self.ids.message.text.strip()
        
        if not all([name, email, message]):
            print("Por favor, completa todos los campos")
            return
        
        data = {
            "name": name,
            "email": email,
            "message": message
        }
        
        endpoint = "http://localhost:5000/send_email"
        
        try:
            response = requests.post(endpoint, data=data)
            
            if response.status_code == 200:
                print("Mensaje enviado exitosamente")
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
        
        self.add_widget(MDLabel(
            text=mascota_data.get('pet_name', ''),
            font_style="H5",
            halign="center"
        ))
        
        tipo = "Perro" if mascota_data.get('type') == 'dog' else "Gato"
        self.add_widget(MDLabel(
            text=tipo,
            font_style="Subtitle1",
            halign="center"
        ))
        
        self.add_widget(MDLabel(
            text=mascota_data.get('breed', ''),
            font_style="Subtitle1",
            halign="center"
        ))
        
        self.add_widget(MDLabel(
            text=mascota_data.get('color', ''),
            font_style="Subtitle1",
            halign="center"
        ))
        
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