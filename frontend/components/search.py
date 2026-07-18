import streamlit as st


def show_search():

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
        placeholder="🔍 Search iPhone, MacBook, Sony, Samsung...",
        label_visibility="collapsed"
    )

    st.write("")

    selected_category = None

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        if st.button("📱 Mobiles", use_container_width=True):
            selected_category = "Mobile"

    with c2:
        if st.button("💻 Laptops", use_container_width=True):
            selected_category = "Laptop"

    with c3:
        if st.button("🎧 Audio", use_container_width=True):
            selected_category = "Audio"

    with c4:
        if st.button("⌚ Watches", use_container_width=True):
            selected_category = "Watch"

    with c5:
        if st.button("🎮 Gaming", use_container_width=True):
            selected_category = "Gaming"

    return search, selected_category