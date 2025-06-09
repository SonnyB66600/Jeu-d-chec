import socket
import threading


class ChessServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.clients = []
        self.colors = ['blanc', 'noir']

    def handle_client(self, client_socket, client_address, color):
        client_socket.send(color.encode('utf-8'))
        while True:
            try:
                move = client_socket.recv(1024).decode('utf-8')
                if not move:
                    break
                self.broadcast(move, client_socket)
            except ConnectionResetError:
                break

        client_socket.close()
        self.clients.remove(client_socket)

    def broadcast(self, move, from_client):
        for client in self.clients:
            if client != from_client:
                client.send(move.encode('utf-8'))

    def start(self):
        print("Server started and waiting for connections...")
        while len(self.clients) < 2:
            client_socket, client_address = self.server.accept()
            self.clients.append(client_socket)
            print(f"Connection from {client_address}")

        for i, client_socket in enumerate(self.clients):
            color = self.colors[i]
            threading.Thread(target=self.handle_client, args=(client_socket, None, color)).start()


if __name__ == "__main__":
    server = ChessServer()
    server.start()