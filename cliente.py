import socket
import threading

class Cliente:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.socket_cliente = None

    def conectar(self):
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((self.host, self.puerto))
        print("Conectado al servidor {}:{}".format(self.host, self.puerto))

        hilo_recepcion = threading.Thread(target=self.recibir_mensajes)
        hilo_recepcion.start()

    def enviar_mensaje(self, mensaje):
        self.socket_cliente.sendall(mensaje.encode())

    def recibir_mensajes(self):
        while True:
            datos = self.socket_cliente.recv(1024).decode()
            print("\nMensaje recibido:", datos)

    def desconectar(self):
        self.socket_cliente.close()

host = 'localhost'
puerto = 8888

cliente = Cliente(host, puerto)
cliente.conectar()

while True:
    mensaje = input("Ingrese un mensaje para el servidor: ")
    cliente.enviar_mensaje(mensaje)
