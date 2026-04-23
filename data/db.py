import sqlite3

DB_NAME = "data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)