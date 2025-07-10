import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print("\n" + message)
            else:
                break
        except:
            print("Disconnected from server.")
            break

def send_messages(client_socket):
    while True:
        try:
            message = input()
            client_socket.send(message.encode())
        except:
            print("Disconnected.")
            break

def main():
    host = '127.0.0.1'
    port = 5566

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    name = input("Enter your name: ")
    client_socket.send(name.encode())

    print("Connected to the chat. You can start typing...")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket)

if __name__ == "__main__":
    main()
