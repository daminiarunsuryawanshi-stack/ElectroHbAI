import streamlit as st


def show_categories():

    st.markdown(
        """
        ## 📱 Shop by Category
        Explore your favorite electronics
        """
    )

    categories = [
        ("📱", "Mobiles"),
        ("💻", "Laptops"),
        ("⌚", "Smart Watches"),
        ("🎧", "Headphones"),
        ("📷", "Cameras"),
        ("🎮", "Gaming"),
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)

    rows = [row1, row2]

    idx = 0

    for row in rows:
        for col in row:

            icon, title = categories[idx]

            with col:

                st.markdown(f"# {icon}")

                st.markdown(f"**{title}**")

                st.button(
                    "Browse",
                    key=f"cat_{idx}",
                    width="stretch",
                )

            idx += 1