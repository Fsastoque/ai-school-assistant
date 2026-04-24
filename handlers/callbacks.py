from telegram import Update
from telegram.ext import ContextTypes
from data.repository import obtener_usuario_por_chat
import services.telegram_bot
#from services.horarios_service import obtener_horario
from services.telegram_menu import menu_principal


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    chat_id = str(query.message.chat_id)    
    data = query.data

    # 🔥 reutilizar el mismo cerebro
    respuesta = services.telegram_bot.responder_telegram(data, chat_id)

    # 🔍 estado actual
    user = obtener_usuario_por_chat(chat_id)

    if user:
        codigo, nombre, step, _ = user

        if step == "chat_activo":
            await query.edit_message_text(
                respuesta,
                reply_markup=menu_principal()
            )
            return

    await query.edit_message_text(respuesta)