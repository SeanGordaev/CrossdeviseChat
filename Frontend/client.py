
import socket
import json, threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent       # папка Backend
PROJECT_DIR = BASE_DIR.parent                    # папка CrossdeviceChat
CONFIG_PATH = PROJECT_DIR / "config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

HOST = data["connect-to-ip-local"]
PORT = data["connect-to-port-local"]

def recv_exact(conn: socket.socket, size):
    data_record = b""
    data = data_record

    while len(data_record) < size:
        data = conn.recv(size - len(data_record))

        if not data:
            raise ConnectionError("Connection closed before receiving all data")

        data_record += data

    return data_record


def GetAllMessage(conn: socket.socket):
    while True:
        try:
            data_size = recv_exact(conn, 2) # First 2 bytes - the size of the message
        except ConnectionError:
            break

        file_size = int.from_bytes(data_size, "big")
        data_record = b""

        while len(data_record) < file_size:

            data = conn.recv(file_size - len(data_record))

            if not data:
                break

            data_record += data

        message = data_record.decode().split("\n")
        print(message[-1])
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, int(PORT)))

    Messages = threading.Thread(target=GetAllMessage, args=(c,))
    Messages.start()

    text = input("Enter Text: ")

    c.send(len(text.encode()).to_bytes(2, "big"))
    c.sendall(text.encode())
