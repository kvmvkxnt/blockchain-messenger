import socket
import threading
from utils.logger import Logger

CHUNK_SIZE = 4096  # Size of each chunk for data transfer
log = Logger("sockets")


class P2PSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self, handler):
        """Start a server socket."""
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        log.info(f"Listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients, args=(handler,)).start()

    def accept_clients(self, handler):
        """Accept incoming client connections."""
        while True:
            conn, addr = self.socket.accept()
            log.info(f"Connected to {addr}")
            threading.Thread(target=handler, args=(conn,)).start()

    def send_message(self, conn, message):
        """Send large message in chunks."""
        data = message.encode('utf-8')
        total_size = len(data)
        conn.sendall(f"{total_size}".encode('utf-8').ljust(CHUNK_SIZE))
        for i in range(0, len(data), CHUNK_SIZE):
            conn.sendall(data[i:i + CHUNK_SIZE])

    def receive_message(self, conn):
        """Receive large message in chunks."""
        try:
            total_size = int(conn.recv(CHUNK_SIZE).strip().decode('utf-8'))
            received_data = b""
            while len(received_data) < total_size:
                chunk = conn.recv(CHUNK_SIZE)
                if not chunk:
                    break
                received_data += chunk
            return received_data.decode('utf-8')
        except Exception as e:
            log.error(f"Error receiving data: {e}")
            return None
