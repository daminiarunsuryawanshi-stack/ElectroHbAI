import requests
from utils.api import API_URL


def login(email, password):
    url = f"{API_URL}/auth/login"

    data = {
        "username": email,
        "password": password
    }

    response = requests.post(url, data=data)

    return response