from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='../templates', static_folder='static')

@app.route('/')
def index():
    print("Template folder:", app.template_folder)
    print("Available templates:", os.listdir(app.template_folder))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)