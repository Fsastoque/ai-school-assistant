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