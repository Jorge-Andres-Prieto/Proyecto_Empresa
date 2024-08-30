import streamlit as st

USERS = {
    "usuario1": "password1",
    "usuario2": "password2",
}


def login():
    st.write("##")
    st.markdown("<h1 style='text-align: center; color: #003041;'>HelPharma</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        login_button = st.button("Ingresar", use_container_width=True)

        if login_button:
            if username in USERS and USERS[username] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        st.write("---")

    # Espacio vertical al final
    st.write("##")