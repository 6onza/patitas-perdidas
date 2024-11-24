from flask import Flask, jsonify, request, redirect
import config
from datetime import datetime, timedelta
from helpers.dates import serialize_dates
from flask_cors import CORS
import mysql.connector
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import secrets
import hashlib
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)

# SMTP Configuración
app.secret_key = os.getenv('APP_SECRET_KEY')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
jwt = JWTManager(app)

# Configuración de CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5001", "http://127.0.0.1:5001", 'http://localhost:5001/login'],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

# Configuración desde config.py
app.config['DEBUG'] = config.DEBUG

# Función para obtener conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_CONFIG['MYSQL_HOST'],
        user=config.DB_CONFIG['MYSQL_USER'],
        password=config.DB_CONFIG['MYSQL_PASSWORD'],
        database=config.DB_CONFIG['MYSQL_DB']
    )

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
   
    if not username or not password:
        return jsonify({'error': 'Nombre de usuario y contraseña son requeridos'}), 400
   
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT id, username, password_hash FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
   
        if not user:
            return jsonify({'error': 'Nombre de usuario o contraseña inválidos'}), 400
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        if hashed_password == user['password_hash']:
            access_token = create_access_token(identity={
                'user_id': user['id'],
                'username': user['username']
            })
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Nombre de usuario o contraseña inválidos'}), 400
    
    except Exception as e:
        print(f"Error de inicio de sesión: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    
    if not username or not password or not name or not phone:
        return jsonify({'error': 'Nombre de usuario, contraseña, nombre y teléfono son requeridos'}), 400
    
    try:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password_hash, name, phone) VALUES (%s, %s, %s, %s)',
                    (username, hashed_password, name, phone))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    
    except Exception as e:
        print(f"Error de registro: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/v1/pets', methods=['GET'])
def get_pets():
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM lost_pets')
        pets_list = cur.fetchall()
        
        # Serializamos las fechas
        for pet in pets_list:
            if 'lost_date' in pet and pet['lost_date']:
                pet['lost_date'] = serialize_dates(pet['lost_date'])
            if 'created_at' in pet and pet['created_at']:
                pet['created_at'] = serialize_dates(pet['created_at'])
            if 'lost_time' in pet and pet['lost_time']:
                pet['lost_time'] = serialize_dates(pet['lost_time'])
        
        cur.close()
        conn.close()
        return jsonify(pets_list)
    except mysql.connector.Error as e:
        app.logger.error(f"Database error in get_pets: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in get_pets: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred'}), 500

@app.route('/api/v1/pets', methods=['POST'])
def add_pet():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO lost_pets (user_id, pet_name, type, breed, color, lost_date, 
                               lost_location, lost_latitude, lost_longitude, 
                               description, photo_url, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['user_id'], data['pet_name'], data['type'], data.get('breed'), data['color'],
        data['lost_date'], data['lost_location'], data['lost_latitude'],
        data['lost_longitude'], data['description'], data.get('photo_url'), data.get('status', 'perdido')
    )
    cur.execute(query, values)
    conn.commit()
    pet_id = cur.lastrowid
    cur.close()
    conn.close()

    data['id'] = pet_id  
    return jsonify(data), 201

@app.route('/api/v1/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM lost_pets WHERE id = %s', (pet_id,))
    pet = cur.fetchone()
    cur.close()
    conn.close()
    
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify(pet)

@app.route('/api/v1/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    data = request.get_json()
    
    query = "UPDATE lost_pets SET "
    values = []
    for key, value in data.items():
        query += f"{key} = %s, "
        values.append(value)
    
    query = query.rstrip(', ')
    query += " WHERE id = %s"
    values.append(pet_id)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, tuple(values))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Pet updated successfully'}), 200

@app.route('/api/v1/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM lost_pets WHERE id = %s', (pet_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Pet deleted successfully'}), 204

@app.route('/api/v1/pets/search', methods=['GET'])
def search_pet():
    try:
        type = request.args.get('type', '').lower()
        sex = request.args.get('sex', '').lower()
        has_tag = request.args.get('has_tag', '')
        city = request.args.get('city', '').strip()
        address = request.args.get('address', '').strip()
        
        ALLOWED_TYPES = ['cat', 'dog']
        ALLOWED_SEXES = ['male', 'female']
        
        query = '''
        SELECT 
            id, pet_name, type, sex, breed, color, 
            lost_date, lost_location, description, 
            has_name_tag, status
        FROM lost_pets 
        WHERE 1=1
        '''
        
        params = []
        
        if type and type in ALLOWED_TYPES:
            query += ' AND type = %s'
            params.append(type)
        elif type:
            return jsonify({'error': 'Invalid pet type'}), 400
        
        if sex and sex in ALLOWED_SEXES:
            query += ' AND sex = %s'
            params.append(sex)
        elif sex:
            return jsonify({'error': 'Invalid sex'}), 400
        
        if has_tag == 'True':
            query += ' AND has_name_tag = 1'
        elif has_tag == 'False':
            query += ' AND has_name_tag = 0'
        elif has_tag:
            return jsonify({'error': 'Invalid name tag filter'}), 400
        
        if city:
            if len(city) > 100:
                return jsonify({'error': 'City name too long'}), 400
            query += ' AND lost_location LIKE %s'
            params.append(f'%{city}%')
        
        if address:
            if len(address) > 255:
                return jsonify({'error': 'Address too long'}), 400
            query += ' AND lost_location LIKE %s'
            params.append(f'%{address}%')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        if params:
            cur.execute(query, tuple(params))
        else:
            cur.execute(query)
        
        pets_list = cur.fetchall()
        
        for pet in pets_list:
            if pet['lost_date']:
                pet['lost_date'] = serialize_dates(pet['lost_date'])
        
        cur.close()
        conn.close()
        
        return jsonify(pets_list)
    
    except mysql.connector.Error as e:
        app.logger.error(f"Database error in pet search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in pet search: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred'}), 500

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        msg_user = MIMEText(
            f"Hola {name},\n\nHemos recibido tu mensaje correctamente. "
            "Nos pondremos en contacto con vos en breve.\n\nGracias por escribirnos.\n\nSaludos,\nEquipo Patitas Perdidas"
        )
        msg_user["From"] = "patitas.perdidas.contacto@gmail.com"
        msg_user["To"] = email
        msg_user["Subject"] = "Mensaje recibido - Patitas Perdidas"
       
        servidor.sendmail(SMTP_USERNAME, email, msg_user.as_string())

        msg_admin = MIMEText(
            f"Correo recibido de: {email}\nNombre: {name}\n\n{message}"
        )
        msg_admin["From"] = "patitas.perdidas.contacto@gmail.com"
        msg_admin["To"] = "patitas.perdidas.contacto@gmail.com"
        msg_admin["Subject"] = f"Nuevo mensaje recibido"

        servidor.sendmail(SMTP_USERNAME, SMTP_USERNAME, msg_admin.as_string())
        servidor.quit()
        return redirect("https://patitas-perdidas.vercel.app/")

if __name__ == '__main__':
    app.run()