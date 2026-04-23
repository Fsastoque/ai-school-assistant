from core.intents import detectar_intencion
from data.repository import crear_ticket, obtener_recursos, guardar_log, validar_codigo, obtener_usuario_por_codigo, vincular_chat_id, actualizar_step, obtener_usuario_por_chat,logout_usuario, actualizar_last_active
import streamlit as st
from core.session import sesion_expirada
from services.telegram_menu import menu_principal

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
    
    if intent == "asignaturas":
        return "📋 Las asignaturas que tienes asignadas para este periodo son:\n\n•Matemáticas \n• Español \n• Inglés \n• Ciencias Naturales \n• Sociales \n• Ética \n• Informática \n• Educación Física"

    if intent == "actividades":
        return "✔️ Las actividades que tienes asignadas son:\n\n•Matemáticas: Función cuadrática (Entregar el lunes)\n\n•Español: Análisis literario (Entregar el miércoles)\n\n•Inglés: Vocabulario (Entregar el viernes) \n\n•Salidas pedagogicas: Excursion a la biblioteca municipal (24 de octubre)"

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

def responder_telegram(texto, chat_id):

    texto = texto.strip()

    # 🔴 1. LOGOUT GLOBAL
    if texto.lower() in ["logout", "salir", "cerrar sesión", "cerrar sesion"]:
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

    # 🔥 3. SI NO EXISTE → INICIAR FLUJO
    if not user:

        # 👉 SI EL MENSAJE PARECE CÓDIGO
        posible_user = obtener_usuario_por_codigo(texto)

        if not posible_user:
            return "❌ Código no válido. Verifica con secretaría."
        
        codigo, nombre, chat_id_db, step = posible_user

        # 🔐 VALIDAR SUPLANTACIÓN
        if chat_id_db and chat_id_db != chat_id:
            return "🚫 Este código ya está vinculado a otro dispositivo."

        # ✔ vincular usuario
        vincular_chat_id(codigo, chat_id)
        actualizar_step(codigo, "privacidad")

        return f"✅ Hola {nombre}.\n\nPara continuar, acepta el tratamiento de datos personales escribiendo SI."

        # 👉 PRIMER CONTACTO (SALUDO)
        return (
            "¡Hola! 👋 Bienvenido al Asistente Educativo Institucional 🎓\n\n"
            "Para poder ayudarte con información personalizada, "
            "por favor ingresa tu código estudiantil."
        )

    # 📦 4. USUARIO YA EXISTE
    codigo, nombre, step, last_active = user   

    # 🔄 6. ACTUALIZAR ACTIVIDAD
    actualizar_last_active(codigo)

    # 🔐 7. PRIVACIDAD
    if step == "privacidad":

        if texto.lower() in ["si", "sí"]:
            actualizar_step(codigo, "chat_activo")
            return f"🔓 Acceso concedido, {nombre}."
            
        return "Debes aceptar los términos para continuar (responde SI)"

    # 💬 8. CHAT NORMAL
    if step == "chat_activo":
        if sesion_expirada(last_active):
            logout_usuario(codigo)
            return "⏳ Tu sesión expiró. Ingresa nuevamente tu código."
        return responder_normal(texto)   
        
        
        if texto == "🚪 Salir":
            user = obtener_usuario_por_chat(chat_id)

            if user:
                logout_usuario(user[0])

            return (
                "👋 Sesión cerrada.\n\n"
                "¡Hola! Bienvenido al Asistente Educativo 🎓\n"
                "Ingresa tu código estudiantil:"
            )

    return "🤖 Iniciando..."