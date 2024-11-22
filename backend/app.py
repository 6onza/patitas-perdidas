from flask import Flask, jsonify, request, redirect
import config
from services.pet_service import find_pet_by_id, add_new_pet, update_existing_pet
from flask_mysqldb import MySQL
from datetime import datetime
from helpers.dates import serialize_dates
from flask_cors import CORS
import MySQLdb

import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)

app.secret_key = "1xu5rTqT7CT/POBFBsB7GEuPLUd8klo/Pw52q5QK87E=" 


CORS(app, resources={
    r"/*": {
        "origins": config.CORS_ORIGIN,
        "methods": config.CORS_ALLOWED_METHODS,
        "allow_headers": config.CORS_ALLOWED_HEADERS,
        "supports_credentials": True
    }
})

# Configuración desde config.py
app.config['DEBUG'] = config.DEBUG

# Configuración de la base de datos desde config.py
app.config.update(config.DB_CONFIG)

mysql = MySQL(app)

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
def send_mail():
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
        return redirect("https://patitas-perdidas.vercel.app/")
    

if __name__ == '__main__':
    app.run()