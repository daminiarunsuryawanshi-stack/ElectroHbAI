import streamlit as st
from utils.api import get_cart, remove_from_cart, update_cart


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