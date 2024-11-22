from .api_config import get, post, put, delete

def get_pets():
    return get('pets')

def get_pet_by_id(pet_id):
    return get(f'pets/{pet_id}')

def add_pet(pet):
    return post('pets', pet)

def update_pet(pet):
    return put(f'pets/{pet["id"]}', pet)

def delete_pet(pet_id):
    return delete(f'pets/{pet_id}')

# todo: se podria agregar que se muestren mensajes de error en caso de que no se pueda realizar la operacion