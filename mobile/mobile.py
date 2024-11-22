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



# Definir las pantallas
class HomeScreen(Screen):
    pass

class RegistrarMascotaScreen(Screen):
    pass

class MascotasPerdidasScreen(Screen):
    pass

class BuscarMascotasScreen(Screen):
    pass

class SobreNosotrosScreen(Screen):
    pass

class ContactoScreen(Screen):
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
            Snackbar(text="Imagen seleccionada").open()

    def register_pet(self):
        name = self.ids.name.text
        animal_type = self.ids.animal_type.active
        sex = self.ids.sex.active
        has_tag = self.ids.has_tag.active
        color = self.ids.color.text
        city = self.ids.city.text
        address = self.ids.address.text
        image = self.ids.image.text
        
        # Aquí puedes realizar la validación o el procesamiento de los datos
        # Mostrar un mensaje de éxito
        Snackbar(text="Mascota registrada exitosamente!").open()



if __name__ == "__main__":
    PatitasPerdidasApp().run()