from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu_principal_old():
    teclado = [
        [KeyboardButton("📅 Horarios"), KeyboardButton("📋 Asignaturas")],
        [KeyboardButton("📄 Certificados"), KeyboardButton("🛠 Reportar falla")],
        [KeyboardButton("📚 Recursos"), KeyboardButton("✔️ Actividades")],
        [KeyboardButton("🚪 Salir")]
    ]

    return ReplyKeyboardMarkup(teclado, resize_keyboard=True)

def menu_principal():

    teclado = [
        [
            InlineKeyboardButton("📅 Horarios", callback_data="horarios"),
            InlineKeyboardButton("📋 Asignaturas", callback_data="asignaturas")
        ],
        [
            InlineKeyboardButton("📄 Certificados", callback_data="certificados"),
            InlineKeyboardButton("🛠 Reportar falla", callback_data="falla")
        ],
        [
            InlineKeyboardButton("📚 Recursos", callback_data="recursos"),
            InlineKeyboardButton("✔️ Actividades", callback_data="actividades")
        ],
        [
            InlineKeyboardButton("🚪 Salir", callback_data="salir")
        ]
    ]

    return InlineKeyboardMarkup(teclado)