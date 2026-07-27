import streamlit as st
from utils.api import chat_with_ai, add_to_cart, add_to_wishlist


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

                    st.markdown(
                        """
                        <div style="border:1px solid #E2E8F0; border-radius:16px; padding:16px; margin-bottom:16px; background:#ffffff;">
                        """,
                        unsafe_allow_html=True,
                    )

                    st.write(product["name"])

                    st.write(f"₹{product.get('price', 0)}")

                    st.write(f"⭐ {product.get('rating', 0)}")

                    if st.button(
                        "View Product",
                        key=f"ai_view_{product['id']}"
                    ):

                        st.session_state["selected_product"] = product["id"]

                        st.session_state["page"] = "product_details"

                        st.rerun()

                    c1, c2 = st.columns([1, 1])

                    with c1:
                        if st.button(
                            "❤️ Wishlist",
                            key=f"ai_wish_{product['id']}"
                        ):
                            result = add_to_wishlist(product["id"])
                            if isinstance(result, dict) and result.get("message"):
                                st.success(result["message"])
                            elif isinstance(result, dict) and result.get("detail"):
                                st.error(result["detail"])
                            elif isinstance(result, dict) and result.get("error"):
                                st.error(result["error"])
                            else:
                                st.error("Unable to add to wishlist.")

                    with c2:
                        if st.button(
                            "🛒 Add to Cart",
                            key=f"ai_cart_{product['id']}"
                        ):
                            result = add_to_cart(product["id"], 1)
                            if isinstance(result, dict) and result.get("message"):
                                st.success(result["message"])
                            elif isinstance(result, dict) and result.get("detail"):
                                st.error(result["detail"])
                            elif isinstance(result, dict) and result.get("error"):
                                st.error(result["error"])
                            else:
                                st.error("Unable to add to cart.")

                    st.markdown("</div>", unsafe_allow_html=True)