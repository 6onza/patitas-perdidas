import requests

base_url = "http://127.0.0.1:5000/api/v1" # URL de la API

def get(endpoint, params=None):
    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params)
    return response.json()

def post(endpoint, data=None):
    url = f"{base_url}/{endpoint}"
    response = requests.post(url, json=data)
    return response.json()

def put(endpoint, data=None):
    url = f"{base_url}/{endpoint}"
    response = requests.put(url, json=data)
    return response.json()

def delete(endpoint):
    url = f"{base_url}/{endpoint}"
    response = requests.delete(url)
    return response.json()
