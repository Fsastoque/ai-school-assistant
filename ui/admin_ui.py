import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from services.analytics_service import obtener_logs

@st.dialog("🔐 Panel Administrativo")
def abrir_admin():

    st.markdown("### 📊 Dashboard")

    df = obtener_logs()

    if df.empty:
        st.info("Sin datos")
        return

    # --- GRÁFICA 1 ---
    conteo = df["intencion"].value_counts()

    fig = plt.figure()
    plt.bar(conteo.index, conteo.values)
    plt.title("Temas más consultados")
    st.pyplot(fig)

    # --- GRÁFICA 2 ---
    df["hora"] = pd.to_datetime(df["timestamp"]).dt.hour
    horas = df["hora"].value_counts().sort_index()

    fig2 = plt.figure()
    plt.plot(horas.index, horas.values)
    plt.title("Horas pico")
    st.pyplot(fig2)

    # 🔥 Asegurar formato fecha
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # ==================================================
    # 📊 GRÁFICA 1: TEMAS MÁS CONSULTADOS
    # ==================================================
    st.subheader("📌 Temas más consultados")
    grafica_temas_consultados()

def grafica_temas_consultados():

    df = obtener_logs()

    # 🔐 validar
    if df.empty:
        st.warning("No hay datos aún")
        return

    st.subheader("📊 Temas más consultados")

    # 🔥 contar intenciones
    conteo = df['intencion'].value_counts()

    # 📈 gráfica
    fig, ax = plt.subplots()
    ax.bar(conteo.index, conteo.values)

    ax.set_title("Consultas por tema")
    ax.set_xlabel("Tema")
    ax.set_ylabel("Cantidad")

    # 🔥 importante: rotar etiquetas
    plt.xticks(rotation=30)

    st.pyplot(fig)