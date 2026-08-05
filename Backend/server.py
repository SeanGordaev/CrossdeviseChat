import socket
import json
import threading


with open(r'Frontend\config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def SaveMessage(text: str):
    with open(r'Backend\messages.txt', 'a', encoding='utf-8') as m:
        m.write(text)


def recv_exact(conn: socket.socket, size):
    data_record = b""
    data = data_record

    while len(data_record) < size:
        data = conn.recv(size - len(data_record))

        if not data:
            raise ConnectionError("Connection closed before receiving all data")

        data_record += data

    return data_record


def GetMessage(conn: socket.socket):
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

        message = data_record.decode()
        if message == "EXIT_USER_NOW": 
            break
        SaveMessage(message)
    conn.close()

def GetAllMessage() -> bytes:
    with open(r'Backend\messages.txt', 'r', encoding='utf-8') as m:
        return m.read().encode('utf-8')

def UserIn(conn: socket.socket):
    conn.sendall(GetAllMessage())
            
    DetectMessage = threading.Thread(target=GetMessage, args=(conn,))
    DetectMessage.start()


HOST = data["ip-local-server"]  # Standard loopback interface address (localhost)
PORT = data["port-local-server"]  # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()


    while True:
        conn, address = s.accept()

        User = threading.Thread(target=UserIn, args=(conn,))
        User.start()

    