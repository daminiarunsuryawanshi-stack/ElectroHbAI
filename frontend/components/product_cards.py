import streamlit as st
from utils.api import (
    get_products,
    add_to_wishlist,
    add_to_cart
)


def show_products(search=None, category=None):

    st.markdown("""
    ## 🔥 Featured Products

    Discover our best electronics selected by AI.
    """)

    products = get_products(search=search)

    # Debug: show how many products were loaded
    try:
        st.write(f"DEBUG: loaded {len(products)} products")
    except Exception:
        st.write("DEBUG: products could not be counted")

    # ---------------- CATEGORY FILTER ---------------- #

    if category:

        keyword_map = {

            "Mobile": [
                "iphone", "phone", "cell", "mobile",
                "galaxy", "lg", "motorola", "htc",
                "nokia", "pixel", "smartphone"
            ],

            "Laptop": [
                "laptop", "notebook", "macbook",
                "workstation", "chromebook",
                "computer", "surface", "thinkpad",
                "dell", "hp", "lenovo", "asus", "acer"
            ],

            "Audio": [
                "headphone", "headphones",
                "speaker", "speakers",
                "earbuds", "earbud",
                "audio", "bluetooth",
                "bose", "sony"
            ],

            "Watch": [
                "watch",
                "smartwatch",
                "apple watch",
                "fitbit",
                "garmin"
            ],

            "Gaming": [
                "gaming",
                "game",
                "xbox",
                "playstation",
                "ps5",
                "ps4",
                "switch"
            ]
        }

        keywords = keyword_map.get(category, [])

        filtered = []

        for product in products:

            text = (
                product.get("name", "")
                + " " +
                product.get("description", "")
            ).lower()

            if any(word in text for word in keywords):
                filtered.append(product)

        products = filtered

    if not products:

        st.warning("No products found.")

        return
    
    # ---------------- REMOVE DUPLICATES ---------------- #

    seen = set()
    unique_products = []

    for product in products:

        product_id = product.get("id")

        if product_id not in seen:
            seen.add(product_id)
            unique_products.append(product)

    products = unique_products

    # ---------------- PRODUCT GRID ---------------- #

    for row in range(0, len(products), 3):

        cols = st.columns(3, gap="large")

        for col, product in zip(cols, products[row:row + 3]):

            with col:

                with st.container():

                    # ---------- IMAGE ---------- #

                    image = product.get("image", "")

                    valid_image = (
                        isinstance(image, str)
                        and image.strip() != ""
                        and image.startswith(("http://", "https://"))
                        and "There are too many imageURLs objects" not in image
                    )

                    if valid_image:
                        st.markdown(
                            """
                            <style>
                            .product-image{
                                width:100%;
                                height:240px;
                                display:flex;
                                justify-content:center;
                                align-items:center;
                                background:#ffffff;
                                border-radius:15px;
                                overflow:hidden;
                                margin-bottom:10px;
                            }

                            .product-image img{
                                max-width:100%;
                                max-height:220px;
                                object-fit:contain;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown('<div class="product-image">', unsafe_allow_html=True)

                        st.image(
                            image,
                            width=280
                        )

                        st.markdown("</div>", unsafe_allow_html=True)

                    else:

                        st.image(
                            "https://via.placeholder.com/300x300?text=No+Image",
                            width=280
                        )

                    st.write("")

                    # ---------- PRODUCT NAME ---------- #

                    name = product.get("name", "Unknown Product")

                    if len(name) > 60:
                        name = name[:60] + "..."

                    st.markdown(
                        f"""
                        <div style="
                            height:70px;
                            overflow:hidden;
                            font-size:18px;
                            font-weight:700;
                            line-height:1.4;
                        ">
                            {name}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # ---------- RATING ---------- #

                    rating = product.get("rating", 4.5)

                    st.markdown(
                        f"⭐ **{rating} / 5**"
                    )

                    # ---------- PRICE ---------- #

                    price = product.get("price", 0)

                    old_price = round(price * 1.20, 2)

                    st.markdown(
                        f"""
                        <h3 style="color:#FB7185;">
                            ₹{price}
                            <span style="
                                color:gray;
                                font-size:16px;
                                text-decoration:line-through;
                            ">
                                ₹{old_price}
                            </span>
                        </h3>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.write("")

                    # ---------- VIEW DETAILS ---------- #

                    if st.button(
                        "🔍 View Details",
                        key=f"view_{row}_{product['id']}",
                        use_container_width=True
                    ):

                        st.session_state["selected_product"] = product["id"]
                        st.session_state["page"] = "product_details"
                        st.rerun()

                    # ---------- ACTION BUTTONS ---------- #

                    c1, c2 = st.columns(2)

                    with c1:

                        if st.button(
                            "❤️ Wishlist",
                            key=f"wish_{row}_{product['id']}",
                            use_container_width=True
                        ):

                            result = add_to_wishlist(product["id"])

                            if isinstance(result, dict):

                                if result.get("message"):
                                    st.success(result["message"])
                                else:
                                    st.error(
                                        result.get(
                                            "detail",
                                            "Failed to add to wishlist."
                                        )
                                    )

                            else:
                                st.success("Added to Wishlist ❤️")

                    with c2:

                        if st.button(
                            "🛒 Cart",
                            key=f"cart_{row}_{product['id']}",
                            use_container_width=True
                        ):

                            result = add_to_cart(
                                product["id"],
                                1
                            )

                            if isinstance(result, dict):

                                if result.get("message"):
                                    st.success(result["message"])
                                else:
                                    st.error(
                                        result.get(
                                            "detail",
                                            "Failed to add to cart."
                                        )
                                    )

                            else:
                                st.success("Added to Cart 🛒")