from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/static')

@app.route('/')
def index():
    mascotas: dict ={"m1":("no tiene chapa", "macho", "raza", "5 años"), 
        "m2":("Mumi", "hembra", "mestizo", "2 años"), 
        "m3":("no tiene chapa", "macho", "raza", "5 años 1 mes"),
        "m4":("Rambo", "macho", "mestizo", "8 años" ),
        "m5":("Simon", "macho", "raza", "2 años 8 meses" ),
        "m6":("no tiene chapa", "hembra", "raza", "3 años") }
    return render_template('index.html', mascotas=mascotas)


if __name__ == '__main__':
    app.run(debug=True)
