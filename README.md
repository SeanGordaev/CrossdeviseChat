# CrossdeviseChat

[English](README.md) | [Русский](README_RU.md)

**CrossdeviseChat** is a lightweight self-hosted chat application for devices connected to the same local network (LAN).

One computer — or a dedicated machine on the LAN — runs the **server** from the `Backend` folder. Other computers run the **client** from the `Frontend` folder and connect to the server using its local IP address and port.

The goal of the project is to provide a simple local chat that does not depend on external messaging services or cloud infrastructure.

> 🚧 **Work in progress:** CrossdeviseChat is still under development. Its protocol, interface, and features may change.

---

## How It Works

CrossdeviseChat uses a **client-server architecture**:

```text
              Local Area Network
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────┐             ┌────▼─────┐
   │ Client A │             │ Client B │
   └────┬─────┘             └────┬─────┘
        │                         │
        └──────────┬──────────────┘
                   │
              TCP connections
                   │
             ┌─────▼─────┐
             │   Server  │
             │   / Host  │
             └─────┬─────┘
                   │
             messages.txt
```

The server:

- listens for incoming TCP connections;
- keeps track of connected clients;
- creates a separate thread for each connected client;
- receives messages from clients;
- broadcasts received messages to all currently connected clients;
- stores received messages in `Backend/messages.txt`.

The host can be:

- one of the computers participating in the chat;
- a dedicated computer;
- a small local server connected to the LAN.

No Internet connection is required for communication inside the local network.

---

## Current Features

The current version includes:

- TCP-based client-server communication;
- multiple simultaneous client connections;
- persistent TCP connections;
- real-time message broadcasting;
- a shared chat for connected clients;
- a simple desktop GUI built with Tkinter;
- sending messages with the **Send** button or **Enter**;
- server-side message storage in `messages.txt`;
- separate server and client configuration files;
- 2-byte length-prefixed message framing;
- multithreaded server-side client handling.

---

## Project Structure

All **server-side files** are stored in `Backend/`.

All **client-side files** are stored in `Frontend/`.

```text
CrossdeviseChat/
│
├── Backend/
│   ├── config.json
│   ├── messages.txt
│   ├── server.py
│   └── start_servet.bat
│
├── Frontend/
│   ├── chat_client.py
│   ├── chat_client_gui.py
│   ├── config.json
│   └── start_client.bat
│
├── README.md
└── README_RU.md
```

> **Note:** the current server launcher is named `start_servet.bat`. Renaming it to `start_server.bat` is recommended for consistency.

### Backend

The `Backend` folder contains everything required to run the server.

- `server.py` — server networking logic;
- `config.json` — local IP address and port used by the server;
- `messages.txt` — simple persistent message storage;
- `start_servet.bat` — Windows launcher for the server.

### Frontend

The `Frontend` folder contains everything required to run a client.

- `chat_client.py` — client networking logic;
- `chat_client_gui.py` — Tkinter graphical interface;
- `config.json` — address of the server the client should connect to;
- `start_client.bat` — Windows launcher for the client GUI.

---

## Message Protocol

CrossdeviseChat uses TCP sockets.

TCP is a **byte stream**, so one `recv()` call is not guaranteed to contain exactly one complete message. To solve this, CrossdeviseChat prefixes every message with its size:

```text
┌──────────────────┬────────────────────────────┐
│ Message Length   │ Message Data               │
│ 2 bytes          │ N bytes                    │
└──────────────────┴────────────────────────────┘
```

The first **2 bytes**, stored in big-endian byte order, contain the message size.

The receiver:

1. reads exactly 2 bytes;
2. converts them into the message length;
3. reads exactly that number of bytes;
4. decodes the received data as text.

With a 2-byte unsigned length field, a single framed message can contain up to **65,535 bytes**.

---

## Requirements

- Python 3
- Tkinter
- TCP/IP support
- devices connected to the same local network
- firewall/network rules that allow the selected TCP port

The server and clients must be able to reach each other through the LAN.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SeanGordaev/CrossdeviseChat.git
cd CrossdeviseChat
```

---

### 2. Install Python and required libraries

CrossdeviseChat currently uses only modules from the Python standard library:

- `socket`
- `json`
- `threading`
- `pathlib`
- `tkinter`

Because of this, **no additional packages need to be installed with `pip`**.

On Windows, Python can be installed directly from the command line with WinGet:

```powershell
winget install --id Python.Python.3.14 --exact
```

After the installation finishes, close and reopen the terminal, then verify Python:

```powershell
python --version
```

You can also verify that Tkinter is available:

```powershell
python -m tkinter
```

If Tkinter is installed correctly, a small test window should open.

If Python is already installed and both commands work, you can skip this step.

---

### 3. Configure the server

Open:

```text
Backend/config.json
```

Example:

```json
{
    "your-ip-local": "192.168.1.100",
    "your-port-local": "5050"
}
```

This file tells the server **who it is on the local network**:

```text
Backend/config.json
        │
        └── "Who am I?"
            │
            ├── Local server IP
            └── Local server port
