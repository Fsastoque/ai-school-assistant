from core.intents import detectar_intencion
from data.repository import crear_ticket, obtener_recursos, guardar_log, validar_codigo, obtener_usuario_por_codigo, vincular_chat_id, actualizar_step, obtener_usuario_por_chat,logout_usuario, actualizar_last_active
import streamlit as st
from services.telegram_menu import menu_principal

if "chat_step" not in st.session_state:
    st.session_state.chat_step = "bienvenida"

def responder(pregunta):

    step = st.session_state.chat_step

    # --- PASO 1: BIENVENIDA ---
    if step == "bienvenida":
        st.session_state.chat_step = "pedir_codigo"

        return (
            "👋 ¡Hola! Bienvenido al Asistente Educativo Institucional 🎓\n\n"
            "Para ayudarte con información personalizada, por favor ingresa tu código estudiantil."
        )

    # --- PASO 2: VALIDAR CÓDIGO ---
    elif step == "pedir_codigo":

        usuario = validar_codigo(pregunta)

        if not usuario:
            return "❌ Código no válido. Verifica con secretaría."

        # ✔ válido
        st.session_state.codigo_estudiante = pregunta
        st.session_state.nombre_usuario = usuario[0]
        st.session_state.chat_step = "privacidad"

        return f"✅ ¡Gracias, {usuario[0]}!.\n\nAntes de continuar, por razones de seguridad y protección de datos (Ley 1581), te informamos que tus consultas serán procesadas para mejorar el servicio y registradas de forma anónima para análisis administrativo. ¿Aceptas el tratamiento de tus datos para este chat?"

    # --- PASO 3: PRIVACIDAD ---
    elif step == "privacidad":
        if "si" in pregunta.lower():
            st.session_state.chat_step = "chat_activo"
            return "🔓 Acceso concedido. ¿En qué puedo ayudarte?"

        else:
            return "Debes aceptar los términos para continuar (responde SI)"

    # --- PASO 4: CHAT NORMAL ---
    elif step == "chat_activo":

        # Aquí llamas tu lógica anterior
        return responder_normal(pregunta)    

def responder_normal(pregunta, canal="web", chat_id=None):

    intent = detectar_intencion(pregunta)
    guardar_log(pregunta, intent)    

    if intent == "horario":
        return "📅 Tu horario es de 7:00am a 1:00pm"

    elif intent == "eventos":
        return "📌 Reunión de padres viernes 4pm"

    elif intent == "certificado":
        return  """
            📄 *Certificado de estudio*
            ━━━━━━━━━━━━━━━
            🔗 Descárgalo aquí:
            https://drive.google.com/file/d/1AEZVUJlmXaZGvQBPUDs03VSKXojotsKa/view?usp=drive_link
            ━━━━━━━━━━━━━━━
            """
    
    elif intent == "constancia_estudio":
        return  """
            📘 *Constancia de estudio*
            ━━━━━━━━━━━━━━━
            🔗 Descárgalo aquí:
            https://drive.google.com/file/d/1SMV2ExwSaLbVK6jWJcHgwI2lH9k3z0_5/view?usp=drive_link
            ━━━━━━━━━━━━━━━
            """
    
    if intent == "asignaturas":
        return "📋 Las asignaturas que tienes asignadas para este periodo son:\n\n•Matemáticas \n• Lenguaje \n• Inglés \n• Quimica \n• Física \n• Ética \n• Deporte \n• Educación Física"

    if intent == "actividades":
        return "✔️ Las actividades que tienes asignadas son:\n\n•Matemáticas: Función cuadrática (Entregar el lunes)\n\n•Español: Análisis literario (Entregar el miércoles)\n\n•Inglés: Vocabulario (Entregar el viernes) \n\n•Salidas pedagogicas: Excursion a la biblioteca municipal (24 de octubre)"

    elif intent == "falla":
        codigo = obtener_codigo_usuario(canal, chat_id)
        if not codigo:
            return "🔐 Debes iniciar sesión"

        ticket_id = crear_ticket(
            codigo,
            "falla",
            pregunta
        )

        return f"🛠️ Ticket #{ticket_id} creado correctamente"

    elif intent == "recursos":
        recursos = obtener_recursos()

        if not recursos:
            return "No hay recursos disponibles"

        r = "\n".join([f"{x[0]}: {x[1]}" for x in recursos])
        return f"📚 Recursos:\n{r}"

    return "🤖 No entendí tu solicitud"

def obtener_codigo_usuario(canal, chat_id=None):

    if canal == "telegram":
        user = obtener_usuario_por_chat(chat_id)
        return user[0] if user else None

    elif canal == "web":
        return st.session_state.get("codigo_estudiante")