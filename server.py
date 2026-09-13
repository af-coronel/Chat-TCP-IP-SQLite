#Servidor de Chat: Escucha mensajes y los guarda en SQLite:
import socket
import sqlite3

# Función para inicializar la base de datos
def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS mensajes (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       contenido TEXT NOT NULL,
       fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
       ip_cliente TEXT NOT NULL
      )
    """)
    conn.commit()
    conn.close()
