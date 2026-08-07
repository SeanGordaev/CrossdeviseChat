import socket
import json
import threading
from pathlib import Path

class Server:
    def __init__(self):
        FILE_DIR = Path(__file__).resolve().parent # Where is the current file

        self.CONFIG_PATH = FILE_DIR / "config.json" # Server Info
        self.MESSAGE_PATH = FILE_DIR / "messages.txt" # All Messages

        with open(self.CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        
        HOST = data["your-ip-local"]
        PORT = data["your-port-local"] 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, int(PORT)))
            s.listen()


            while True:
                conn, address = s.accept()

                User = threading.Thread(target=self.UserIn, args=(conn,))
                User.start()


    def SaveMessage(self, text: str):
        with open(self.MESSAGE_PATH, 'a', encoding='utf-8') as m:
            m.write(text)


    def recv_exact(self, conn: socket.socket, size):
        data_record = b""
        data = data_record

        while len(data_record) < size:
            data = conn.recv(size - len(data_record))

            if not data:
                raise ConnectionError("Connection closed before receiving all data")

            data_record += data

        return data_record


    def GetMessage(self, conn: socket.socket):
        while True:
            try:
                data_size = self.recv_exact(conn, 2) # First 2 bytes - the size of the message
            except ConnectionError:
                break
            file_size = int.from_bytes(data_size, "big")
            data_record = b""

            while len(data_record) < file_size:

                data = conn.recv(file_size - len(data_record))

                if not data:
                    break

                data_record += data

            message = data_record.decode()
            if message == "EXIT_USER_NOW": 
                break
            self.SaveMessage(message)
        conn.close()

    def GetAllMessage(self) -> bytes:
        with open(self.CONFIG_PATH, 'r', encoding='utf-8') as m:
            return m.read().encode('utf-8')

    def UserIn(self, conn: socket.socket):
        AllMessage = self.GetAllMessage()
        conn.sendall(len(AllMessage).to_bytes(2, "big"))
        conn.sendall(AllMessage)
                
        DetectMessage = threading.Thread(target=self.GetMessage, args=(conn,))
        DetectMessage.start()


    