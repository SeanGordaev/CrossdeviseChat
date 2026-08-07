# CrossdeviseChat

**CrossdeviseChat** is a lightweight local network chat application designed for communication between devices connected to the same LAN.

One computer — or a dedicated machine on the local network — acts as the **host/server**. Other computers connect to it as clients, allowing everyone on the network to participate in a shared chat.

The main goal of the project is to build a simple, self-hosted chat system that works entirely inside a local network without depending on external messaging services or cloud infrastructure.

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
              TCP connection
                   │
             ┌─────▼─────┐
             │   Server  │
             │   / Host  │
             └─────┬─────┘
                   │
             Message storage
```

The server listens for incoming TCP connections from devices on the LAN.

Clients connect to the server using its local IP address and port. Messages are sent to the server, which acts as the central point of communication for the chat.

This means that the host can be:

* one of the computers participating in the chat;
* a dedicated computer;
* a small home server connected to the LAN.

No Internet connection is required for communication inside the local network.

---

## Current Goals

The project is currently focused on creating the basic networking infrastructure for a LAN chat.

The intended functionality includes:

* communication between multiple computers on the same local network;
* one central host/server;
* multiple simultaneous clients;
* a shared chat visible to connected users;
* persistent TCP connections;
* reliable message transmission;
* basic message history;
* simple configuration of server IP and port.

---

## Current Architecture

The project is divided into two main parts:

```text
CrossdeviseChat/
│
├── Backend/
│   ├── server.py
│   ├── config.json
│   └── messages.txt
│
├── Frontend/
│   └── ...
│
└── README.md
```

### Backend

The backend is responsible for:

* accepting client connections;
* receiving messages;
* managing connected clients;
* storing messages;
* providing the central communication point for the network.

### Frontend

The frontend/client is responsible for:

* connecting to the host;
* sending messages;
* receiving chat data;
* displaying messages to the user.

---

## Message Protocol

CrossdeviseChat uses TCP sockets for communication.

Messages are transferred using a simple framing system:

```text
┌──────────────────┬────────────────────────────┐
│ Message Length   │ Message Data               │
│ 2 bytes          │ N bytes                    │
└──────────────────┴────────────────────────────┘
```

The first **2 bytes** contain the size of the message.

The receiver then knows exactly how many bytes must be read for the complete message.

This avoids relying on individual `recv()` calls to correspond to individual messages, since TCP is a byte stream rather than a message-based protocol.

---

## Requirements

The project currently requires:

* Python 3
* a local network connection
* TCP/IP connectivity between devices

The host and clients must be able to reach each other through the LAN.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SeanGordaev/CrossdeviseChat.git
cd CrossdeviseChat
```

### 2. Configure the connection

CrossdeviseChat uses two separate configuration files: one for the server and one for the client.

Backend configuration

Inside Backend/config.json:

``` json 
{
    "your-ip-local": "...",
    "your-port-local": "..."
}
```

This configuration tells the server who it is on the local network — which local IP address and port it should use for accepting incoming client connections.

For example:

``` json 
{
    "your-ip-local": "192.168.1.100",
    "your-port-local": "5050"
}
```

In this example, the server will use:

192.168.1.100:5050
Frontend configuration

Inside Frontend/config.json:

``` json
{
    "connect-to-ip-local": "...",
    "connect-to-port-local": "..."
}
```

This configuration tells the client who it should connect to.

The IP address and port should normally match the values configured on the server.

For example, if the server configuration is:

``` json
{
    "your-ip-local": "192.168.1.100",
    "your-port-local": "5050"
}
```

Then the client configuration should be:

``` json
{
    "connect-to-ip-local": "192.168.1.100",
    "connect-to-port-local": "5050"
}
```

In simple terms:

```text
Backend/config.json
        │
        └── "Who am I?" → Server IP and port

Frontend/config.json
        │
        └── "Who do I connect to?" → Server IP and port
```

If several computers want to join the same chat, each client should set its connect-to-ip-local and connect-to-port-local values to the IP address and port of the computer running the server.

### 3. Start the server

```bash
python Backend/server.py
```

The server should now begin listening for connections from other computers on the network.

### 4. Connect clients

Client devices should connect to:

```text
SERVER_IP:SERVER_PORT
```

For example:

```text
192.168.1.100:5050
```

All clients must be able to reach the host through the local network.

---

## Example Network

For example, a home network could look like this:

```text
Router
192.168.1.1
     │
     ├── Chat Server
     │   192.168.1.100:5050
     │
     ├── PC #1
     │   192.168.1.101
     │
     ├── PC #2
     │   192.168.1.102
     │
     └── Laptop
         192.168.1.103
```

All clients connect directly to:

```text
192.168.1.100:5050
```

The server then handles communication between them.

---

## Roadmap

CrossdeviseChat is still under development.

Planned improvements include:

* [ ] Real-time message broadcasting
* [ ] Multiple simultaneous users
* [ ] Usernames
* [ ] Join/leave notifications
* [ ] Better message history
* [ ] Timestamps
* [ ] Improved client interface
* [ ] Automatic server discovery on the LAN
* [ ] Better configuration management
* [ ] Graceful client disconnection
* [ ] Error handling and reconnection
* [ ] Message protocol improvements
* [ ] Optional authentication
* [ ] Optional message encryption
* [ ] File transfer
* [ ] Cross-platform support

---

## Security

CrossdeviseChat is intended primarily for communication inside **trusted local networks**.

The current development version should not be exposed directly to the public Internet.

Future versions may introduce features such as:

* client authentication;
* encrypted communication;
* permissions;
* safer message validation.

---

## Project Motivation

Most modern chat applications depend on external servers and Internet connectivity.

CrossdeviseChat explores a different approach:

> **If the devices are already connected to the same network, they should be able to communicate directly through infrastructure controlled by the users themselves.**

The project is also an opportunity to explore networking concepts such as:

* TCP sockets;
* client-server architecture;
* message framing;
* concurrent connections;
* local IP addressing;
* network protocols;
* server-side message handling.

---

## Contributing

The project is in active development.

Suggestions, bug reports, experiments, and improvements are welcome.

If you want to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Open a pull request.

---

## Author

Created by **Sean Gordaev**

GitHub: `SeanGordaev`

---

## Status

> 🚧 **Work in progress**

CrossdeviseChat is currently an experimental project and its architecture, protocol, and features may change during development.
