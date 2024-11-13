from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/static')


app.secret_key = "1xu5rTqT7CT/POBFBsB7GEuPLUd8klo/Pw52q5QK87E="  

@app.route('/')
def index():
    mascotas = {
        "m1": ("no tiene chapa", "macho", "raza", "5 años"), 
        "m2": ("Mumi", "hembra", "mestizo", "2 años"), 
        "m3": ("no tiene chapa", "macho", "raza", "5 años 1 mes"),
        "m4": ("Rambo", "macho", "mestizo", "8 años"),
        "m5": ("Simon", "macho", "raza", "2 años 8 meses"),
        "m6": ("no tiene chapa", "hembra", "raza", "3 años")
    }
    return render_template('index.html', mascotas=mascotas)

@app.route('/enviar_email', methods=['POST'])
def enviar_mail():
    if request.method == "POST":
        nombre = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login("patitas.perdidas.contacto@gmail.com", "tmha xurb ybfn ndsn")  
        
        msg_user = MIMEText(
            f"Hola {nombre},\n\nHemos recibido tu mensaje correctamente. "
            "Nos pondremos en contacto contigo pronto.\n\nGracias por escribirnos.\n\nSaludos,\nEquipo Patitas Perdidas"
        )
        msg_user["From"] = "patitas.perdidas.contacto@gmail.com"
        msg_user["To"] = email
        msg_user["Subject"] = "Confirmación de recepción de mensaje"
       
        servidor.sendmail("patitas.perdidas.contacto@gmail.com", email, msg_user.as_string())

        msg_admin = MIMEText(
            f"Correo recibido de: {email}\nNombre: {nombre}\n\n{message}"
        )
        msg_admin["From"] = "patitas.perdidas.contacto@gmail.com"
        msg_admin["To"] = "patitas.perdidas.contacto@gmail.com"
        msg_admin["Subject"] = "Nuevo mensaje de contacto recibido"

        servidor.sendmail("patitas.perdidas.contacto@gmail.com", "patitas.perdidas.contacto@gmail.com", msg_admin.as_string())
        servidor.quit()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
