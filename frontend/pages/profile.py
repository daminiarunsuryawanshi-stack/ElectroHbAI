import streamlit as st


def profile_page():

    st.title("👤 My Profile")

    if not st.session_state.get("logged_in"):

        st.warning("Please login first.")

        if st.button("🔐 Login"):

            st.session_state["page"] = "login"

            st.rerun()

        return

    st.success("Logged in successfully ✅")

    st.write("You are logged in to ElectroHub AI.")

    st.divider()

    if st.button(
        "📦 My Orders",
        use_container_width=True
    ):

        st.session_state["page"] = "orders"

        st.rerun()

    if st.button(
        "❤️ My Wishlist",
        use_container_width=True
    ):

        st.session_state["page"] = "wishlist"

        st.rerun()

    if st.button(
        "🛒 My Cart",
        use_container_width=True
    ):

        st.session_state["page"] = "cart"

        st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.session_state["page"] = "home"

        st.rerun()