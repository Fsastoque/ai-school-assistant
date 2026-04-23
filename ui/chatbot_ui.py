import streamlit as st
from core.chatbot import responder


def mostrar_chatbot():

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.write(msg)

    pregunta = st.text_input("Escribe tu mensaje")

    if st.button("Enviar") and pregunta:

        st.session_state.chat.append(f"👤 {pregunta}")

        respuesta = responder(pregunta)

        st.session_state.chat.append(f"🤖 {respuesta}")

        st.rerun()