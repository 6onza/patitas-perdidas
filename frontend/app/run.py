from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from services import pets_service

app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/static')

@app.route('/')
def index():
    ctx = {
        'pets' : pets_service.get_pets()
    }
    return render_template('index.html', **ctx)
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)
