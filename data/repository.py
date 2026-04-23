from data.db import get_connection

def crear_ticket(codigo, tipo, descripcion):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    INSERT INTO tickets (codigo, tipo, descripcion, estado)
    VALUES (?, ?, ?, ?)
    """, (codigo, tipo, descripcion, "Abierto"))

    ticket_id = c.lastrowid
    conn.commit()
    conn.close()

    return ticket_id


def obtener_recursos():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT titulo, url FROM recursos LIMIT 5")
    data = c.fetchall()

    conn.close()
    return data


def guardar_log(consulta, intencion):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    INSERT INTO logs (consulta, intencion)
    VALUES (?, ?)
    """, (consulta, intencion))

    conn.commit()
    conn.close()

def validar_codigo(codigo):

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT nombre FROM usuarios WHERE codigo = ?", (codigo,))
    user = c.fetchone()
    conn.close()
    
    return user