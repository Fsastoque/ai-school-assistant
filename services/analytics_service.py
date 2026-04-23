from data.db import get_connection
import pandas as pd

def obtener_logs():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()
    return df