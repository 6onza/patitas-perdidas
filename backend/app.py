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

if __name__ == '__main__':
    app.run()