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

# Función para inicializar el socket del servidor
def init_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost",5000))
    server.listen(5)
    return server

# Punto de entrada del programa (se ejecuta al correr python server.py)
if __name__ == "__main__":
    init_db()
    server = init_socket()
    print("Servidor escuchando en localhost:5000...")