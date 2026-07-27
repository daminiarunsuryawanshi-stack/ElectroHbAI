import streamlit as st

from components.navbar import show_navbar
from components.hero import show_hero
from components.search import show_search
from components.product_cards import show_products
from pages.cart import cart_page
from pages.checkout import checkout_page
from pages.orders import orders_page
from pages.payment import payment_page
from pathlib import Path

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="ElectroHub AI",
    page_icon="⚡",
    layout="wide"
)


# ================= LOAD CSS =================


css_file = Path(__file__).parent / "styles" / "style.css"

with open(css_file, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ================= NAVBAR =================

show_navbar()


# ================= PAGE ROUTING =================

if st.session_state.get("page") == "login":

    from pages.login import show_login

    show_login()

    st.stop()



if st.session_state.get("page") == "cart":

    from pages.cart import cart_page

    cart_page()

    st.stop()

if st.session_state.get("page") == "checkout":

    from pages.checkout import checkout_page

    checkout_page()

    st.stop()

if st.session_state.get("page") == "orders":

    from pages.orders import orders_page

    orders_page()

    st.stop()
if st.session_state.get("page") == "product_details":

    from pages.product_details import product_details_page

    product_details_page(
        st.session_state.get("selected_product")
    )

    st.stop()

if st.session_state.get("page") == "wishlist":

    from pages.wishlist import wishlist_page

    wishlist_page()

    st.stop()

if st.session_state.get("page") == "profile":

    from pages.profile import profile_page

    profile_page()

    st.stop()

if st.session_state.get("page") == "admin":

    from pages.admin import admin_page

    admin_page()

    st.stop()

if st.session_state.get("page") == "assistant":

    from pages.assistant import assistant_page

    assistant_page()

    st.stop()

if st.session_state.get("page") == "product":

    from pages.product_details import product_details_page

    product_details_page(
        st.session_state.get("selected_product")
    )

    st.stop()
    
if st.session_state.get("page") == "payment":
    payment_page()
    st.stop()

# ================= HOME PAGE =================

show_hero()

st.write("")
st.write("")


search, category = show_search()

st.write("")
st.write("")



show_products(
    search=search,
    category=category
)


st.write("")
st.write("")


st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748B;
        padding:40px;
        font-size:16px;
    ">
        © 2026 ElectroHub AI • Smart Shopping Powered by Artificial Intelligence
    </div>
    """,
    unsafe_allow_html=True
)