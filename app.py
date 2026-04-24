import streamlit as st
import pandas as pd
import sqlite3
from core.security import validar_usuario
from services.analytics_service import obtener_logs
from core.chatbot import responder

# Inicializar base de datos si no existe
from data.init_db import init_db
init_db()

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Portal Escolar | Institución Educativa", layout="wide")

# --- 2. CSS GLOBAL ---
st.markdown("""
<style>
/* HEADER */
.nav-header {
    background: linear-gradient(90deg, #003366 0%, #0055aa 100%);
    padding: 20px;
    color: white;
    text-align: center;
    border-bottom: 4px solid #ffcc00;
}
.sub-nav {
    background-color: #f0f0f0;
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #ddd;
    margin-bottom: 20px;
}
.sub-nav a {
    margin: 0 15px;
    text-decoration: none;
    color: #333;
    font-weight: bold;
}

/* TARJETAS */
.module-box {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}
.module-title {
    background-color: #003366;
    color: white;
    padding: 5px 10px;
    margin: -15px -15px 15px -15px;
    border-radius: 4px 4px 0 0;
    font-weight: bold;
}

/* Botón tipo chat flotante */
button[kind="secondary"] {
    border-radius: 50px !important;
    background-color: #003366 !important;
    color: white !important;
    font-weight: bold !important;
    padding: 10px 15px !important;
}

/* Hover */
button[kind="secondary"]:hover {
    background-color: #0055aa !important;
}

/* Botones dentro del popover */
div[data-testid="stPopover"] button {
    width: 100%;
    border-radius: 10px !important;
    margin-top: 5px;
}

/* Animación ligera */
div[data-testid="stPopover"] {
    animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px);}
    to { opacity: 1; transform: translateY(0);}
}

/* MODAL */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.4);
    z-index: 9998;
}
.modal-box {
    position: fixed;
    bottom: 100px;
    right: 25px;
    width: 300px;
    background: white;
    border-radius: 15px;
    padding: 20px;
    z-index: 9999;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px);}
    to { opacity: 1; transform: translateY(0);}
}

/* FOOTER */
.footer {
    background: #003366;
    color: white;
    padding: 20px;
    text-align: center;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)
# --- 3. ESTADO ---
if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = False
if "vista" not in st.session_state:
    st.session_state.vista = "inicio"
if "admin_logueado" not in st.session_state:
    st.session_state.admin_logueado = False
if st.session_state.admin_logueado:
    st.success("🔓 Admin activo")
if "abrir_admin" not in st.session_state:
    st.session_state.abrir_admin = False
if "abrir_chat" not in st.session_state:
    st.session_state.abrir_chat = False

    

def toggle_menu():
    st.session_state.mostrar_menu = not st.session_state.mostrar_menu

# --- FUNCIÓN MODAL CHATBOT ---
@st.dialog("🤖 Asistente Virtual")
def abrir_chatbot():
    if "chat_historial" not in st.session_state:
        st.session_state.chat_historial = []
    if not st.session_state.chat_historial:
        saludo = responder("")  # dispara bienvenida
        st.session_state.chat_historial.append(f"{saludo}")   

    for msg in st.session_state.chat_historial:
        st.write(msg)

    with st.form("chat_form", clear_on_submit=True):
        pregunta = st.text_input("Escribe tu mensaje")
        enviado = st.form_submit_button("Enviar")
        if enviado and pregunta:
            st.session_state.chat_historial.append(f"👤 {pregunta}")
            respuesta = responder(pregunta)
            st.session_state.chat_historial.append(f"🤖 {respuesta}")
            st.session_state.abrir_chat = True
            st.rerun()
        #st.session_state.chat_historial.append(f"👤 {pregunta}")
        #respuesta = responder(pregunta)
        #st.session_state.chat_historial.append(f"🤖 {respuesta}")        
        #st.session_state.abrir_chat = True
        #st.rerun()
        

# --- FUNCIÓN MODAL PANEL ADMINISTRATIVO ---
@st.dialog("🔐 Panel Administrativo")
def abrir_admin():

     # --- LOGIN ---
    if not st.session_state.admin_logueado:

        st.markdown("### 🔐 Acceso Administrativo")
        st.caption("Ingresa tus credenciales")

        user = st.text_input("Usuario")
        pwd = st.text_input("Clave", type="password")

        if st.button("Entrar"):
            if user == "admin" and pwd == "admin123":
                st.session_state.admin_logueado = True
                st.session_state.abrir_admin = True
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")

    # --- DASHBOARD ---
    else:
        st.markdown("### 📊 Dashboard Administrativo")
        st.caption("Panel de control institucional")

        col1, col2, col3 = st.columns(3)

        col1.metric("👥 Estudiantes", "320")
        col2.metric("📚 Cursos", "18")
        col3.metric("🚌 Rutas", "12")

        st.markdown("---")

        st.markdown("#### 📌 Acciones rápidas")

        if st.button("📄 Ver reportes"):
            st.info("Generando reporte académico...")

        if st.button("👨‍🎓 Gestionar estudiantes"):
            st.success("Módulo de estudiantes abierto")

        if st.button("📢 Publicar aviso"):
            aviso = st.text_input("Escribe el aviso")
            if aviso:
                st.success(f"Aviso publicado: {aviso}")

        st.markdown("---")

        if st.button("🚪 Cerrar sesión"):
            st.session_state.admin_logueado = False
            st.rerun()

# --- 4. HEADER ---
st.markdown('''
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#003366">

<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
}
</script>
<div class="nav-header">
    <h1>PORTAL EDUCATIVO INSTITUCIONAL</h1>
    <p>Excelencia, Valores y Tecnología</p>
</div>
<div class="sub-nav">
    <a href="#">INICIO</a> | <a href="#">MI COLEGIO</a> | 
    <a href="#">GALERÍA</a> | <a href="#">CIRCULARES</a> | 
    <a href="#">CONTÁCTENOS</a>
</div>
''', unsafe_allow_html=True)

# --- 5. CONTENIDO ---
col_izq, col_cen, col_der = st.columns([1, 2, 1])

with col_izq:
    st.markdown('<div class="module-box"><div class="module-title">📂 SECCIONES</div>', unsafe_allow_html=True)
    st.button("🟢 Preescolar", use_container_width=True)
    st.button("🔵 Primaria", use_container_width=True)
    st.button("🔴 Bachillerato", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_cen:
    st.markdown('<div class="module-box"><div class="module-title">📰 NOTICIAS</div>', unsafe_allow_html=True)
    st.subheader("Proyecto de Inteligencia Artificial 2026")
    st.image("https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800")
    st.write("Nuestros estudiantes lideran el desarrollo de agentes autónomos para la comunidad.")
    st.markdown('</div>', unsafe_allow_html=True)   

with col_der:
    st.markdown('<div class="module-box"><div class="module-title">📢 AVISOS</div>', unsafe_allow_html=True)
    st.warning("📅 15 de Mayo: Entrega de informes académicos.")
    st.info(" 📋 Directorio atención a padres 2026.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    # 👇 BOTÓN DE CHAT
    with st.popover("💬 Chat"):
        st.caption("Haz clic fuera para cerrar")
        st.markdown("""
        <div style='text-align:center'>
            <h3 style='color:#003366;'>🤖 Asistencia Digital</h3>
            <p style='font-size:14px;color:gray;'>¿En qué puedo ayudarte?</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📚 Chatbot"):
            abrir_chatbot()           

        if st.button("🔐 Panel administrativo"):
            abrir_admin()

        st.divider()

        if st.session_state.abrir_admin:
            st.session_state.abrir_admin = False
            abrir_admin()

        if st.session_state.abrir_chat:
            st.session_state.abrir_chat = False
            abrir_chatbot()

# --- 8. VISTAS ---
if st.session_state.vista == "chat":
    st.sidebar.header("🤖 Chatbot")
    st.sidebar.write("Identifícate:")
    st.sidebar.text_input("Código Estudiantil")
    if st.sidebar.button("Volver"):
        st.session_state.vista = "inicio"
        st.rerun()

if st.session_state.vista == "admin":
    st.markdown("""
    <div style="position: fixed; top: 20%; left: 30%; width: 40%;
    background: white; padding: 30px; border-radius: 15px;
    box-shadow: 0 0 40px rgba(0,0,0,0.4); z-index: 9999;">
    """, unsafe_allow_html=True)

    st.subheader("Panel Admin")
    user = st.text_input("Usuario")
    pwd = st.text_input("Clave", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar"):
            if pwd == "admin123":
                st.success("Acceso correcto")
            else:
                st.error("Clave incorrecta")

    with col2:
        if st.button("Salir"):
            st.session_state.vista = "inicio"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- 9. FOOTER ---
st.markdown('''
<div class="footer">
    <p><b>INSTITUCIÓN EDUCATIVA DIGITAL</b></p>
    <p>📍 Bogotá, Colombia | 📞 (601) 555-0199</p>
    <p>© 2026 Hackathon</p>
</div>
''', unsafe_allow_html=True)