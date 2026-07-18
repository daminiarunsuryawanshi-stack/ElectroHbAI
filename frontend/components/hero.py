import streamlit as st


def show_hero():

    left, right = st.columns([1, 1.3])

    with left:

        st.markdown("""
        <div style="
            display:inline-block;
            padding:8px 18px;
            border:2px solid #C084FC;
            border-radius:30px;
            color:#A855F7;
            font-weight:600;
            font-size:16px;
            margin-bottom:20px;
        ">
            ✨ Smart Shopping with AI
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <h1 style="
            font-size:72px;
            line-height:1.05;
            font-weight:800;
            color:#0F172A;
            margin-bottom:15px;
        ">
            Upgrade Your
            <br>
            <span style="
                background:linear-gradient(90deg,#60A5FA,#A855F7,#FB7185);
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
            ">
            Digital Life
            </span>
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="
            font-size:22px;
            color:#64748B;
            line-height:1.8;
            max-width:650px;
        ">
        Discover premium electronics, compare products instantly,
        and shop smarter with AI-powered recommendations.
        </p>
        """, unsafe_allow_html=True)

        st.write("")

        c1, c2 = st.columns(2)

        with c1:

            st.button(
                "🛍 Shop Now",
                width="stretch"
            )

        with c2:

            if st.button(
                "🤖 AI Assistant",
                width="stretch"
            ):
                st.session_state["page"] = "assistant"
                st.rerun()

    with right:

        st.image(
        "assets/hero_banner.png",
        width="stretch"
)

    st.write("")