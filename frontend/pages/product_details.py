import streamlit as st
from utils.api import (
    get_products,
    add_to_cart,
    add_to_wishlist,
    get_reviews,
    add_review,
    get_recommendations,
)


def product_details_page(product_id=None):

    st.title("📦 Product Details")

    products = get_products()

    if not products:
        st.warning("No products found.")
        return

    product = products[0]

    if product_id is not None:
        for p in products:
            if p.get("id") == product_id:
                product = p
                break

    image = product.get("image", "")
    name = product.get("name", "Unknown Product")
    price = product.get("price", 0)
    rating = product.get("rating", 4.8)

    description = product.get(
        "description",
        "Premium electronic product powered by ElectroHub AI."
    )

    brand = product.get("brand", "Unknown")
    category = product.get("category", "Electronics")

    old_price = round(price * 1.20, 2)

    left, right = st.columns([1, 1])

    with left:

        try:

            valid_image = (
            isinstance(image, str)
            and image.strip() != ""
            and image.startswith(("http://", "https://"))
            and "There are too many imageURLs objects" not in image
    )

            if valid_image:

                st.image(
                    image,
                    width="stretch"
                )

            else:

                st.image(
                    "https://via.placeholder.com/600x500?text=No+Image",
                    width="stretch"
                )

        except Exception:

            st.image(
                "https://via.placeholder.com/600x500?text=No+Image",
                width="stretch"
            )

    with right:

        st.markdown(f"## {name}")

        st.write(f"⭐ {rating} / 5")

        st.markdown(
            f"""
            <h2 style="color:#FB7185;">
                ₹{price}
                <span style="
                    color:#94A3B8;
                    font-size:22px;
                    text-decoration:line-through;">
                    ₹{old_price}
                </span>
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Brand")
        st.write(brand)

        st.markdown("### Category")
        st.write(category)

        st.markdown("### Availability")
        st.success("✅ In Stock")

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "❤️ Add to Wishlist",
                key=f"detail_wishlist_{product['id']}",
                use_container_width=True,
            ):

                result = add_to_wishlist(product["id"])

                if "message" in result:
                    st.success(result["message"])

                elif "detail" in result:
                    st.error(result["detail"])

                elif "error" in result:
                    st.error(result["error"])

                else:
                    st.error("Unable to add to wishlist.")

        with col2:

            if st.button(
                "🛒 Add to Cart",
                key=f"detail_cart_{product['id']}",
                use_container_width=True,
            ):

                result = add_to_cart(
                    product["id"],
                    quantity
                )

                if "message" in result:
                    st.success("Added to Cart 🛒")

                elif "detail" in result:
                    st.error(result["detail"])

                elif "error" in result:
                    st.error(result["error"])

                else:
                    st.error("Unable to add product to cart.")

        if st.button(
            "⚡ Buy Now",
            use_container_width=True,
        ):

            result = add_to_cart(
                product["id"],
                quantity
            )

            if "message" in result:

                st.session_state["page"] = "checkout"

                st.rerun()

            else:

                st.error("Unable to continue.")

    st.divider()

    st.subheader("📝 Description")
    st.write(description)

    st.divider()

    st.subheader("📋 Specifications")

    specs = {
        "Brand": brand,
        "Category": category,
        "Rating": rating,
        "Price": f"₹{price}",
        "Availability": "In Stock",
    }

    for key, value in specs.items():
        st.write(f"**{key}:** {value}")

    st.divider()

    st.subheader("⭐ Reviews")

    reviews = get_reviews(product["id"])

    if not reviews:

        st.info("No reviews yet.")

    else:

        for review in reviews:

            with st.container(border=True):

                st.write(f"⭐ {review['rating']} / 5")

                st.write(review["comment"])

    st.divider()

    st.subheader("✍ Write a Review")

    review_rating = st.slider(
        "Your Rating",
        1,
        5,
        5
    )

    comment = st.text_area(
        "Your Review"
    )

    if st.button(
        "Submit Review",
        use_container_width=True
    ):

        result = add_review(
            product["id"],
            review_rating,
            comment
        )

        if "message" in result:

            st.success(result["message"])

            st.rerun()

        elif "detail" in result:

            st.error(result["detail"])

        elif "error" in result:

            st.error(result["error"])

        else:

            st.error("Unable to submit review.")

    st.divider()

    st.subheader("🤖 Recommended For You")

    recommended = get_recommendations(product["id"])

    if not recommended:
        st.info("No recommendations available.")
    else:
        unique_ids = set()
        filtered = []

        for item in recommended:
            item_id = item.get("id")
            if item_id and item_id != product["id"] and item_id not in unique_ids:
                unique_ids.add(item_id)
                filtered.append(item)

        if not filtered:
            st.info("No new recommendations available.")
        else:
            for i in range(0, len(filtered), 4):
                cols = st.columns(4)

                for col, item in zip(cols, filtered[i:i+4]):
                    with col:
                        with st.container():
                            st.markdown(
                                """
                                <div style="border:1px solid #E2E8F0; border-radius:16px; padding:12px; margin-bottom:12px; background:#ffffff;">
                                """,
                                unsafe_allow_html=True,
                            )

                            image = item.get("image", "")

                            if image and image.startswith(("http://", "https://")):
                                st.image(image, width=180)
                            else:
                                st.image(
                                    "https://via.placeholder.com/180x180?text=No+Image",
                                    width=180
                                )

                            st.markdown(f"**{item.get('name', 'Unknown Product')[:40]}**")
                            st.write(f"₹{item.get('price', 0)}")
                            st.write(f"⭐ {item.get('rating', 0)}")

                            if st.button(
                                "View",
                                key=f"rec_view_{item['id']}"
                            ):
                                st.session_state["selected_product"] = item["id"]
                                st.session_state["page"] = "product_details"
                                st.rerun()

                            c1, c2 = st.columns([1, 1])

                            with c1:
                                if st.button(
                                    "❤️ Wishlist",
                                    key=f"rec_wish_{item['id']}"
                                ):
                                    result = add_to_wishlist(item["id"])
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
                                    key=f"rec_cart_{item['id']}"
                                ):
                                    result = add_to_cart(item["id"], 1)
                                    if isinstance(result, dict) and result.get("message"):
                                        st.success(result["message"])
                                    elif isinstance(result, dict) and result.get("detail"):
                                        st.error(result["detail"])
                                    elif isinstance(result, dict) and result.get("error"):
                                        st.error(result["error"])
                                    else:
                                        st.error("Unable to add product to cart.")

                            st.markdown("</div>", unsafe_allow_html=True)

    if __name__ == "__main__":

        product_id = st.session_state.get(
            "selected_product",
            None
        )

        product_details_page(product_id)