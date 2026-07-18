import streamlit as st
from utils.auth import login


def show_login():

    st.title("🔐 Login")


    email = st.text_input("Email")


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        if email == "" or password == "":

            st.warning("Please fill all fields")


        else:

            response = login(
                email,
                password
            )


            if response.status_code == 200:

                token = response.json()["access_token"]

                st.session_state["token"] = token
                st.session_state["logged_in"] = True
                st.session_state["page"] = "home"

                st.success("Login Successful ✅")

                st.rerun()


            else:

                st.error("Invalid Email or Password")
                