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
from kivy.uix.label import Label
from kivy.metrics import dp
import requests
import hashlib
from kivy.storage.jsonstore import JsonStore
import webbrowser
from kivy.network.urlrequest import UrlRequest 
from kivymd.uix.widget import Widget

from datetime import datetime
from functools import partial
import base64
import os
import json

from kivy.core.window import Window
Window.size = (360, 640)
Window.allow_resize = False

API_URL = 'http://localhost:5000/api/v1/pets'

class HomeScreen(Screen):
    pass
class BuscarMascotasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = []

    def search_pets(self):
        # Get values from form
        params = {}
        if self.ids.gato.active:
            params['type'] = 'cat'
        elif self.ids.perro.active:
            params['type'] = 'dog'
        if self.ids.macho.active:
            params['sex'] = 'male'
        elif self.ids.hembra.active:
            params['sex'] = 'female'
        if self.ids.con_chapa.active:
            params['has_tag'] = 'True'
        elif self.ids.sin_chapa.active:
            params['has_tag'] = 'False'
        params['city'] = self.ids.ciudad.text
        params['address'] = self.ids.direccion.text

        # Build query string
        query_params = '&'.join([f"{k}={v}" for k, v in params.items() if v])
        url = f'http://localhost:5000/api/v1/pets/search'

        # Make API request
        UrlRequest(
            f"{url}?{query_params}",
            on_success=self.handle_search_success,
            on_error=self.handle_search_error,
            on_failure=self.handle_search_error
        )

    def handle_search_success(self, request, result):
        # Validar que el backend devolvió resultados válidos
        if not isinstance(result, list):
            self.ids.results_label.text = "Error: formato de datos inválido recibido del servidor"
            return

        # Guardar los resultados y actualizar pantalla
        self.results = result
        app = PatitasPerdidasApp.get_running_app()
        resultados_screen = app.root.ids.screen_manager.get_screen("resultados_busqueda")
        resultados_screen.set_results(self.results)
        app.change_screen("resultados_busqueda")

    def handle_search_error(self, request, error):
        self.ids.results_label.text = f"Error al buscar mascotas: {str(error)}"

    def update_results_display(self):
        # Limpiar resultados previos
        results_container = self.ids.results_container
        results_container.clear_widgets()

        if not self.results:
            # Mostrar mensaje de no resultados
            no_results_label = MDLabel(
                text="No se encontraron mascotas con los criterios especificados",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="40dp"
            )
            results_container.add_widget(no_results_label)
            return

        # Validar y filtrar resultados basados en los criterios seleccionados
        filtered_results = self.results
        if self.ids.gato.active:
            filtered_results = [pet for pet in filtered_results if pet.get('type') == 'cat']
        elif self.ids.perro.active:
            filtered_results = [pet for pet in filtered_results if pet.get('type') == 'dog']
        if self.ids.macho.active:
            filtered_results = [pet for pet in filtered_results if pet.get('sex') == 'male']
        elif self.ids.hembra.active:
            filtered_results = [pet for pet in filtered_results if pet.get('sex') == 'female']
        if self.ids.con_chapa.active:
            filtered_results = [pet for pet in filtered_results if pet.get('has_tag') == 'True']
        elif self.ids.sin_chapa.active:
            filtered_results = [pet for pet in filtered_results if pet.get('has_tag') == 'False']

        # Mostrar mensaje si no quedan resultados tras filtrar
        if not filtered_results:
            no_results_label = MDLabel(
                text="No se encontraron mascotas que coincidan con los criterios seleccionados.",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="40dp"
            )
            results_container.add_widget(no_results_label)
            return

        # Agregar tarjetas de resultados filtrados
        for pet in filtered_results:
            card = MDCard(
                orientation="vertical",
                size_hint=(1, None),
                height="180dp",
                padding="10dp",
                spacing="10dp",
                elevation=1
            )

            # Encabezado con nombre y tipo
            header = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="30dp"
            )
            name_label = MDLabel(
                text=f"{pet['pet_name']} - {pet['type'].capitalize()}",
                theme_text_color="Primary",
                font_style="H6"
            )
            header.add_widget(name_label)

            # Detalles de la mascota
            details = MDLabel(
                text=f"""
                Sexo: {pet['sex']}
                Raza: {pet['breed']}
                Color: {pet['color']}
                Fecha de pérdida: {pet['lost_date']}
                Ubicación: {pet['lost_location']}
                Descripción: {pet['description']}
                """.strip(),
                theme_text_color="Secondary",
                size_hint_y=None,
                height="120dp"
            )
            card.add_widget(header)

            # Separador visual
            separator = Widget(size_hint_y=None, height="1dp")
            separator.md_bg_color = [0, 0, 0, 1]
            card.add_widget(separator)
            card.add_widget(details)

            # Agregar tarjeta al contenedor
            results_container.add_widget(card)

