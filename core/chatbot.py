from core.intents import detectar_intencion
from data.repository import crear_ticket, obtener_recursos, guardar_log, validar_codigo
import streamlit as st

if "chat_step" not in st.session_state:
    st.session_state.chat_step = "bienvenida"

def responder(pregunta):

    step = st.session_state.chat_step

    # --- PASO 1: BIENVENIDA ---
    if step == "bienvenida":
        st.session_state.chat_step = "pedir_codigo"

        return (
            "¡Hola! Bienvenido al Asistente Educativo Institucional 🎓\n\n"
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

def responder_normal(pregunta):

    intent = detectar_intencion(pregunta)
    guardar_log(pregunta, intent)

    if intent == "horario":
        return "📅 Tu horario es de 7:00am a 1:00pm"

    elif intent == "eventos":
        return "📌 Reunión de padres viernes 4pm"

    elif intent == "certificado":
        return "📄 Solicitud registrada"

    elif intent == "falla":
        ticket_id = crear_ticket(
            st.session_state.codigo_estudiante,
            "falla",
            pregunta
        )
        return f"🛠️ Ticket #{ticket_id} creado"

    elif intent == "recursos":
        recursos = obtener_recursos()

        if not recursos:
            return "No hay recursos disponibles"

        r = "\n".join([f"{x[0]}: {x[1]}" for x in recursos])
        return f"📚 Recursos:\n{r}"

    return "🤖 No entendí tu solicitud"