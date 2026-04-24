user_states = {}

def init_user(chat_id: str):
    if chat_id not in user_states:
        user_states[chat_id] = {
            "chat_step": "bienvenida",
            "codigo_estudiante": None,
            "nombre_usuario": None
        }


def get_session(chat_id: str):
    return user_states.get(chat_id)


def update_session(chat_id: str, data: dict):
    if chat_id not in user_states:
        init_user(chat_id)

    user_states[chat_id].update(data)


def set_step(chat_id: str, step: str):
    init_user(chat_id)
    user_states[chat_id]["chat_step"] = step


def get_step(chat_id: str):
    return user_states.get(chat_id, {}).get("chat_step")


def clear_session(chat_id: str):
    if chat_id in user_states:
        user_states[chat_id] = {
            "chat_step": "bienvenida",
            "codigo_estudiante": None,
            "nombre_usuario": None
        }