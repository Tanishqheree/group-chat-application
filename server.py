import socket
import threading

class Server:
    clients = {}  # client_socket: client_name

    def __init__(self, host='127.0.0.1', port=5566):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"[+] Server started on {host}:{port}")
        self.listen()

    def broadcast(self, message, source_socket=None):
        for client_socket in self.clients:
            if client_socket != source_socket:
                try:
                    client_socket.send(message.encode())
                except:
                    client_socket.close()
                    del self.clients[client_socket]

    def handle_client(self, client_socket):
        name = client_socket.recv(1024).decode()
        self.clients[client_socket] = name
        print(f"[+] {name} joined the chat")
        self.broadcast(f"{name} has joined the chat!")

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"{name}: {message}")
                    self.broadcast(f"{name}: {message}", client_socket)
                else:
                    raise Exception("Client disconnected")
            except:
                print(f"[-] {name} disconnected")
                self.broadcast(f"{name} has left the chat")
                client_socket.close()
                del self.clients[client_socket]
                break

    def listen(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[+] New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    Server()
