from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu_principal():

    teclado = [
        [
            InlineKeyboardButton("📚 Preguntas frecuentes", callback_data="faq"),
            InlineKeyboardButton("🛠 Gestor de trámites", callback_data="tramites")
        ],
        [
            InlineKeyboardButton("📂 Recursos", callback_data="recursos"),
            InlineKeyboardButton("🛡 Panel administrativo", callback_data="admin")
        ],
        [InlineKeyboardButton("🚪 Salir", callback_data="salir")]       
    ]

    return InlineKeyboardMarkup(teclado)

def menu_faq():
    teclado = [
        [
            InlineKeyboardButton("📅 Horario", callback_data="faq_horario"),
            InlineKeyboardButton("📘 Materias", callback_data="faq_materias")
        ],        
        [
            InlineKeyboardButton("📆 Actividades", callback_data="faq_actividades"),
            InlineKeyboardButton("📢 Reuniones", callback_data="faq_reuniones")
        ],       
        [InlineKeyboardButton("⬅️ Volver", callback_data="menu_principal")]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_tramites():
    teclado = [
        [
            InlineKeyboardButton("📄 Certificado de paz y salvo", callback_data="tram_cert"), 
            InlineKeyboardButton("📘 Constancia de estudio", callback_data="tram_asistencia")
        ],        
        [InlineKeyboardButton("🚧 Reportar falla", callback_data="tram_falla")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="menu_principal")]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_recursos():
    teclado = [
        [InlineKeyboardButton("🎥 Videos", callback_data="rec_videos")],
        [InlineKeyboardButton("📄 PDFs", callback_data="rec_pdfs")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="menu_principal")]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_horarios():
    teclado = [
        [InlineKeyboardButton("📆 Horario de hoy", callback_data="horario_hoy")],
        [InlineKeyboardButton("🗓 Horario semanal", callback_data="horario_semana")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="faq")]
    ]
    return InlineKeyboardMarkup(teclado)