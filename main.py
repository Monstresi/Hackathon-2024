import socket

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

def host_game(host, port):
    s = create_socket()
    s.bind((host, port))
    s.listen(1)
    print("Waiting for player...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    while True:
        move = input("Enter your move: ")
        conn.sendall(move.encode())
        response = conn.recv(1024).decode()
        print(f"Opponent's move: {response}")

def join_game(host, port):
    s = create_socket()
    s.connect((host, port))
    print("Connected to the host!")

    while True:
        response = s.recv(1024).decode()
        print(f"Opponent's move: {response}")
        move = input("Enter your move: ")
        s.sendall(move.encode())

def main():
    choice = input("Do you want to (h)ost or (j)oin a game? ")
    if choice == 'h':
        host_game('localhost', 9999)
    else:
        join_game('localhost', 9999)    

if __name__ == "__main__":
    main()