import requests

base_url = "https://gvineg.pythonanywhere.com/api/v1" # URL de la API

def get(endpoint, params=None):
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def post(endpoint, data=None):
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def put(endpoint, data=None):
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete(endpoint):
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
