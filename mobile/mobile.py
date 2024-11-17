from kivy.app import App
from kivy.uix.webview import WebView

def app_mobile_create():
    webview = WebView(url='') # Aca tenemos que poner la url de la pagina una vez que ya la tengamos lista (con dominio y todo creo)
    app = App()
    app.root = webview
    app.run()

if __name__ == '__main__':
    app_mobile_create()


# Al tener las dependencias instaladas (kivy y buildozer) se va a crear un buildozer.spec donde tambien tenemos que reemplazar parametros con nuestra url y otras cosas