# seed data
pets = [
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

# la logica de estas funciones se reemplazara por las consultas a la base de datos
def get_all_pets():
    """Retorna todas las mascotas"""
    return pets

def find_pet_by_id(pet_id):
    """Busca una mascota por su ID"""
    return next((pet for pet in pets if pet['id'] == pet_id), None)

def add_new_pet(pet_data):
    """Agrega una nueva mascota"""
    pets.append(pet_data)
    return pet_data

def update_existing_pet(pet_id, updated_data):
    """Actualiza los datos de una mascota existente"""
    pet = find_pet_by_id(pet_id)
    if pet:
        pet.update(updated_data)
    return pet

def delete_pet(pet_id):
    """Elimina una mascota"""
    pet = find_pet_by_id(pet_id)
    if pet:
        pets.remove(pet)
    return pet