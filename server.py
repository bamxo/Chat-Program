import socket
import argparse

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}

    def start(self):
        try:
            self.server_socket = socket.socket()
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server is listening on {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.handle_client(client_socket, client_address)
        except KeyboardInterrupt:
            print("\nServer terminated.")
            exit()
        except Exception as e:
            print("Error:", e)
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        try:
            data = client_socket.recv(1024).decode()
            if data.startswith("REGISTER"):
                # Extract client information from the registration message
                lines = data.split("\r\n")
                client_id = lines[1].split(": ")[1]
                client_ip = lines[2].split(": ")[1]
                client_port = int(lines[3].split(": ")[1])
                # Store client information
                self.clients[client_id] = (client_ip, client_port)
                print(f"REGISTER: {client_id} from {client_ip}:{client_port} received")

                # Send registration acknowledgment back to the client
                regack_message = f"REGACK\r\nclientID: {client_id}\r\nIP: {client_ip}\r\nPort: {client_port}\r\n\r\n"
                client_socket.send(regack_message.encode())
            elif data.startswith("BRIDGE"):
                if len(self.clients) == 1:
                    # If there's only one client, respond with an empty BRIDGEACK
                    client_id = data.split("\r\n")[1].split(": ")[1]
                    client_ip = client_address[0]
                    client_port = client_address[1]
                    print(f"BRIDGE : {client_id} {client_ip}:{self.clients[client_id][1]}")

                    # Sending Empty BRIDGEACK
                    bridgeack_message = "BRIDGEACK\r\nclientID: \r\nIP: \r\nPort: \r\n\r\n"
                    client_socket.send(bridgeack_message.encode())
                else:
                    # If there are multiple clients, respond with BRIDGEACK containing the first client's information
                    client_ids = " ".join([f"{client_id} {client[0]}:{client[1]}" for client_id, client in self.clients.items()])
                    print(f"BRIDGE  : {client_ids}")

                    # Sending Full BRIDGEACK
                    first_client_id, (first_client_ip, first_client_port) = next(iter(self.clients.items()))
                    bridgeack_message = f"BRIDGEACK\r\nclientID: {first_client_id}\r\nIP: {first_client_ip}\r\nPort: {first_client_port}\r\n\r\n"
                    client_socket.send(bridgeack_message.encode())
        except Exception as e:
            print("Error handling client:", e)
        finally:
            client_socket.close()
            
def main():
    parser = argparse.ArgumentParser(description="Server for chat program")
    parser.add_argument("--port", help="Port number", type=int, required=True)
    args = parser.parse_args()

    host = "127.0.0.1"
    port = args.port
    server = Server(host, port)
    server.start()

if __name__ == "__main__":
    main()