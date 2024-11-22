from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from services import pets_service

app = Flask(__name__, static_url_path='/static')


app.secret_key = "1xu5rTqT7CT/POBFBsB7GEuPLUd8klo/Pw52q5QK87E="  

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    response = redirect(url_for('index'))
    response.delete_cookie('access_token')
    return response


@app.route('/')
def index():
    access_token = request.cookies.get('access_token')
    print(access_token)
    
    ctx = {
        'pets': pets_service.get_pets()
    }
    return render_template('index.html', **ctx)

@app.route('/enviar_email', methods=['POST'])
def enviar_mail():
    '''
    Procesa el formulario de contacto y envia un correo electrónico tanto al usuario que envió el formulario como al administrador del sitio web.
    - Crea dos mensajes de correo electrónico:
    * Mensaje para el usuario: Confirma que su mensaje se ha recibido correctamente y que se pondrán en contacto pronto.
    * Mensaje para el administrador: Contiene la información proporcionada por el usuario (nombre, correo electrónico y mensaje).
    Redirige al usuario a la página de inicio al finalizar.
    '''
    if request.method == "POST":
        nombre = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login("patitas.perdidas.contacto@gmail.com", "tmha xurb ybfn ndsn")  
        
        msg_user = MIMEText(
            f"Hola {nombre},\n\nHemos recibido tu mensaje correctamente. "
            "Nos pondremos en contacto con vos en breve.\n\nGracias por escribirnos.\n\nSaludos,\nEquipo Patitas Perdidas"
        )
        msg_user["From"] = "patitas.perdidas.contacto@gmail.com"
        msg_user["To"] = email
        msg_user["Subject"] = "Mensaje recibido - Patitas Perdidas"
       
        servidor.sendmail("patitas.perdidas.contacto@gmail.com", email, msg_user.as_string())

        msg_admin = MIMEText(
            f"Correo recibido de: {email}\nNombre: {nombre}\n\n{message}"
        )
        msg_admin["From"] = "patitas.perdidas.contacto@gmail.com"
        msg_admin["To"] = "patitas.perdidas.contacto@gmail.com"
        msg_admin["Subject"] = f"Nuevo mensaje recibido"

        servidor.sendmail("patitas.perdidas.contacto@gmail.com", "patitas.perdidas.contacto@gmail.com", msg_admin.as_string())
        servidor.quit()
        return redirect(url_for('index'))
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)
