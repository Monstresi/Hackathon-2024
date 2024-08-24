import socketserver
import threading
import json
import sys
import random

clients = []   # List to keep track of connected clients
usernames = []
messages = []

file_lock = threading.Lock()

# Check if there are enough arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <argument>")
    sys.exit(1)
else:
    # Get the argument (second item in the list)
    max_clients = sys.argv[1]


class ChatHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Add the new client connection to the list of clients
        username = self.request.recv(1024).decode()
        usernames.append(username)
        clients.append(self.request)
        with file_lock:
            with open('users.json', 'w') as file:
                json.dump(usernames, file, indent=4)
        print(f"{self.client_address}/{username} connected.")

        # If everyone has connected
        if len(clients) == max_clients:
            start_packet = "PKT_MSG_STR"
            random_number = random.randint(1, 5)
            voting_packet = f"{start_packet}:{random_number}"
            print(f"Broadcasting: {broadcast_msg}")
            broadcast_all(broadcast_msg, self.request)
        
        try:
            while True:
                # Receive a message from the client
                message = self.request.recv(1024).decode()
                if not message:
                    break  # Client disconnected
                print(f"Received from {username}: {message}")
                messages.append(f"{username}: {message}")
                
                # Broadcast the message to all connected clients
                broadcast_message(f"{username} says: {message}", self.request)

                if len(messages) > 20:
                    voting_packet = "PKT_MSG_VTE"
                    # "PKT_MSG_VTE;Hassan:Ronaldo:Messi:Salah:Kane"
                    names = ":".join(usernames)
                    broadcast_msg = f"{voting_packet};{names}"
                    print(f"Broadcasting: {broadcast_msg}")
                    broadcast_all(broadcast_msg, self.request)
        except ConnectionResetError:
            print(f"{self.client_address} disconnected unexpectedly.")
        finally:
            clients.remove(self.request)
            print(f"{self.client_address} disconnected.")
            self.request.close()

def broadcast_all(message, sender_socket):
    for client in clients:        
        try:
            client.sendall(message.encode())
        except:
            # Handle broken connection during broadcast
            clients.remove(client)

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Do not send the message back to the sender
            try:
                client.sendall(message.encode())
            except:
                # Handle broken connection during broadcast
                clients.remove(client)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    socketserver.TCPServer.allow_reuse_address = True
    with ThreadedTCPServer((HOST, PORT), ChatHandler) as server:
        print("Chat room server started on port", PORT)
        server.serve_forever()