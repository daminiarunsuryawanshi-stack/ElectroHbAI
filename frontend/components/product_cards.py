import streamlit as st
from utils.api import get_products, add_to_wishlist, add_to_cart

def show_products(search=None, category=None):

    st.markdown("""
    ## 🔥 Featured Products

    Discover our best electronics selected by AI.
    """)

    products = get_products(search=search)

# Category Filter
    if category:

        keyword_map = {
        "Mobile": [
            "iphone", "phone", "cell", "mobile",
            "galaxy", "lg", "motorola", "htc",
            "nokia", "pixel", "smartphone"
        ],

        "Laptop": [
            "laptop", "notebook", "macbook",
            "workstation", "chromebook", "pc",
            "computer", "surface", "thinkpad",
            "dell", "hp", "lenovo", "asus", "acer"
        ],

        "Audio": [
            "headphone", "headphones",
            "earbud", "earbuds",
            "speaker", "speakers",
            "microphone", "audio",
            "bluetooth", "beats",
            "sony", "bose", "sennheiser"
        ],

        "Watch": [
            "watch",
            "smartwatch",
            "apple watch",
            "fitbit",
            "garmin",
            "wearable"
        ],

        "Gaming": [
            "gaming",
            "game",
            "xbox",
            "playstation",
            "ps4",
            "ps5",
            "nintendo",
            "switch",
            "controller"
        ]
    }

        keywords = keyword_map.get(category, [])

        filtered = []

        for product in products:

            text = (
                product.get("name", "") + " " +
                product.get("description", "")
            ).lower()

            if any(word in text for word in keywords):
                filtered.append(product)

        products = filtered

    if not products:
        st.warning("No products found.")
        return

    # Remove duplicate product names
    seen = set()
    unique_products = []

    for product in products:

        name = product.get("name", "")

        if name not in seen:
            seen.add(name)
            unique_products.append(product)

    if search:
        products = unique_products
    else:
        products = unique_products

    # Display products
    for i in range(0, len(products), 3):

        cols = st.columns(3)

        for col, product in zip(cols, products[i:i + 3]):

            with col:

                with st.container(border=True):

                    image = product.get("image", "")

                    try:

                        valid_image = (
                            isinstance(image, str)
                            and image.strip() != ""
                            and image.startswith(("http://", "https://"))
                            and "There are too many imageURLs objects" not in image
                        )

                        if valid_image:
                            st.image(image, width=220)
                        else:
                            st.image(
                                "https://via.placeholder.com/220x220?text=No+Image",
                                width=220
                            )

                    except Exception:

                        st.image(
                            "https://via.placeholder.com/220x220?text=No+Image",
                            width=220
                        )

                    name = product.get("name", "Unknown Product")

                    if len(name) > 55:
                        name = name[:55] + "..."

                    st.markdown(f"### {name}")

                    rating = product.get("rating", 4.8)
                    st.write(f"⭐ {rating}")

                    price = product.get("price", 0)
                    old_price = round(price * 1.20, 2)

                    st.markdown(
                        f"""
                        <h3 style="color:#FB7185;">
                            ₹{price}
                            <span style="
                                color:gray;
                                font-size:18px;
                                text-decoration:line-through;
                            ">
                                ₹{old_price}
                            </span>
                        </h3>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "🔍 View Details",
                        key=f"view_{product['id']}",
                        use_container_width=True,
                    ):
                        st.session_state["selected_product"] = product["id"]
                        st.session_state["page"] = "product_details"
                        st.rerun()

                    c1, c2 = st.columns(2)

                    with c1:

                        if st.button(
                            "❤️ Wishlist",
                            key=f"wish_{product['id']}",
                            use_container_width=True,
                        ):
                            add_to_wishlist(product["id"])
                            st.success("Added to Wishlist ❤️")

                    with c2:

                        if st.button(
                            "🛒 Cart",
                            key=f"cart_{product['id']}",
                            use_container_width=True,
                        ):

                            result = add_to_cart(product["id"], 1)

                            if "message" in result:
                                st.success("Added to Cart 🛒")
                            else:
                                st.error(
                                    result.get(
                                        "detail",
                                        "Something went wrong"
                                    )
                                )