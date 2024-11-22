from flask import Flask, jsonify, request, redirect
import config
from services.pet_service import find_pet_by_id, add_new_pet, update_existing_pet
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from helpers.dates import serialize_dates
from flask_cors import CORS
import MySQLdb
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
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expira en 1 hora
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

# Configuración desde config.py
app.config['DEBUG'] = config.DEBUG

# Configuración de la base de datos desde config.py
app.config.update(config.DB_CONFIG)

mysql = MySQL(app)


@app.route('/api/v1/login', methods=['POST'])
def login():
    # Obtener los datos JSON de la solicitud
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
   
    # Validar que se proporcionen username y password
    if not username or not password:
        return jsonify({'error': 'Nombre de usuario y contraseña son requeridos'}), 400
   
    try:
        # Establecer conexión a la base de datos y buscar el usuario
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, username, password_hash FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
   
        # Verificar si el usuario existe
        if not user:
            return jsonify({'error': 'Nombre de usuario o contraseña inválidos'}), 400
        
        # Verificar la contraseña usando hashing seguro
        user_id, db_username, stored_password = user
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # Comparar contraseñas de forma segura
        if hashed_password == stored_password:
            # Generar token de acceso
            access_token = create_access_token(identity={
                'user_id': user_id,
                'username': db_username
            })
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Nombre de usuario o contraseña inválidos'}), 400
    
    except Exception as e:
        # Manejo de errores generales
        print(f"Error de inicio de sesión: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    
@app.route('/api/v1/register', methods=['POST'])
def register():
    # Obtener los datos JSON de la solicitud
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    
    # Validar que se proporcionen username, password, name y phone
    if not username or not password or not name or not phone:
        return jsonify({'error': 'Nombre de usuario, contraseña, nombre y teléfono son requeridos'}), 400
    
    try:
        # Hash de la contraseña sin salt
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # Establecer conexión a la base de datos y guardar el usuario
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (username, password_hash, name, phone) VALUES (%s, %s, %s, %s)',
                    (username, hashed_password, name, phone))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    
    except Exception as e:
        # Manejo de errores generales
        print(f"Error de registro: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
@app.route('/api/v1/pets', methods=['GET'])
def get_pets():
    try:
        cur = mysql.connection.cursor()
        
        # obtenemos los nombres de las columnas
        cur.execute("DESCRIBE lost_pets")
        columns = [column[0] for column in cur.fetchall()]
        
        # Luego hacemos la consulta de las mascotas
        cur.execute('SELECT * FROM lost_pets')
        rows = cur.fetchall()
        
        # Convertimos las tuplas a diccionarios
        pets_list = []
        for row in rows:
            pet_dict = dict(zip(columns, row))
            
            # Serializamos las fechas
            if 'lost_date' in pet_dict and pet_dict['lost_date']:
                pet_dict['lost_date'] = serialize_dates(pet_dict['lost_date'])
            if 'created_at' in pet_dict and pet_dict['created_at']:
                pet_dict['created_at'] = serialize_dates(pet_dict['created_at'])
            if 'lost_time' in pet_dict and pet_dict['lost_time']:
                pet_dict['lost_time'] = serialize_dates(pet_dict['lost_time'])
                
            pets_list.append(pet_dict)
        
        cur.close()
        return jsonify(pets_list)
    except MySQLdb.Error as e:
        app.logger.error(f"Database error in get_pets: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in get_pets: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred'}), 500


@app.route('/api/v1/pets', methods=['POST'])
def add_pet():
    data = request.get_json()

    cur = mysql.connection.cursor()
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
    mysql.connection.commit()
    pet_id = cur.lastrowid
    cur.close()

    data['id'] = pet_id  
    return jsonify(data), 201

@app.route('/api/v1/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM lost_pets WHERE id = %s', (pet_id,))
    row = cur.fetchone()
    if row is None:
        cur.close()
        return jsonify({'error': 'Pet not found'}), 404
    
    cur.execute("DESCRIBE lost_pets")
    columns = [column[0] for column in cur.fetchall()]
    pet = dict(zip(columns, row))
    cur.close()
    return jsonify(pet)


@app.route('/api/v1/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    data = request.get_json()
    
    query = "UPDATE lost_pets SET "
    values = []
    for key, value in data.items():
        query += f"{key} = %s, "
        values.append(value)
    
    # Removamos la última coma y espacio
    query = query.rstrip(', ')
    query += " WHERE id = %s"
    values.append(pet_id)
    
    cur = mysql.connection.cursor()
    cur.execute(query, tuple(values))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Pet updated successfully'}), 200

@app.route('/api/v1/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM lost_pets WHERE id = %s', (pet_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Pet deleted successfully'}), 204


@app.route('/api/v1/pets/search', methods=['GET'])
def search_pet():
    try:
        # Validate and sanitize input parameters
        type = request.args.get('type', '').lower()
        sex = request.args.get('sex', '').lower()
        has_tag = request.args.get('has_tag', '')
        city = request.args.get('city', '').strip()
        address = request.args.get('address', '').strip()
        
        # Define allowed values
        ALLOWED_TYPES = ['cat', 'dog']
        ALLOWED_SEXES = ['male', 'female']
        
        # Initialize base query with strong filtering
        query = '''
        SELECT 
            id, pet_name, type, sex, breed, color, 
            lost_date, lost_location, description, 
            has_name_tag, status
        FROM lost_pets 
        WHERE 1=1
        '''
        
        # Prepare parameters list for safe query execution
        params = []
        
        # Type validation and filtering
        if type and type in ALLOWED_TYPES:
            query += ' AND type = %s'
            params.append(type)
        elif type:
            # Invalid type provided
            return jsonify({'error': 'Invalid pet type'}), 400
        
        # Sex validation and filtering
        if sex and sex in ALLOWED_SEXES:
            query += ' AND sex = %s'
            params.append(sex)
        elif sex:
            # Invalid sex provided
            return jsonify({'error': 'Invalid sex'}), 400
        
        # Has tag filtering with strict boolean conversion
        if has_tag == 'True':
            query += ' AND has_name_tag = 1'
        elif has_tag == 'False':
            query += ' AND has_name_tag = 0'
        elif has_tag:
            # Invalid has_tag value
            return jsonify({'error': 'Invalid name tag filter'}), 400
        
        # City filtering with length and injection protection
        if city:
            # Limit length to prevent potential DOS
            if len(city) > 100:
                return jsonify({'error': 'City name too long'}), 400
            query += ' AND lost_location LIKE %s'
            params.append(f'%{city}%')
        
        # Address filtering with length and injection protection
        if address:
            # Limit length to prevent potential DOS
            if len(address) > 255:
                return jsonify({'error': 'Address too long'}), 400
            query += ' AND lost_location LIKE %s'
            params.append(f'%{address}%')

        
        # Get database cursor
        cur = mysql.connection.cursor()
        
        # Execute query safely with parameters
        if params:
            cur.execute(query, tuple(params))
        else:
            cur.execute(query)
        
        # Fetch results
        rows = cur.fetchall()
        
        # Predefined column names to prevent descriptor injection
        columns = [
            'id', 'pet_name', 'type', 'sex', 'breed', 'color', 
            'lost_date', 'lost_location', 'description', 
            'has_name_tag', 'status'
        ]
        
        # Convert results to list of dictionaries
        pets_list = []
        for row in rows:
            pet_dict = dict(zip(columns, row))
            
            # Safe date serialization
            if pet_dict['lost_date']:
                pet_dict['lost_date'] = serialize_dates(pet_dict['lost_date'])
            
            pets_list.append(pet_dict)
        
        cur.close()
        
        return jsonify(pets_list)
    
    except MySQLdb.Error as e:
        # Log the error server-side
        app.logger.error(f"Database error in pet search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        # Catch any unexpected errors
        app.logger.error(f"Unexpected error in pet search: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred'}), 500
    
@app.route('/send_email', methods=['POST'])
def send_email():
    '''
    Procesa el formulario de contacto y envia un correo electrónico tanto al usuario que envió el formulario como al administrador del sitio web.
    - Crea dos mensajes de correo electrónico:
    * Mensaje para el usuario: Confirma que su mensaje se ha recibido correctamente y que se pondrán en contacto pronto.
    * Mensaje para el administrador: Contiene la información proporcionada por el usuario (nombre, correo electrónico y mensaje).
    Redirige al usuario a la página de inicio al finalizar.
    '''
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("SMTP_USERNAME:", SMTP_USERNAME)
        print("SMTP_PASSWORD:", SMTP_PASSWORD)

        
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