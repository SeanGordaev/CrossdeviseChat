# CrossdeviseChat
# Copyright (C) 2026 Sean Gordaev
#
# This file is part of CrossdeviseChat.
# CrossdeviseChat is licensed under the GNU Affero General Public License v3.0.
# See the LICENSE file for details.

import socket
import json
import threading
from pathlib import Path

class Server:
    def __init__(self):
        self.Clients: list[socket.socket] = []
        self.ClientsLock = threading.Lock()
        self.MessageFileLock = threading.Lock()


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

                with self.ClientsLock:
                    self.Clients.append(conn)
                User = threading.Thread(target=self.UserIn, args=(conn, ))
                User.start()


    def SaveMessage(self, text: str):
        with open(self.MESSAGE_PATH, 'a', encoding='utf-8') as m:
            m.write(text + "\n")

    def recv_exact(self, conn: socket.socket, size):
        data_record = b""
        data = data_record

        while len(data_record) < size:
            data = conn.recv(size - len(data_record))

            if not data:
                raise ConnectionError("Connection closed before receiving all data")

            data_record += data

        return data_record

    def Broadcast(self, Data: bytes):
        with self.ClientsLock:
            ClientsCopy = self.Clients.copy()

        for Client in ClientsCopy:
            try:
                Client.sendall(len(Data).to_bytes(2, "big") + Data)
            except OSError:
                continue

    def UserIn(self, conn: socket.socket):
        while True:
            try:
                data_size = self.recv_exact(conn, 2) # First 2 bytes - the size of the message
                file_size = int.from_bytes(data_size, "big")
                data_record = self.recv_exact(conn, file_size)
            except ConnectionError:
                break

            message = data_record.decode()
            if message == "EXIT_USER_NOW": 
                break
            self.Broadcast(data_record)
            self.SaveMessage(message)
        with self.ClientsLock:
            self.Clients.remove(conn)
            conn.close()



if __name__ == "__main__":
    Host = Server()