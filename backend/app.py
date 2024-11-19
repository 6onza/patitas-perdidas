from flask import Flask, jsonify, request
from config import DEBUG, DB_CONFIG
from services.pet_service import find_pet_by_id, add_new_pet, update_existing_pet
from flask_mysqldb import MySQL
from datetime import datetime
from helpers.dates import serialize_dates

app = Flask(__name__)

# Configuración desde config.py
app.config['DEBUG'] = DEBUG

# Configuración de la base de datos desde config.py
app.config.update(DB_CONFIG)

mysql = MySQL(app)

@app.route('/pets', methods=['GET'])
def get_pets():
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


@app.route('/pets', methods=['POST'])
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

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM lost_pets WHERE id = %s', (pet_id,))
    row = cur.fetchone()
    cur.close()

    if row is None:
        return jsonify({'error': 'Pet not found'}), 404

    cur.execute("DESCRIBE lost_pets")
    columns = [column[0] for column in cur.fetchall()]
    pet = dict(zip(columns, row))
    return jsonify(pet)

@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    data = request.get_json()

    cur = mysql.connection.cursor()
    query = """
        UPDATE lost_pets
        SET pet_name = %s, type = %s, breed = %s, color = %s, lost_date = %s, 
            lost_location = %s, lost_latitude = %s, lost_longitude = %s, 
            description = %s, photo_url = %s, status = %s
        WHERE id = %s
    """
    values = (
        data['pet_name'], data['type'], data.get('breed'), data['color'], 
        data['lost_date'], data['lost_location'], data['lost_latitude'], 
        data['lost_longitude'], data['description'], data.get('photo_url'), 
        data['status'], pet_id
    )
    cur.execute(query, values)
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Pet updated successfully'}), 200

@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM lost_pets WHERE id = %s', (pet_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Pet deleted successfully'}), 204

if __name__ == '__main__':
    app.run()