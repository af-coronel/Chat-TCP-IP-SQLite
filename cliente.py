# Cliente de Chat: se conecta al servidor, envía mensajes y muestra las respuestas
import socket

# Configuración del socket TCP/IP
HOST = "localhost"
PORT = 5000


# Función para enviar un mensaje y mostrar la respuesta del servidor
def send_message(client, mensaje):
    client.send(mensaje.encode("utf-8"))
    respuesta = client.recv(1024).decode("utf-8")
    print(f"Servidor: {respuesta}")


# Función principal del cliente
def run_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"Conectado al servidor en {HOST}:{PORT}. "
              "Escribí un mensaje o 'éxito' para salir.")

        while True:
            try:
                mensaje = input("Mensaje: ").strip()
            except EOFError:
                print("\nEntrada cerrada. Saliendo del chat...")
                break
            if mensaje.lower() == "éxito":
                print("Saliendo del chat...")
                break
            send_message(client, mensaje)

        client.close()
    except (ConnectionError, OSError) as e:
        print(f"[ERROR] No se pudo conectar al servidor en {HOST}:{PORT}: {e}")


# Punto de entrada del programa
if __name__ == "__main__":
    run_client()