from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from services.telegram_menu import menu_principal
from core.chatbot import responder_telegram
import streamlit as st

# 🔥 Estado por usuario (clave)
user_states = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = str(update.message.chat_id)
    texto = update.message.text

    # --- Inicializar estado del usuario ---
    if chat_id not in user_states:
        user_states[chat_id] = {
            "chat_step": "bienvenida",
            "codigo_estudiante": None,
            "nombre_usuario": None
        }

    # 🔥 Simular session_state
    fake_session = user_states[chat_id]

    # --- Inyectar estado en Streamlit-like ---
    st.session_state.chat_step = fake_session["chat_step"]
    st.session_state.codigo_estudiante = fake_session["codigo_estudiante"]
    st.session_state.nombre_usuario = fake_session["nombre_usuario"]

    # --- Ejecutar cerebro ---
    respuesta = responder_telegram(texto, chat_id)

    # --- Guardar estado actualizado ---
    fake_session["chat_step"] = st.session_state.chat_step
    fake_session["codigo_estudiante"] = st.session_state.codigo_estudiante
    fake_session["nombre_usuario"] = st.session_state.nombre_usuario

    user_states[chat_id] = fake_session

    # --- Responder en Telegram ---
    #await update.message.reply_text(respuesta)
    if "Acceso concedido" in respuesta:
        await update.message.reply_text(
            respuesta,
            reply_markup=menu_principal()
        )
    else:
        await update.message.reply_text(respuesta)


def run_telegram_bot():

    TOKEN = "8573643441:AAFLHmDGeFUq_StmT3nTNRk_OtqRS2rTinQ"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot de Telegram corriendo...")
    app.run_polling()