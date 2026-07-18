import streamlit as st

from utils.api import make_payment


def payment_page():

    st.title("💳 Secure Payment")

    order_id = st.session_state.get("order_id")
    amount = st.session_state.get("final_total", 0)

    if order_id is None:

        st.error("No order found.")

        return

    st.success("Scan the QR Code below to complete your payment.")

    st.image(
        "assets/upi_qr.png",
        width=320
    )

    st.divider()

    st.subheader("📄 Payment Details")

    st.write(f"**Order ID:** {order_id}")

    st.write(f"**Amount to Pay:** ₹{amount}")

    st.markdown("### 🏦 UPI ID")

    st.code("77569493551@ipb")

    st.info(
        "After completing the payment using any UPI app, click the button below."
    )

    if st.button(
        "✅ I Have Paid",
        use_container_width=True
    ):

        result = make_payment(order_id)

        if "message" in result:

            st.balloons()

            st.success("🎉 Payment Successful!")

            st.success(
                f"Transaction ID: {result['transaction_id']}"
            )

            st.session_state["page"] = "orders"

            st.rerun()

        elif "detail" in result:

            st.error(result["detail"])

        elif "error" in result:

            st.error(result["error"])

        else:

            st.error("Payment Failed.")