
import socket
import json, threading
from pathlib import Path

class ChatClient:
    def __init__(self):
        FILE_DIR = Path(__file__).resolve().parent # Where is the current file
        CONFIG_PATH = FILE_DIR / "config.json" # Server Info

        self.__Chat: list[str] = []
        self.__NewMessage = False

        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        HOST = data["connect-to-ip-local"]
        PORT = data["connect-to-port-local"]

        self.__Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__Client.connect((HOST, int(PORT)))

        Messages = threading.Thread(target=self.GetAllMessage)
        Messages.start()

    @property
    def GetChat(self) -> list[str]:
        return self.__Chat

    @property
    def IsThereNewMessage(self) -> bool:
        return self.__NewMessage

    def IReadTheNewMessage(self) -> None:
        self.__NewMessage = False

    def recv_exact(self, conn: socket.socket, size):
        data_record = b""
        data = data_record

        while len(data_record) < size:
            data = conn.recv(size - len(data_record))

            if not data:
                raise ConnectionError("Connection closed before receiving all data")

            data_record += data

        return data_record


    def GetAllMessage(self):
        while True:
            try:
                data_size = self.recv_exact(self.__Client, 2) # First 2 bytes - the size of the message
                file_size = int.from_bytes(data_size, "big")
                data_record = self.recv_exact(self.__Client, file_size)
            except ConnectionError:
                break

            message = data_record.decode()
            self.__Chat.append(message)
            self.__NewMessage = True
            
        self.__Client.close()

    def SendMessage(self, text: str):
        Data = text.encode()
        self.__Client.sendall(len(Data).to_bytes(2, "big") + Data)


if __name__ == "__main__":
    C = Client()