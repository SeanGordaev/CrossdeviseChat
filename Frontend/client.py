
import socket
import json

with open(r'Frontend\config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

HOST = data["ip-local-server"]  # Standard loopback interface address (localhost)
PORT = data["port-local-server"]  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, PORT))
    
    # Send data (must be encoded to bytes)
    c.sendall(b"Hello, Server!")
    
    # Receive response
    data = c.recv(1024)
    print(f"Received: {data.decode()}")
