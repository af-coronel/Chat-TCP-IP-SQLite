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

# Función para guardar un mensaje en la base de datos
def save_message(contenido, ip_cliente):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mensaje (contine, ip_cliente) VALUES (?, ?)",
        (contenido, ip_cliente),
    )
    conn.commit()
    conn.close()

# Función principal: acepta conexiones, recibe, guarda y responde
def run_server(server):
    while True:
        client, addr = server.accept()
        print(f"Cliente conectado desde: {addr[0]}:{addr[1]}")

        data = client.recv(1024)
        if not data:
            client.close()
            continue

        mensaje = data.decode("utf-8")
        ip_cliente = addr[0]
        save_message(mensaje, ip_cliente)

        respuesta = f"Mensaje recibido: {mensaje}"
        client.send(respuesta.encode("utf-8"))
        client.close()

# Punto de entrada del programa
if __name__ == "__main__":
    init_db()
    server = init_socket()
    print("Servidor escuchando en localhost:5000...")
    run_server(server)