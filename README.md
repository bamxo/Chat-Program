# Chat Program with Socket Programming

This chat program, named Basic Chat Protocol, is implemented using socket programming in Python. It allows multiple clients to connect to a server and communicate with each other in real-time.

## Features

- **Server-Client Architecture:** The program follows a client-server architecture where the server manages client connections and facilitates communication between clients.
- **Real-time Messaging:** Clients can send and receive messages in real-time, enabling instant communication.
- **Multi-client Support:** The server supports multiple client connections simultaneously, allowing for group chat functionality.
- **Simple User Interface:** The program provides a command-line interface (CLI) for ease of use and interaction.

## Getting Started

### Prerequisites
- Python 3.x installed on your system.

### Running the Program
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/chat-program.git

## Usage

### Commands
- `/id`: Prints username.
- `/register`: Connects to the server.
- `/bridge`: Connects to clients.
- `/quit`: Quits chatting mode.

### Modes
- **Read Mode:** Receives messages from other clients.
- **Write Mode:** Sends messages to other clients.

## Chat Protocol

The chat protocol follows a simple message format:
CHATREQ\r\nclientID: [Client_ID]\r\n\r\n

This message format includes a `clientID` header to identify clients during chat sessions.

## TCP/IP Protocol Stack Layer

The Chat Protocol operates at the application layer of the TCP/IP protocol stack, which is suitable for implementing chat applications.

## Architecture

The project follows a Client-Server architecture. The server listens for incoming connections from clients and handles their requests. When in Chat mode, the peers operate as both clients and servers, allowing bidirectional communication.

## Connection Type

- **Client-Server client communication:** Non-persistent TCP connections are used, where each connection is short-lived and closed after communication.
- **Peer-Peer client program:** Persistent TCP connection is used for the duration of the chat session.

## Half-Duplex Communication

The chatting aspect of the program follows half-duplex communication, allowing data transmission in both directions alternately.
