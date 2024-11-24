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
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Tarjeta contenedora
        card = MDCard(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(None, None),
            size=(1000, 1000),  # Aumentado para acomodar la imagen
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=4,
            radius=[20],
            md_bg_color=[1, 1, 1, 1]
        )
        
        # Imagen
        image = Image(
            source='assets/images/dog.png',  # Asegúrate de tener esta imagen
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5}
        )
        card.add_widget(image)
        
        # Encabezado
        card.add_widget(MDLabel(
            text='Iniciar Sesión',
            font_style='H5',
            halign='center',
            size_hint_y=None,
            height=40,
            bold=True,
            padding=40
        ))
        
        # Contenedor para campos de entrada
        fields_container = BoxLayout(
            orientation='vertical',
            spacing=40,
            size_hint_y=None,
            height=dp(200),
            padding=[0, 40, 0, 40]
        )
        
        # Campos de entrada con etiquetas
        self.username = MDTextField(
            hint_text='Usuario',
            helper_text_mode='on_error',
            size_hint=(1, None),
            height=50
        )
        
        self.password = MDTextField(
            hint_text='Contraseña',
            password=True,
            helper_text_mode='on_error',
            size_hint=(1, None),
            height=50
        )
        
        fields_container.add_widget(self.username)
        fields_container.add_widget(self.password)
        
        card.add_widget(fields_container)
        
        # Mensaje de error
        self.message = MDLabel(
            text='',
            theme_text_color='Error',
            halign='center',
            size_hint_y=None,
            height=30
        )
        card.add_widget(self.message)
        
        # Botón de inicio de sesión
        login_btn = MDFillRoundFlatButton(
            text='Iniciar Sesión',
            pos_hint={'center_x': 0.5},
            size_hint=(0.8, None),
            on_release=self.do_login
        )
        card.add_widget(login_btn)
        
        # Enlace de registro
        register_text = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=5,
            pos_hint={'center_x': 0.5}
        )
        
        # Reemplaza la sección del register_text por esto:
        register_box = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            height=50,
            width=300,  # Ajusta este valor según necesites
            spacing=0,
            pos_hint={'center_x': 0.5}
        )

        # Texto no clickeable
        register_box.add_widget(MDLabel(
            text='¿No tienes cuenta? ',  # Espacio añadido al final
            theme_text_color='Secondary',
            size_hint=(None, None),
            size=(300, 50),  # Ajusta el ancho según necesites
            halign='center',
            valign='middle'
        ))

        # Texto clickeable
        register_link = MDTextButton(
            text='Regístrate',
            theme_text_color='Primary',
            size_hint=(None, None),
            size=(300, 50),  # Ajusta el ancho según necesites
            on_release=self.go_to_register
        )
        register_box.add_widget(register_link)

        # Añadir el box a la tarjeta
        card.add_widget(register_box)
        
        # Añadir tarjeta al layout principal
        layout.add_widget(card)
        self.add_widget(layout)
    
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
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        card = MDCard(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(None, None),
            size=(1000, 1000),  # Aumentado para acomodar la imagen
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=4,
            radius=[20],
            md_bg_color=[1, 1, 1, 1]
        )
        
        # Imagen
        image = Image(
            source='assets/images/dog.png',
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5}
        )
        card.add_widget(image)
        
        card.add_widget(MDLabel(
            text='Registro',
            font_style='H5',
            halign='center',
            size_hint_y=None,
            height=50,
            padding=100,
            bold=True
        ))
        
        # Contenedor para campos
        fields_container = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=dp(240),  # Reducido porque ya no tenemos etiquetas
            padding=[0, 20, 0, 20]
        )

        # Crear y añadir campos directamente
        fields = [
            self.create_field('username'),
            self.create_field('password', is_password=True),
            self.create_field('fullname'),
            self.create_field('phone')
        ]

        for field in fields:
            fields_container.add_widget(field)

        card.add_widget(fields_container)
        
        self.message = MDLabel(
            text='',
            theme_text_color='Error',
            halign='center',
            size_hint_y=None,
            height=30
        )
        card.add_widget(self.message)
        
        # Botones
        buttons_container = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=100
        )
        
        register_btn = MDFillRoundFlatButton(
            text='Registrarse',
            pos_hint={'center_x': 0.5},
            size_hint=(0.8, None),
            on_release=self.do_register
        )
        
        back_btn = MDTextButton(
            text='Volver al inicio de sesión',
            theme_text_color='Primary',
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_login
        )
        
        buttons_container.add_widget(register_btn)
        buttons_container.add_widget(back_btn)
        
        card.add_widget(buttons_container)
        
        layout.add_widget(card)
        self.add_widget(layout)

    # Mueve el método fuera del __init__
    def create_field(self, field_type, is_password=False):
        hints = {
            'username': 'Usuario',
            'password': 'Contraseña',
            'fullname': 'Nombre completo',
            'phone': 'Teléfono'
        }
        
        field = MDTextField(
            hint_text=hints[field_type],
            password=is_password,
            helper_text_mode='on_error',
            size_hint=(1, None),
            height=50
        )
        setattr(self, f'{field_type}_field', field)  # Mantener la referencia al campo
        return field
    
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
        self.size_hint_y = None
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