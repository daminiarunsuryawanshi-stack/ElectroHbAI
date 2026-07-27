import requests
from utils.api import BASE_URL

def login(email, password):
    url = f"{BASE_URL}/auth/login"

    data = {
        "username": email,
        "password": password
    }

    response = requests.post(url, data=data)

    return response