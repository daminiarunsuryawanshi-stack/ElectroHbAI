import streamlit as st

from utils.api import get_admin_dashboard


def admin_page():

    st.title("🛠 Admin Dashboard")

    data = get_admin_dashboard()

    if not data:

        st.error("Unable to load dashboard.")

        return

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "👥 Users",
            data["total_users"]
        )

        st.metric(
            "📂 Categories",
            data["total_categories"]
        )

    with c2:

        st.metric(
            "📦 Products",
            data["total_products"]
        )

        st.metric(
            "🏷 Brands",
            data["total_brands"]
        )

    with c3:

        st.metric(
            "🛒 Orders",
            data["total_orders"]
        )

        st.metric(
            "💰 Revenue",
            f"₹{data['total_revenue']}"
        )