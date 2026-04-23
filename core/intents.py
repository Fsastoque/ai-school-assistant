def detectar_intencion(texto):
    t = texto.lower()

    if "horario" in t:
        return "horario"

    if "reunión" in t or "actividad" in t:
        return "eventos"

    if "certificado" in t:
        return "certificado"

    if "falla" in t or "problema" in t:
        return "falla"

    if "guia" in t or "pdf" in t or "video" in t:
        return "recursos"

    return "otro"