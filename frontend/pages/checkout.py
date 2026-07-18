import streamlit as st
from utils.api import place_order


def checkout_page():

    st.title("💳 Checkout")

    shipping_address = st.text_area(
        "Shipping Address"
    )

    coupon_code = st.text_input(
        "Coupon Code (Optional)"
    )

    if st.button(
        "✅ Place Order",
        use_container_width=True
    ):

        if not shipping_address.strip():

            st.warning(
                "Please enter your shipping address."
            )

            return

        result = place_order(
            shipping_address,
            coupon_code
        )

        if "message" in result:

            st.success(result["message"])

            st.write(
                f"🆔 Order ID: {result['order_id']}"
            )

            st.write(
                f"💰 Original Total: ₹{result['original_total']}"
            )

            st.write(
                f"🎁 Discount: ₹{result['discount']}"
            )

            st.write(
                f"✅ Final Total: ₹{result['final_total']}"
            )

            # Save order details for payment page
            st.session_state["order_id"] = result["order_id"]
            st.session_state["final_total"] = result["final_total"]

            # Go to payment page
            st.session_state["page"] = "payment"

            st.rerun()

        else:

            st.error(
                result.get(
                    "detail",
                    "Something went wrong"
                )
            )