from telegram import ReplyKeyboardMarkup, KeyboardButton

def menu_principal():
    teclado = [
        [KeyboardButton("📅 Horarios"), KeyboardButton("📋 Asignaturas")],
        [KeyboardButton("📄 Certificados"), KeyboardButton("🛠 Reportar falla")],
        [KeyboardButton("📚 Recursos"), KeyboardButton("✔️ Actividades")],
        [KeyboardButton("🚪 Salir")]
    ]

    return ReplyKeyboardMarkup(teclado, resize_keyboard=True)