```

`your-ip-local` should be the local IP address of the computer that will host the chat.

`your-port-local` is the TCP port on which the server will listen for clients.

For example:

```text
192.168.1.100:5050
```

---

### 4. Configure the client

Open:

```text
Frontend/config.json
```

Example:

```json
{
    "connect-to-ip-local": "192.168.1.100",
    "connect-to-port-local": "5050"
}
```

This file tells the client **who it should connect to**:

```text
Frontend/config.json
        │
        └── "Who do I connect to?"
            │
            ├── Server IP
            └── Server port
```

The client values should normally match the IP address and port configured in `Backend/config.json` on the server computer.

If several computers want to join the same chat, every client should point to the same server.

---

## Starting the Server

### Windows — quick launch

Open the `Backend` folder and run:

```text
start_servet.bat
```

The batch file changes the working directory to `Backend` and starts:

```bash
python server.py
```

### Manual launch

From the project root:

```bash
cd Backend
python server.py
```

Keep the server running while clients are connected.

---

## Starting a Client

Before starting a client, make sure `Frontend/config.json` contains the correct server IP address and port.

### Windows — quick launch

Open the `Frontend` folder and run:

```text
start_client.bat
```

The batch file changes the working directory to `Frontend` and starts the GUI:

```bash
python chat_client_gui.py
```

### Manual launch

From the project root:

```bash
cd Frontend
python chat_client_gui.py
```

Repeat this on every computer that should join the chat.

---

## Example Network

```text
Router
192.168.1.1
     │
     ├── Server / Host
     │   192.168.1.100:5050
     │
     ├── Client A
     │   192.168.1.101
     │
     ├── Client B
     │   192.168.1.102
     │
     └── Client C
         192.168.1.103
```

All clients connect to:

```text
192.168.1.100:5050
```

Clients do not need to connect directly to each other:

```text
Client A ──┐
           │
Client B ──┼──► Server ──► Broadcast to connected clients
           │
Client C ──┘
```

---

## Concurrency

The server creates a separate thread for every connected client.

The shared client list is protected with a thread lock while connections are added, removed, or copied for broadcasting.

This allows multiple clients to remain connected to the same server at the same time.

---

## Message Storage

Every regular message received by the server is appended to:

```text
Backend/messages.txt
```

This provides basic server-side persistence.

Currently, stored messages are **not automatically sent to newly connected clients**. A client sees messages broadcast while it is connected.

---

## Current Limitations

CrossdeviseChat is still an experimental project.

The current version does not yet provide:

- usernames;
- timestamps;
- automatic chat-history synchronization;
- automatic LAN server discovery;
- automatic reconnection;
- authentication;
- encrypted communication;
- file transfer;
- a user-friendly configuration screen;
- complete graceful shutdown/disconnect handling from the GUI.

The server also recognizes the special message:

```text
EXIT_USER_NOW
```

as a disconnect command, but the current GUI does not yet expose this as a complete user-facing disconnect system.

---

## Roadmap

Already implemented:

- [x] TCP client-server communication
- [x] Multiple simultaneous clients
- [x] Persistent TCP connections
- [x] Real-time message broadcasting
- [x] Basic message storage
- [x] Tkinter desktop GUI
- [x] Send with button or Enter
- [x] Separate Backend/Frontend configuration
- [x] 2-byte length-prefixed message framing
- [x] Multithreaded server
- [x] Windows `.bat` launchers for server and client

Planned:

- [ ] Usernames
- [ ] Join/leave notifications
- [ ] Timestamps
- [ ] Send stored chat history to newly connected clients
- [ ] Automatic server discovery on the LAN
- [ ] Automatic reconnection
- [ ] Better error handling
- [ ] Graceful GUI disconnect
- [ ] Configuration screen
- [ ] Authentication
- [ ] Message encryption
- [ ] File transfer
- [ ] Cross-platform launch scripts / packaging

---

## Security

CrossdeviseChat is currently intended for use inside **trusted local networks**.

The current protocol does not provide authentication or encryption. Because of this, the application should **not be exposed directly to the public Internet**.

Possible future improvements include:

- client authentication;
- encrypted connections;
- permissions;
- message validation;
- connection limits and abuse protection.

---

## Project Motivation

Most modern chat applications depend on external servers and Internet connectivity.

CrossdeviseChat explores a different approach:

> **If devices are already connected to the same local network, they should be able to communicate through infrastructure controlled by the users themselves.**

The project is also an opportunity to explore:

- TCP sockets;
- client-server architecture;
- message framing;
- multithreading;
- concurrent connections;
- local IP addressing;
- network protocols;
- server-side broadcasting;
- GUI/network interaction;
- connection lifecycle management.

---

## Contributing

Suggestions, bug reports, experiments, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Open a pull request.

---

## Author

Created by **Sean Gordaev**

GitHub: `SeanGordaev`
