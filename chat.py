import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="EducaBot Colombia", layout="wide")

tab_chat, tab_admin = st.tabs(["💬 Chat Escolar", "📊 Panel Administrativo"])

# --- PESTAÑA 1: INTERFAZ DE CHAT (Función 5) ---
with tab_chat:
    st.header("Asistente Educativo Multidepartamental")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada del usuario
    if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ENVIAR A n8n
        response = requests.post("TU_WEBHOOK_N8N", json={"message": prompt, "user": "usuario_web"})
        bot_reply = response.json().get("output", "Lo siento, tengo problemas de conexión.")

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# --- PESTAÑA 2: DASHBOARD (Fase 4 - Análisis) ---
with tab_admin:
    st.header("Estadísticas y Necesidades Emergentes")
    
    # Aquí conectas con el endpoint /stats de tu FastAPI o consultas SQLite directo
    data = pd.DataFrame({
        'Tema': ['Matrículas', 'Rutas', 'Aprendizaje', 'Certificados'],
        'Consultas': [50, 30, 80, 20]
    })

    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Temas más consultados")
        fig, ax = plt.subplots()
        ax.bar(data['Tema'], data['Consultas'], color='#007BFF')
        st.pyplot(fig)
    
    with col2:
        st.write("#### Resumen de Eficiencia")
        st.metric("Resolución Automática", "92%", "+5%")
        st.metric("Transferencia a Humano", "8%", "-2%")