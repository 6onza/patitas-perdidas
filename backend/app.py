from flask import Flask, jsonify, request
from config import DEBUG
from services.pet_service import get_all_pets, find_pet_by_id, add_new_pet, update_existing_pet

app = Flask(__name__)
app.config['DEBUG'] = DEBUG


@app.route('/pets', methods=['GET'])
def get_pets():
    return jsonify(get_all_pets())

@app.route('/pets', methods=['POST'])
def add_pet():
    new_pet = request.get_json()
    result = add_new_pet(new_pet)
    return jsonify(result), 201

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = find_pet_by_id(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify(pet)

@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    pet = find_pet_by_id(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    updated_data = request.get_json()
    updated_pet = update_existing_pet(pet_id, updated_data)
    return jsonify(updated_pet)

@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet = find_pet_by_id(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    print(str(pet) + " deleted")
    return jsonify(pet), 204

if __name__ == '__main__':
    app.run()