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

@app.route('/cuenta', methods=['GET'])
def cuenta():
    return render_template('account.html')


@app.route('/')
def index():
    ctx = {
        'pets': pets_service.get_pets()
    }
    return render_template('index.html', **ctx)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
