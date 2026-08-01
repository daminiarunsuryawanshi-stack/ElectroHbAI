import requests
from utils.api import BASE_URL

def login(email, password):
    url = f"{BASE_URL}/auth/login"

    data = {
        "username": email,
        "password": password
    }

    response = requests.post(url, data=data)

    print("URL:", url)
    print("Status:", response.status_code)
    print("Response:", response.text)

    return response