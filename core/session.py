from datetime import datetime, timedelta

SESSION_TIMEOUT = 10  # minutos

def sesion_expirada(last_active):

    if not last_active:
        return True

    try:
        last = datetime.fromisoformat(last_active)
    except:
        return True

    return datetime.now() - last > timedelta(minutes=SESSION_TIMEOUT)