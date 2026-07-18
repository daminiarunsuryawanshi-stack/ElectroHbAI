import streamlit as st


def show_navbar():

    c1, c2 = st.columns([3, 7])

    with c1:

        st.markdown("""
        <div style="
            font-size:42px;
            font-weight:800;
            background:linear-gradient(90deg,#FB7185,#A855F7,#60A5FA);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            letter-spacing:1px;
            padding-top:8px;
        ">
            ⚡ ElectroHub
        </div>
        """, unsafe_allow_html=True)

    with c2:

        c21, c22, c23, c24, c25 = st.columns(5)

        with c21:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state["page"] = "home"
                st.rerun()

        with c22:
            if st.button("❤️ Wishlist", use_container_width=True):
                st.session_state["page"] = "wishlist"
                st.rerun()

        with c23:
            if st.button("🛒 Cart", use_container_width=True):
                st.session_state["page"] = "cart"
                st.rerun()

        with c24:
            if st.button("📦 Orders", use_container_width=True):
                st.session_state["page"] = "orders"
                st.rerun()

        with c25:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state["page"] = "login"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)