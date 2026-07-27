import streamlit as st


def show_search():

    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = None

    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""

    st.markdown("""
    <div class="search-title">
    🔍 Find Your Next Gadget
    </div>

    <div class="search-subtitle">
    Search thousands of AI-powered electronics
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input(
        "Search Products",
        value=st.session_state["search_query"],
        placeholder="🔍 Search iPhone, MacBook, Sony, Samsung...",
        label_visibility="collapsed",
        key="search_query"
    )

    st.write("")

    selected_category = st.session_state["selected_category"]

    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 0.8])

    with c1:
        if st.button("📱 Mobiles", use_container_width=True):
            st.session_state["selected_category"] = "Mobile"
            st.rerun()

    with c2:
        if st.button("💻 Laptops", use_container_width=True):
            st.session_state["selected_category"] = "Laptop"
            st.rerun()

    with c3:
        if st.button("🎧 Audio", use_container_width=True):
            st.session_state["selected_category"] = "Audio"
            st.rerun()

    with c4:
        if st.button("⌚ Watches", use_container_width=True):
            st.session_state["selected_category"] = "Watch"
            st.rerun()

    with c5:
        if st.button("🎮 Gaming", use_container_width=True):
            st.session_state["selected_category"] = "Gaming"
            st.rerun()

    with c6:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state["selected_category"] = None
            st.session_state["search_query"] = ""
            st.rerun()

    if selected_category:
        st.markdown(f"**Showing:** {selected_category} products")

    return search, selected_category