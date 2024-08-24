import socket
import threading

def receive_messages(sock):
    while True:
        try:
            # Receive and print messages from the server
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            print("Connection closed by the server.")
            break

def main():
    host = '10.19.254.160' #input("Enter server IP: ")
    port = 9999

    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    username = input("Enter a username: ")
    sock.sendall(username.encode())

    # Start a thread for receiving messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()

    try:
        while True:
            # Send messages to the server
            message = input()
            sock.sendall(message.encode())
    except:
        print("Connection closed.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
