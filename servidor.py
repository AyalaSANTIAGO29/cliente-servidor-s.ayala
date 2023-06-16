import socket
import threading

class Servidor:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.socket_servidor = None
        self.clientes = []
        self.candado = threading.Lock()

    def iniciar(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.puerto))
        self.socket_servidor.listen(5)
        print("Servidor en ejecución en {}:{}".format(self.host, self.puerto))

        while True:
            cliente, direccion = self.socket_servidor.accept()
            self.clientes.append(cliente)
            print("Nueva conexión entrante desde:", direccion)
            hilo_cliente = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            hilo_cliente.start()
            hilo_envio = threading.Thread(target=self.enviar_mensajes, args=(cliente,))
            hilo_envio.start()

    def manejar_cliente(self, cliente):
        while True:
            try:
                datos = cliente.recv(1024).decode()
                if datos:
                    print("Mensaje recibido de {}: {}".format(cliente.getpeername(), datos))
                else:
                    print("Cliente desconectado:", cliente.getpeername())
                    self.clientes.remove(cliente)
                    cliente.close()
                    break
            except ConnectionResetError:
                print("Cliente desconectado inesperadamente:", cliente.getpeername())
                self.clientes.remove(cliente)
                cliente.close()
                break

    def enviar_mensajes(self, cliente):
        while True:
            mensaje_servidor = input("Ingrese un mensaje desde el servidor: ")
            cliente.sendall(mensaje_servidor.encode())

    def enviar_mensaje_a_clientes(self, mensaje):
        with self.candado:
            for cliente in self.clientes:
                try:
                    cliente.sendall(mensaje.encode())
                except ConnectionResetError:
                    print("Error al enviar mensaje a:", cliente.getpeername())

    def detener(self):
        for cliente in self.clientes:
            cliente.close()
        self.socket_servidor.close()

host = 'localhost'
puerto = 8888

servidor = Servidor(host, puerto)

try:
    servidor.iniciar()
except KeyboardInterrupt:
    servidor.detener()
