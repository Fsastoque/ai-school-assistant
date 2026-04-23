from data.db import get_connection

def init_db():

    conn = get_connection()
    c = conn.cursor()

    # --- USUARIOS ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        codigo TEXT PRIMARY KEY,
        nombre TEXT,
        grado TEXT,
        acepto_terminos INTEGER,
        chat_id TEXT,
        chat_step TEXT DEFAULT 'bienvenida',
        last_active TIMESTAMP
    )
    """)

    # --- TICKETS ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        tipo TEXT,
        descripcion TEXT,
        estado TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --- RECURSOS ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS recursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        url TEXT,
        materia TEXT,
        grado TEXT
    )
    """)

    # --- HORARIOS ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS horarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grado TEXT,
        dia TEXT,
        hora TEXT,
        asignatura TEXT
    )
    """)

    # --- LOGS (CLAVE PARA DASHBOARD) ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        consulta TEXT,
        intencion TEXT
    )
    """)


        # --- DATOS DE PRUEBA ---
    c.execute("SELECT COUNT(*) FROM recursos")
    if c.fetchone()[0] == 0:

        c.execute("""
        INSERT INTO recursos (titulo, url, materia, grado)
        VALUES
        ('Guía de Matemáticas', 'https://example.com/mate.pdf', 'Matemáticas', '10'),
        ('Video Física', 'https://youtube.com/fisica', 'Física', '10'),
        ('Guía Química', 'https://example.com/quimica.pdf', 'Química', '11')
        """)

    c.execute("SELECT COUNT(*) FROM usuarios")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO usuarios (codigo, nombre, grado, acepto_terminos)
        VALUES ('28288', 'Carlos Perez', '10', 1)
        """)   
    conn.commit()
    conn.close()