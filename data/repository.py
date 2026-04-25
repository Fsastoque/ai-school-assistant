from data.db import get_connection
from datetime import datetime

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

def obtener_usuario_por_codigo(codigo):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT codigo, nombre, chat_id, chat_step FROM usuarios WHERE codigo = ?", (codigo,))
    user = c.fetchone()

    conn.close()
    return user


def obtener_usuario_por_chat(chat_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT codigo, nombre, chat_step, last_active FROM usuarios WHERE chat_id = ?", (chat_id,))
    user = c.fetchone()

    conn.close()
    return user


def vincular_chat_id(codigo, chat_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE usuarios SET chat_id = ? WHERE codigo = ?", (chat_id, codigo))

    conn.commit()
    conn.close()


def actualizar_step(codigo, step):
    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE usuarios SET chat_step = ? WHERE codigo = ?", (step, codigo))

    conn.commit()
    conn.close()

def actualizar_last_active(codigo):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    UPDATE usuarios SET last_active = ?
    WHERE codigo = ?
    """, (datetime.now(), codigo))

    conn.commit()
    conn.close()


def logout_usuario(codigo):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    UPDATE usuarios
    SET chat_id = NULL, chat_step = 'inicio', last_active = NULL
    WHERE codigo = ?
    """, (codigo,))

    conn.commit()
    conn.close()
