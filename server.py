import socketserver
import threading
from flask import Flask, render_template, request

clients = []  # List to keep track of connected clients

class ChatHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Add the new client connection to the list of clients
        username = self.request.recv(1024).decode()
        clients.append(self.request)
        print(f"{self.client_address}/{username} connected.")
        
        try:
            while True:
                # Receive a message from the client
                message = self.request.recv(1024).decode()
                if not message:
                    break  # Client disconnected
                print(f"Received from {username}: {message}")
                
                # Broadcast the message to all connected clients
                broadcast_message(f"{username} says: {message}", self.request)
        except ConnectionResetError:
            print(f"{self.client_address} disconnected unexpectedly.")
        finally:
            clients.remove(self.request)
            print(f"{self.client_address} disconnected.")
            self.request.close()

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
