import streamlit as st
from utils.api import get_cart, remove_from_cart, update_cart, get_recommendations, add_to_cart, add_to_wishlist


def cart_page():

    st.title("🛒 Shopping Cart")


    cart_items = get_cart()


    if not cart_items:

        st.info("Your cart is empty.")
        return


    total = 0


    for item in cart_items:


        col1, col2 = st.columns([1, 3])


        with col1:

            image = item.get("image", "")

            if image:

                st.image(
                    image,
                    width=150
                )


        with col2:


            st.subheader(
                item.get(
                    "name",
                    "Product"
                )
            )


            price = item.get(
                "price",
                0
            )


            quantity = item.get(
                "quantity",
                1
            )


            st.write(
                f"💰 Price: ₹{price}"
            )


            new_quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=quantity,
                key=f"qty_{item['id']}"
            )


            if new_quantity != quantity:

                update_cart(
                    item["id"],
                    new_quantity
                )

                st.rerun()



            if st.button(
                "🗑 Remove",
                key=f"remove_{item['id']}"
            ):

                remove_from_cart(
                    item["id"]
                )

                st.rerun()



            total += price * new_quantity


        st.divider()



    st.subheader(
        f"Grand Total : ₹{round(total,2)}"
    )


    if st.button(
    "💳 Proceed to Checkout",
    use_container_width=True
    ):

        st.session_state["page"] = "checkout"

        st.rerun()


    # ============================================
    # SHOW RECOMMENDATIONS FOR CART ITEMS
    # ============================================
    st.divider()
    
    st.subheader("🤖 Recommended Products")
    st.write("Items you might want to add to your cart:")
    
    all_recommendations = []
    recommended_ids = set()
    
    # Debug: show cart items being used for recommendations
    print("CART ITEMS FOR RECOMMENDATIONS:", cart_items)

    # Get recommendations for each item in cart (use product_id, not cart id)
    for item in cart_items:
        try:
            recommended = get_recommendations(item["product_id"])
            if recommended:
                for rec in recommended:
                    # Avoid duplicate recommendations
                    if rec["id"] not in recommended_ids and rec["id"] != item["product_id"]:
                        all_recommendations.append(rec)
                        recommended_ids.add(rec["id"])
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            continue
    
    if all_recommendations:
        # Display recommendations in rows of 4
        for i in range(0, len(all_recommendations), 4):
            cols = st.columns(4)
            for col, rec_item in zip(cols, all_recommendations[i:i+4]):
                with col:
                    st.markdown(
                        """
                        <div style="border:1px solid #E2E8F0; border-radius:16px; padding:16px; margin-bottom:16px; background:#ffffff;">
                        """,
                        unsafe_allow_html=True,
                    )

                    image = rec_item.get("image", "")
                    if image and image.startswith(("http://", "https://")):
                        st.image(image, width=180)
                    else:
                        st.image(
                            "https://via.placeholder.com/180x180?text=No+Image",
                            width=180
                        )

                    st.write(f"**{rec_item.get('name', 'Product')}**")

                    price = rec_item.get("price", 0)
                    rating = rec_item.get("rating", 0)
                    st.write(f"₹{price}")
                    st.write(f"⭐ {rating}")

                    if st.button(
                        "View",
                        key=f"rec_view_{rec_item['id']}"
                    ):
                        st.session_state["selected_product"] = rec_item["id"]
                        st.session_state["page"] = "product_details"
                        st.rerun()

                    c1, c2 = st.columns([1, 1])

                    with c1:
                        if st.button(
                            "❤️ Wishlist",
                            key=f"rec_wish_{rec_item['id']}"
                        ):
                            result = add_to_wishlist(rec_item["id"])
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
                            "➕ Add to Cart",
                            key=f"rec_add_{rec_item['id']}"
                        ):
                            result = add_to_cart(rec_item["id"], 1)
                            if isinstance(result, dict) and result.get("message"):
                                st.success(f"Added {rec_item.get('name', 'Product')} to cart!")
                                st.rerun()
                            elif isinstance(result, dict) and result.get("detail"):
                                st.error(result["detail"])
                            elif isinstance(result, dict) and result.get("error"):
                                st.error(result["error"])
                            else:
                                st.error("Failed to add item to cart")

                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No recommendations available. Keep shopping!")