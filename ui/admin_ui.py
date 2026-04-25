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

    st.subheader("📈 Horas pico")

    # --- GRÁFICA 2: HORAS PICO ---
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["hora"] = df["timestamp"].dt.hour

    horas = df["hora"].value_counts().sort_index()

    fig, ax = plt.subplots()
    plt.ylim(0, 25)

    ax.plot(horas.index, horas.values, marker='o')

    # 🎯 Títulos y etiquetas
    ax.set_title("Horas pico de uso", fontsize=14)
    ax.set_xlabel("Hora del día (0 - 23)")
    ax.set_ylabel("Cantidad de consultas")

    # 🎯 mostrar cada hora
    ax.set_xticks(range(0, 24))

    # 🎯 grid para mejor lectura
    ax.grid(True, linestyle='--', alpha=0.5)

    # 🎯 destacar la hora pico
    hora_pico = horas.idxmax()
    valor_pico = horas.max()

    ax.scatter(hora_pico, valor_pico, s=100)
    ax.annotate(
        f"Pico: {hora_pico}:00",
        (hora_pico, valor_pico),
        textcoords="offset points",
        xytext=(0,10),
        ha='center'
    )

    st.pyplot(fig)
