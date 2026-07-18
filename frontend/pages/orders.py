import streamlit as st
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

from utils.api import (
    get_orders,
    get_invoice
)


def create_invoice_pdf(invoice):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>ElectroHub AI Invoice</b>", styles["Title"])
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(f"Invoice No: {invoice['invoice_number']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Customer: {invoice['customer']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Email: {invoice['email']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Shipping Address: {invoice['shipping_address']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Payment Status: {invoice['payment_status']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Transaction ID: {invoice['transaction_id']}", styles["Normal"])
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("<b>Items</b>", styles["Heading2"])
    )

    for item in invoice["items"]:

        elements.append(
            Paragraph(
                f"{item['product']} × {item['quantity']} = ₹{item['subtotal']}",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"<b>Total Amount : ₹{invoice['total_amount']}</b>",
            styles["Heading2"]
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


def orders_page():

    st.title("📦 My Orders")

    orders = get_orders()

    if not orders:

        st.info("No orders found.")

        return

    for order in orders:

        with st.container(border=True):

            st.subheader(f"Order #{order['id']}")

            st.write(f"💰 Total : ₹{order['total_amount']}")

            st.write(f"📍 Address : {order['shipping_address']}")

            st.write(f"📦 Status : {order['status']}")

            if st.button(
                "🧾 View Invoice",
                key=f"invoice_{order['id']}"
            ):

                invoice = get_invoice(order["id"])

                if invoice:

                    st.divider()

                    st.markdown("## 🧾 Invoice")

                    st.write(f"Invoice No : {invoice['invoice_number']}")

                    st.write(f"Customer : {invoice['customer']}")

                    st.write(f"Email : {invoice['email']}")

                    st.write(f"Payment : {invoice['payment_status']}")

                    st.write(f"Transaction : {invoice['transaction_id']}")

                    st.write(f"Address : {invoice['shipping_address']}")

                    st.divider()

                    for item in invoice["items"]:

                        st.write(
                            f"• {item['product']} × {item['quantity']} = ₹{item['subtotal']}"
                        )

                    st.divider()

                    st.subheader(
                        f"Total : ₹{invoice['total_amount']}"
                    )

                    pdf = create_invoice_pdf(invoice)

                    st.download_button(
                        label="📥 Download Invoice PDF",
                        data=pdf,
                        file_name=f"invoice_{invoice['invoice_number']}.pdf",
                        mime="application/pdf"
                    )

                else:

                    st.error("Unable to load invoice.")