import streamlit as st

from utils.api import (
    get_wishlist,
    remove_from_wishlist,
    add_to_cart,
)


def wishlist_page():

    st.title("❤️ My Wishlist")

    products = get_wishlist()

    if not products:
        st.info("Your wishlist is empty.")
        return

    for product in products:

        col1, col2 = st.columns([1, 3])

        with col1:

            image = product.get("image", "")

            if image:
                st.image(image, width=150)

        with col2:

            st.subheader(product.get("name", "Product"))

            st.write(f"⭐ {product.get('rating', 4.8)}")

            st.markdown(f"### ₹{product.get('price', 0)}")

            c1, c2, c3 = st.columns(3)

            with c1:

                if st.button(
                    "🔍 Details",
                    key=f"details_{product['id']}"
                ):
                    st.session_state["selected_product"] = product["product_id"]
                    st.session_state["page"] = "product_details"
                    st.rerun()

            with c2:

                if st.button(
                    "🛒 Move to Cart",
                    key=f"cart_{product['id']}"
                ):

                    add_to_cart(product["product_id"], 1)
                    st.rerun()

            with c3:

                if st.button(
                    "🗑 Remove",
                    key=f"remove_{product['id']}"
                ):

                    remove_from_wishlist(product["id"])

                    st.success("Removed from Wishlist")

                    st.rerun()