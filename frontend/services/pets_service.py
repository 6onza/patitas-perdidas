from .api_config import get

def get_pets():
    return get('pets', {'status': 'lost'})
