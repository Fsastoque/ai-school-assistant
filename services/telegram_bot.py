from data.repository import obtener_usuario_por_codigo, vincular_chat_id, actualizar_step, obtener_usuario_por_chat,logout_usuario, actualizar_last_active
from core.session import sesion_expirada
from core.chatbot import responder_normal
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from services.telegram_menu import menu_principal
from handlers.callbacks import button_handler
from telegram.ext import CallbackQueryHandler


# 🔥 Estado por usuario (clave)
user_states = {}

def responder_telegram(texto, chat_id):
    texto = texto.strip().lower()

    # 🔴 1. LOGOUT GLOBAL
    if texto in ["logout", "salir", "cerrar sesión", "cerrar sesion"]:
        user = obtener_usuario_por_chat(chat_id)

        if user:
            codigo = user[0]
            logout_usuario(codigo)
            return (
                "👋 Sesión cerrada correctamente.\n\n"
                "¡Hola! Bienvenido al Asistente Educativo Institucional 🎓\n\n"
                "Para poder ayudarte con información personalizada, "
                "por favor ingresa tu código estudiantil."
            )

        return "No tienes sesión activa."

    # 🔍 2. BUSCAR USUARIO POR CHAT_ID
    user = obtener_usuario_por_chat(chat_id)

    # 🟢 3. PRIMER CONTACTO (SIN SESIÓN)
    if not user:
        # 👉 Validar código
        posible_user = obtener_usuario_por_codigo(texto)

        if not posible_user:
            return "❌ Código no válido. Verifica con secretaría."

        codigo, nombre, chat_id_db, step = posible_user

        # 🔐 ANTI-SUPLANTACIÓN
        if chat_id_db and chat_id_db != chat_id:
            return "🚫 Este código ya está vinculado a otro dispositivo."

        # ✔ vincular usuario
        vincular_chat_id(codigo, chat_id)
        actualizar_step(codigo, "privacidad")

        return f"✅ Hola {nombre}.\n\nPara continuar, escribe SI para aceptar el tratamiento de datos."

    # 📦 4. USUARIO EXISTE
    codigo, nombre, step, last_active = user

    # 🔄 actualizar actividad
    actualizar_last_active(codigo)

    # 🔐 5. PRIVACIDAD
    if step == "privacidad":
        if texto in ["si", "sí"]:
            actualizar_step(codigo, "chat_activo")
            return "🔓 Acceso concedido. ¿En qué puedo ayudarte?"

        return "Debes aceptar los términos para continuar (responde SI)"

    # 💬 6. CHAT NORMAL
    if step == "chat_activo":
        if sesion_expirada(last_active):
            logout_usuario(codigo)
            return "⏳ Tu sesión expiró. Ingresa nuevamente tu código."

        # 👉 aquí va tu lógica real
        return responder_normal(texto)

    return "🤖 Iniciando..."

def reset_session(chat_id):
    user_states[chat_id] = {
        "chat_step": "bienvenida",
        "codigo_estudiante": None,
        "nombre_usuario": None
    }

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    texto = update.message.text

    # --- Inicializar estad|o del usuario ---
    #init_user(chat_id)
    #session = get_session(chat_id)

    # 🔥 llamar cerebro
    respuesta = responder_telegram(texto, chat_id)

    user = obtener_usuario_por_chat(chat_id)
    if user:
        codigo, nombre, step, _ = user

    if step == "chat_activo":
        await update.message.reply_text(respuesta + "\n\n👇 Selecciona una opción:", reply_markup=menu_principal())
        return

    '''if "Acceso concedido" in respuesta: 
        await update.message.reply_text( respuesta, reply_markup=menu_principal() )
        return'''

    await update.message.reply_text(respuesta)


def run_telegram_bot():

    TOKEN = ""

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot de Telegram corriendo...")
    app.run_polling()
