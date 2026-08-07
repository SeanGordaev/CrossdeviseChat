
import socket
import json, threading
from pathlib import Path

class Client:
    def __init__(self):
        FILE_DIR = Path(__file__).resolve().parent # Where is the current file
        CONFIG_PATH = FILE_DIR / "config.json" # Server Info

        self.chat: list[str] = []

        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        HOST = data["connect-to-ip-local"]
        PORT = data["connect-to-port-local"]

                
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Client:
            Client.connect((HOST, int(PORT)))

            Messages = threading.Thread(target=self.GetAllMessage, args=(Client,))
            Messages.start()

            while True:

                text = input("Enter Text: ")
                Data = text.encode()
                Client.send(len(Data).to_bytes(2, "big") + Data)


    def recv_exact(self, conn: socket.socket, size):
        data_record = b""
        data = data_record

        while len(data_record) < size:
            data = conn.recv(size - len(data_record))

            if not data:
                raise ConnectionError("Connection closed before receiving all data")

            data_record += data

        return data_record


    def GetAllMessage(self, conn: socket.socket):
        while True:
            try:
                data_size = self.recv_exact(conn, 2) # First 2 bytes - the size of the message
                file_size = int.from_bytes(data_size, "big")
                data_record = self.recv_exact(conn, file_size)
            except ConnectionError:
                break

            message = data_record.decode()
            self.chat.append(message)
            
        conn.close()

if __name__ == "__main__":
    C = Client()