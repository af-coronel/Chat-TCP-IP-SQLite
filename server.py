#Servidor de Chat: Escucha mensajes y los guarda en SQLite:
import socket
import sqlite3
from datetime import datetime

# Configuración del socket TCP/IP
HOST = "localhost"
PORT = 5000
DB_PATH = "chat.db"


# Función para inicializar la base de datos
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
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
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo acceder a la base de datos: {e}")
        raise


# Función para inicializar el socket del servidor
def init_socket():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        return server
    except OSError as e:
        print(f"[ERROR] No se pudo iniciar el socket en {HOST}:{PORT}. "
              f"¿Estará el puerto ocupado? {e}")
        raise


# Función para guardar un mensaje en la base de datos
def save_message(contenido, ip_cliente, timestamp):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (contenido, timestamp, ip_cliente),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo guardar el mensaje: {e}")
        raise

# Función principal: acepta conexiones, recibe, guarda y responde
def run_server(server):
    while True:
        try:
            client, addr = server.accept()
            print(f"Cliente conectado desde: {addr[0]}:{addr[1]}")

            data = client.recv(1024)
            if not data:
                client.close()
                continue

            mensaje = data.decode("utf-8")
            ip_cliente = addr[0]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_message(mensaje, ip_cliente, timestamp)

            respuesta = f"Mensaje recibido: {timestamp}"
            client.send(respuesta.encode("utf-8"))
            client.close()
        except (OSError, sqlite3.Error, UnicodeDecodeError) as e:
            print(f"[ERROR] Al procesar la conexión: {e}")
            client.close()


# Punto de entrada del programa
if __name__ == "__main__":
    try:
        init_db()
        server = init_socket()
        print(f"Servidor escuchando en {HOST}:{PORT}...")
        run_server(server)
    except Exception as e:
        print(f"[ERROR] No se pudo iniciar el servidor: {e}")