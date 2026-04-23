def detectar_intencion(texto):
    t = texto.lower()

    if "horario" in t:
        return "horario"

    if "reunión" in t  or "eventos" in t or "reuniones" in t:
        return "eventos"

    if "certificado" in t:
        return "certificado"

    if "falla" in t or "problema" in t:
        return "falla"

    if "guia" in t or "pdf" in t or "video" in t or "recursos" in t:
        return "recursos"
    
    if "asignaturas" in t or "materias" in t or "clases" in t:
        return "asignaturas"

    if "actividades" in t or "tareas" in t or "trabajos" in t:
        return "actividades"

    return "otro"