class ResultadosBusquedaScreen(Screen):
    def set_results(self, results):
        results_container = self.ids.results_container
        results_container.clear_widgets()

        if not results:
            no_results_label = MDLabel(
                text="No se encontraron mascotas con los criterios especificados",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="40dp"
            )
            results_container.add_widget(no_results_label)
            return

        for pet in results:
            card = MDCard(
                orientation="vertical",
                size_hint=(1, None),
                height="180dp",
                padding="10dp",
                spacing="10dp",
                elevation=1
            )

            header = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="30dp"
            )
            name_label = MDLabel(
                text=f"{pet['pet_name']} - {pet['type'].capitalize()}",
                theme_text_color="Primary",
                font_style="H6"
            )
            header.add_widget(name_label)

            details = MDLabel(
                text=f"""
                Sexo: {pet['sex']}
                Raza: {pet['breed']}
                Color: {pet['color']}
                Fecha de pérdida: {pet['lost_date']}
                Ubicación: {pet['lost_location']}
                Descripción: {pet['description']}
                """.strip(),
                theme_text_color="Secondary",
                size_hint_y=None,
                height="120dp"
            )
            card.add_widget(header)

            separator = Widget(size_hint_y=None, height="1dp")
            separator.md_bg_color = [0, 0, 0, 1]
            card.add_widget(separator)
            card.add_widget(details)

            results_container.add_widget(card)

    def go_to_search(self):
        # Cambiar de vuelta a la pantalla de búsqueda
        PatitasPerdidasApp.get_running_app().change_screen("buscar_mascotas")
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

    def show_message(self, title, message):
        popup = Popup(title=title,
                     content=Label(text=message),
                     size_hint=(0.8, 0.3))
        popup.open()

    def on_success(self, req, result):
        self.show_message('Éxito', 'Mascota registrada correctamente')
        
        self.clear_fields()

    def on_failure(self, req, error):
        self.show_message('Error', f'Error al registrar mascota: {error}')

    def on_error(self, req, error):
        self.show_message('Error', 'Error de conexión con el servidor')

    def clear_fields(self):
        self.ids.name.text = ''
        self.ids.color.text = ''
        self.ids.city.text = ''
        self.ids.address.text = ''
        self.ids.image.text = ''
        self.ids.animal_type_gato.active = False
        self.ids.animal_type_perro.active = False
        self.ids.sex_macho.active = False
        self.ids.sex_hembra.active = False
        self.ids.has_tag_yes.active = False
        self.ids.has_tag_no.active = False

    def get_image_base64(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error al procesar imagen: {e}")
            return None

    def register_pet(self):
        name = self.ids.name.text
        animal_type = 'cat' if self.ids.animal_type_gato.active else 'dog'
        sex = 'male' if self.ids.sex_macho.active else 'female'
        has_tag = True if self.ids.has_tag_yes.active else False
        color = self.ids.color.text
        city = self.ids.city.text
        address = self.ids.address.text
        image_path = self.ids.image.text  # El campo de la imagen es opcional

        latitude = self.ids.latitude.text  # Obtener latitud del formulario
        longitude = self.ids.longitude.text  # Obtener longitud del formulario

        # Validar solo los campos obligatorios
        if not all([name, color, city, address]):
            self.show_message('Error', 'Todos los campos obligatorios son requeridos')
            return

        if not any([self.ids.animal_type_gato.active, self.ids.animal_type_perro.active]):
            self.show_message('Error', 'Seleccione el tipo de mascota')
            return

        if not any([self.ids.sex_macho.active, self.ids.sex_hembra.active]):
            self.show_message('Error', 'Seleccione el sexo de la mascota')
            return

        # Validar latitud y longitud
        if not latitude or not longitude:
            self.show_message('Error', 'Las coordenadas de latitud y longitud son requeridas')
            return

        try:
            latitude = float(latitude)  # Convertir a número flotante
            longitude = float(longitude)  # Convertir a número flotante
        except ValueError:
            self.show_message('Error', 'Las coordenadas deben ser números válidos')
            return

        # Datos para enviar en el cuerpo de la solicitud
        data = {
            'pet_name': name,
            'type': animal_type,
            'sex': sex,
            'color': color,
            'lost_date': datetime.now().isoformat(),
            'lost_city': city,
            'lost_location': address,
            'lost_latitude': latitude,
            'lost_longitude': longitude,
            'description': f"Mascota perdida en {city}",
            'has_name_tag': has_tag,
            'photo_url': self.get_image_base64(image_path) if image_path else None  # La imagen es opcional
        }

        # Cabecera de la solicitud
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_jwt_token()}'  # Implementa get_jwt_token según tu manejo de autenticación
        }

        # Realizar la solicitud
        UrlRequest(
            'http://localhost:5000/api/v1/pets/create',
            req_headers=headers,
            req_body=json.dumps(data),
            on_success=self.on_success,
            on_failure=self.on_failure,
            on_error=self.on_error
        )

    def get_jwt_token(self):
        try:
            user_data_path = os.path.join(os.path.dirname(__file__), 'user_data.json')
            
            with open(user_data_path, 'r') as file:
                user_data = json.load(file)
                
            if 'user_session' in user_data and 'token' in user_data['user_session']:
                return user_data['user_session']['token']
            else:
                self.show_message('Error', 'No hay sesión activa. Por favor, inicie sesión.')
                return None
                
        except FileNotFoundError:
            self.show_message('Error', 'No se encontró información de sesión. Por favor, inicie sesión.')
            return None
        except json.JSONDecodeError:
            self.show_message('Error', 'Error al leer la información de sesión.')
            return None
        except Exception as e:
            self.show_message('Error', f'Error inesperado: {str(e)}')
            return None

def show_error( message):
    popup = Popup(
        title='Error', 
        content=MDLabel(
            text=message, 
            halign='center',
            theme_text_color='Error'
        ),
        size_hint=(0.8, 0.2),  # Tamaño más pequeño
        title_color=(1, 0, 0, 1),  # Color rojo para el título
    )
    popup.open()

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
                
        except requests.exceptions.ConnectionError as e:
            # para debug
            print(f"Error de conexión: {e}")
            return False, f"Hubo un error de conexión al iniciar sesión"
        
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

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
                
        except requests.exceptions.ConnectionError as e:
            # para debug
            print(f"Error de conexión: {e}")
            return False, f"Hubo un error de conexión al registrar"
        
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

        saber_mas_button = MDFillRoundFlatButton(
            text="Saber más",
            pos_hint={"center_x": 0.5},
            on_release=self.open_url  # Enlaza el evento al método
        )
        self.add_widget(saber_mas_button)

    def open_url(self, instance):
        # Redirige al navegador con la URL de localhost:5001 o el front hosteado
        webbrowser.open("http://localhost:5001/#lostPets")


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