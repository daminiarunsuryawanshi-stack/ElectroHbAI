import requests
import streamlit as st


BASE_URL = "https://electrohbai-1.onrender.com"
BASE_URL = API_URL


# ==========================
# PRODUCT API
# ==========================

def get_products():

    url = f"{BASE_URL}/products/"

    print("=" * 50)
    print("REQUEST URL:", url)

    try:

        response = requests.get(
            url,
            timeout=30
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR RESPONSE:", response.text)
            return []

        data = response.json()

        print("TOTAL PRODUCTS:", len(data))

        return data


    except Exception as e:

        print("EXCEPTION:", repr(e))
        return []



def get_products(search=None, category=None):

    params = {}

    if search:
        params["search"] = search

    if category:
        params["category"] = category

    try:

        response = requests.get(
            f"{BASE_URL}/products/",
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception as e:
        print(e)
        return []


# ==========================
# AUTH TOKEN
# ==========================

def get_headers():

    token = st.session_state.get("token")

    print("TOKEN:", token)

    if token:
        return {
            "Authorization": f"Bearer {token}"
        }

    return {}

# ==========================
# WISHLIST API
# ==========================

def get_wishlist():

    try:

        response = requests.get(
            f"{BASE_URL}/wishlist/",
            headers=get_headers(),
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return []


    except Exception:

        return []



def add_to_wishlist(product_id):

    headers = get_headers()
    if not headers:
        return {"detail": "Please login to add items to your wishlist."}

    try:

        response = requests.post(
            f"{BASE_URL}/wishlist/",
            json={
                "product_id": product_id
            },
            headers=headers
        )

        return response.json()


    except Exception as e:

        return {
            "error": str(e)
        }



def remove_from_wishlist(product_id):

    try:

        response = requests.delete(
            f"{BASE_URL}/wishlist/{product_id}",
            headers=get_headers()
        )

        return response.json()


    except Exception as e:

        return {
            "error": str(e)
        }



# ==========================
# CART API
# ==========================

def get_cart():

    try:

        response = requests.get(
            f"{BASE_URL}/cart/",
            headers=get_headers(),
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return []


    except Exception:

        return []



def add_to_cart(product_id, quantity=1):

    headers = get_headers()
    if not headers:
        return {"detail": "Please login to add items to your cart."}

    try:

        print("HEADERS:", headers)

        response = requests.post(
            f"{BASE_URL}/cart/add",
            json={
                "product_id": product_id,
                "quantity": quantity
            },
            headers=headers,
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        return response.json()


    except Exception as e:

        return {
            "error": str(e)
        }


def remove_from_cart(cart_id):

    try:

        response = requests.delete(
            f"{BASE_URL}/cart/{cart_id}",
            headers=get_headers()
        )

        return response.json()


    except Exception as e:

        return {
            "error": str(e)
        }



def update_cart(cart_id, quantity):

    try:

        response = requests.put(
            f"{BASE_URL}/cart/{cart_id}?quantity={quantity}",
            headers=get_headers()
        )

        return response.json()


    except Exception as e:

        return {
            "error": str(e)
        }
    
def place_order(shipping_address, coupon_code=""):

    try:

        response = requests.post(
            f"{BASE_URL}/orders/",
            json={
                "shipping_address": shipping_address,
                "coupon_code": coupon_code
            },
            headers=get_headers()
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }
    
def get_orders():

    try:

        response = requests.get(
            f"{BASE_URL}/orders/",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception:
        return []
    
def get_reviews(product_id):

    try:

        response = requests.get(
            f"{BASE_URL}/reviews/{product_id}"
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception:

        return []



def add_review(product_id, rating, comment):

    try:

        response = requests.post(
            f"{BASE_URL}/reviews/",
            json={
                "product_id": product_id,
                "rating": rating,
                "comment": comment
            },
            headers=get_headers()
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }
    
def get_admin_dashboard():

    try:

        response = requests.get(
            f"{BASE_URL}/admin/dashboard",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()

        return {}

    except Exception:
        return {}
    
def get_invoice(order_id):

    try:

        response = requests.get(
            f"{BASE_URL}/invoice/{order_id}",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()

        return {}

    except Exception:

        return {}
    
def get_recommendations(product_id):

    try:

        url = f"{BASE_URL}/recommendation/{product_id}"
        print("REQUESTING RECOMMENDATIONS URL:", url)
        response = requests.get(
            url,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception:

        return []
    
def chat_with_ai(message):

    try:

        response = requests.post(
            f"{BASE_URL}/assistant/chat",
            json={
                "message": message
            }
        )

        if response.status_code == 200:
            return response.json()

        return {
            "reply": "Something went wrong.",
            "products": []
        }

    except Exception as e:

        return {
            "reply": str(e),
            "products": []
        }
    
def make_payment(order_id):

    try:

        response = requests.post(
            f"{BASE_URL}/payments/",
            json={
                "order_id": order_id,
                "payment_method": "Demo QR Payment"
            },
            headers=get_headers()
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }