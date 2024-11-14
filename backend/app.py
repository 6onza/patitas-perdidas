from flask import Flask, request, jsonify

app = Flask(__name__)

# seed data
pets: list = [
    {
        "id": 1,
        "name": "Toby",
        "breed": "Golden Retriever",
        "lost_date": "2024-07-01",
        "lost_time": "12:00",
        "lost_description": "Golden retriever de 2 años de edad, color dorado, muy amigable.",
        "lost_contact": "John Doe, 123-456-7890",
        "latitude": "-34.6037",
        "longitude": "-58.3816"
    },
    {
        "id": 2,
        "name": "Bella",
        "breed": "German Shepherd",
        "lost_date": "2024-07-02",
        "lost_time": "12:00",
        "lost_description": "Pastor alemán de 3 años de edad, color blanco, muy juguetona.",
        "lost_contact": "Jane Doe, 123-456-7890",
        "latitude": "-34.6027",
        "longitude": "-58.3906"
    },
    {
        "id": 3,
        "name": "Luna",
        "breed": "Husky Siberiano",
        "lost_date": "2024-07-03",
        "lost_time": "12:00",
        "lost_description": "Husky siberiano de 1 año de edad, color blanco, ojos azules.",
        "lost_contact": "Pepe Picapiedra, 123-456-7890",
        "latitude": "-34.6007",
        "longitude": "-58.3506"
    }
]

@app.route('/pets', methods=['GET'])
def get_pets():
    return jsonify(pets)

@app.route('/pets', methods=['POST'])
def add_pet():
    new_pet = request.get_json()
    pets.append(new_pet)
    
    return jsonify(new_pet), 201

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = next((pet for pet in pets if pet['id'] == pet_id), None)
    
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify(pet)

@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    pet = next((pet for pet in pets if pet['id'] == pet_id), None)
    
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    updated_data = request.get_json()
    pet.update(updated_data)
    
    return jsonify(pet)

if __name__ == '__main__':
    app.run(debug=True)