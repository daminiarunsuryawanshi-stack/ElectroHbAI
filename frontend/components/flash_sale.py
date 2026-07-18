import streamlit as st
from utils.api import get_products


def show_flash_sale():

    st.markdown(
        """
        <h2 style="font-size:42px;font-weight:800;color:#334155;margin-top:60px;">
            ⚡ Flash Sale
        </h2>

        <p style="font-size:20px;color:#64748B;margin-bottom:30px;">
            Today's hottest AI-picked deals
        </p>
        """,
        unsafe_allow_html=True,
    )

    products = get_products()

    if not products:
        st.warning("No products available.")
        return

    # Remove duplicate products
    seen = set()
    unique_products = []

    for product in products:
        name = product.get("name", "")

        if name not in seen:
            seen.add(name)
            unique_products.append(product)

    flash_products = unique_products[:3]

    cols = st.columns(3)

    for col, product in zip(cols, flash_products):

        with col:

            with st.container(border=True):

                st.markdown(
                    """
                    <div style="
                    background:#FB7185;
                    color:white;
                    display:inline-block;
                    padding:6px 12px;
                    border-radius:20px;
                    font-size:13px;
                    font-weight:bold;
                    margin-bottom:10px;
                    ">
                    🔥 20% OFF
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                image = product.get("image", "")

                if image:
                    st.image(image, width="stretch")
                else:
                    st.image(
                        "https://via.placeholder.com/350x250?text=No+Image",
                        width="stretch",
                    )

                name = product.get("name", "Unknown Product")

                if len(name) > 55:
                    name = name[:55] + "..."

                st.markdown(f"**{name}**")

                rating = product.get("rating", 4.8)
                st.write(f"⭐ {rating}")

                price = product.get("price", 0)
                old_price = round(price * 1.20, 2)

                st.markdown(
                    f"""
                    <span style="font-size:28px;font-weight:bold;color:#FB7185;">
                        ₹{price}
                    </span>

                    <span style="
                        color:gray;
                        text-decoration:line-through;
                        margin-left:8px;
                        font-size:18px;
                    ">
                        ₹{old_price}
                    </span>
                    """,
                    unsafe_allow_html=True,
                )

                st.button(
                    "🛒 Buy Now",
                    key=f"flash_{product['id']}",
                    width="stretch",
                )