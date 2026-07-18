import streamlit as st
from utils.api import chat_with_ai


def assistant_page():

    st.title("🤖 ElectroHub AI Shopping Assistant")

    st.write("Ask me anything about products.")

    question = st.text_input(
        "Example: Laptop, TV, Samsung, Headphones..."
    )

    if st.button(
        "Search",
        use_container_width=True
    ):

        result = chat_with_ai(question)

        st.success(result["reply"])

        products = result.get("products", [])

        if not products:

            st.info("No matching products found.")

            return

        for i in range(0, len(products), 3):

            cols = st.columns(3)

            for col, product in zip(cols, products[i:i+3]):

                with col:

                    image = product.get("image", "")

                    try:

                        if (
                            image
                            and image.startswith(("http://", "https://"))
                        ):
                            st.image(image, width=200)

                    except Exception:
                        pass

                    st.write(product["name"])

                    st.write(f"₹{product['price']}")

                    st.write(f"⭐ {product['rating']}")

                    if st.button(
                        "View Product",
                        key=f"ai_{product['id']}"
                    ):

                        st.session_state["selected_product"] = product["id"]

                        st.session_state["page"] = "product"

                        st.rerun()