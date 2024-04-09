import socket
import argparse

class Client:
    def __init__(self, client_id, port, server_address):
        self.client_id = client_id
        self.peer_id = None
        self.port = port
        self.server_address = server_address
        self.sock = None
        self.peer_sock = None
        self.peer_address = None

    def connect_to_server(self):
        self.sock = socket.socket()
        try:
            self.sock.connect(self.server_address)
        except Exception as e:
            print("Error connecting to server:", e)
            exit()
    
    def print_client_id(self):
        print(self.client_id)
        
    def register(self):
        self.connect_to_server()
        message = f"REGISTER\r\nclientID: {self.client_id}\r\nIP: {self.server_address[0]}\r\nPort: {self.port}\r\n\r\n"
        self.sock.send(message.encode())
        #response = self.sock.recv(1024).decode()
        #print(response)
        self.sock.close()

    def bridge(self):
        self.connect_to_server()
        message = f"BRIDGE\r\nclientID: {self.client_id}\r\n\r\n"
        self.sock.send(message.encode())
        response = self.sock.recv(1024).decode()
        #print(response)
        if response == "BRIDGEACK\r\nclientID: \r\nIP: \r\nPort: \r\n\r\n":
            print(f"{self.client_id} IN WAIT MODE")
            self.accept_incoming_connection()
        else:
            # Extracting Peer Information
            lines = response.split("\r\n")
            self.peer_id = lines[1].split(": ")[1]
            peer_ip = lines[2].split(": ")[1]
            peer_port = int(lines[3].split(": ")[1])
            self.peer_address = (peer_ip, peer_port)
        self.sock.close()

    def connect_to_client(self):
        if self.peer_address is None:
            print("Error: Peer information not available. Please bridge first.")
            return
        self.peer_sock = socket.socket()
        try:
            self.peer_sock.connect(self.peer_address)
            sender_info = f"CHATREQ\r\nclientID: {self.client_id}\r\n\r\n"
            self.peer_sock.send(sender_info.encode())
        except Exception as e:
            print("Error connecting to peer:", e)
            exit()
        finally:
            print("IN CHAT MODE")
            self.chat()
        
    def accept_incoming_connection(self):
        try:
            self.sock = socket.socket()
            self.sock.bind(("0.0.0.0", self.port))
            self.sock.listen(1)
            self.peer_sock, addr = self.sock.accept()
            response = self.peer_sock.recv(1024).decode()
            lines = response.split("\r\n")
            self.peer_id = lines[1].split(": ")[1]
            self.sock.close()
            self.receive_messages()
        except Exception as e:
            print("Error accepting incoming connection:", e)
            exit()
    
    def receive_messages(self):
        print("IN READ MODE")
        while True:
            try:
                data = self.peer_sock.recv(1024).decode()
                if data == "/quit":
                    print(f"{self.peer_id} has ended the chat session")
                    print("Exiting program")
                    exit()
                elif data:
                    print(f"{self.peer_id}> {data}")
                    self.chat()
            except KeyboardInterrupt:
                message = "/quit"
                self.peer_sock.send(message.encode())
                print("\nChat session ended")
                print("Exiting program")
                exit()
            except Exception as e:
                print("Error receiving message:", e)
                exit()

    def chat(self):
        print("IN WRITE MODE")
        try:
            while True:
                message = input()
                if message == "/quit":
                    self.peer_sock.send(message.encode())
                    print("Chat session ended")
                    print("Exiting program")
                    exit()
                self.peer_sock.send(message.encode())
                self.receive_messages()
                return
        except KeyboardInterrupt:
            message = "/quit"
            self.peer_sock.send(message.encode())
            print("\nChat session ended")
            print("Exiting program")
            exit()

    def start(self):
        try:
            while True:
            # Logic for waiting for user input and sending approriate messages
                command = input()
                if command.strip() == "/id":
                    self.print_client_id()
                elif command.strip() == "/register":
                    self.register()
                elif command.strip() == "/bridge":
                    self.bridge()
                elif command.strip() == "/chat":
                    self.connect_to_client()
                elif command.strip() == "/quit":
                    print("Terminating the chat client")
                    print("Exiting program")
                    exit()
                else:
                    print("Invalid command.")
        except KeyboardInterrupt:
            print("\nTerminating the chat client")
            print("Exiting program")
            exit()


def main():
    parser = argparse.ArgumentParser(description="Client for chat program")
    parser.add_argument("--id", help="Client ID", required=True)
    parser.add_argument("--port", help="Port number", type=int, required=True)
    parser.add_argument("--server", help="Server address in IP:port format", required=True)
    args = parser.parse_args()

    client_id = args.id
    port = args.port
    server_address_parts = tuple(args.server.split(':'))
    if len(server_address_parts) != 2:
        print("Invalid server address format. Please provide the address in IP:port format.")
        exit()
    server_address= (server_address_parts[0], int(server_address_parts[1]))

    client = Client(client_id, port, server_address)
    client.start()

if __name__ == "__main__":
    main()