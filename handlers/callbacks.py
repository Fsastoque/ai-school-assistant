from telegram import Update
from telegram.ext import ContextTypes
from data.repository import obtener_usuario_por_chat
import services.telegram_bot
from services.telegram_menu import menu_principal, menu_faq, menu_tramites, menu_horarios, menu_recursos


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    chat_id = str(query.message.chat_id)    
    data = query.data
    
    # 🔝 MENÚ PRINCIPAL
    if data == "menu_principal":
        await query.edit_message_text(
            "📌 Menú principal",
            reply_markup=menu_principal()
        )
        return

    # 📚 FAQ
    if data == "faq":
        await query.edit_message_text(
            "📚 Preguntas frecuentes",
            reply_markup=menu_faq()
        )
        return

    if data == "faq_horario":
        await query.edit_message_text(
            "📅 Selecciona el tipo de horario:",
            reply_markup=menu_horarios()
        )
        return
    
    # 📆 HORARIO DE HOY
    if data == "horario_hoy":
        respuesta = services.telegram_bot.responder_telegram("horario hoy", chat_id)

        await query.edit_message_text(
            respuesta,
            reply_markup=menu_horarios()
        )
        return

    # 🗓 HORARIO SEMANAL
    if data == "horario_semana":
        respuesta = services.telegram_bot.responder_telegram("horario semana", chat_id)

        await query.edit_message_text(
            respuesta,
            reply_markup=menu_horarios()
        )
        return

    if data == "faq_materias":
        respuesta = services.telegram_bot.responder_telegram("asignaturas", chat_id)        
        await query.edit_message_text(
            respuesta,
            reply_markup=menu_faq()
        )
        return

    if data == "faq_actividades":
        respuesta = services.telegram_bot.responder_telegram("actividades", chat_id)        
        await query.edit_message_text(
            respuesta,
            reply_markup=menu_faq()
        )
        return
    
    if data == "faq_reuniones":
        respuesta = services.telegram_bot.responder_telegram("eventos", chat_id)        
        await query.edit_message_text(
            respuesta,
            reply_markup=menu_faq()
        )
        return

    # 🛠 TRÁMITES
    if data == "tramites":
        await query.edit_message_text(
            "🛠 Gestor de trámites",
            reply_markup=menu_tramites()
        )
        return

    if data == "tram_cert":
        respuesta = services.telegram_bot.responder_telegram("certificado", chat_id)
        await query.edit_message_text(
            respuesta,
            reply_markup=menu_tramites()
        )
        return
    
    if data == "tram_asistencia":
        respuesta = services.telegram_bot.responder_telegram("constancia", chat_id)
        await query.edit_message_text(
            respuesta,
            reply_markup=menu_tramites()
        )
        return

    if data == "tram_falla":
        respuesta = services.telegram_bot.responder_telegram("falla", chat_id)
        await query.edit_message_text(
            respuesta,
            reply_markup=menu_tramites()
        )
        return

    # 📂 RECURSOS
    if data == "recursos":
        await query.edit_message_text(
            "📂 Recursos",
            reply_markup=menu_recursos()
        )
        return

    if data == "rec_videos":
        respuesta = services.telegram_bot.responder_telegram("videos", chat_id)
        await query.edit_message_text(respuesta)
        return

    # 🛡 ADMIN
    if data == "admin":
        await query.edit_message_text("🔐 Panel administrativo (próximamente)")
        return
    
    # LOGOUT
    if data == "salir":
        respuesta = services.telegram_bot.responder_telegram("salir", chat_id)
        await query.edit_message_text(respuesta)
        return  