from flask import Flask, request, render_template
import requests
import socket
import threading

messages = []

app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '10.19.254.160'
server_port = 9999
try:
    s.connect((server_ip, server_port))
    print("Connected to server")
except ConnectionRefusedError:
    print("Failed to connect to the server")

def receive_messages():
    while True:
        try:
            # Receive and print messages from the server
            message = s.recv(1024).decode()
            if not message:
                break
            print(message)
            messages.append(message)
            return render_template('index.html', messages=messages) 
        except:
            print("Connection closed by the server.")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    print(f"User entered: {user_input}")

    send_to_others(f"{user_input}")
    
    # Render the HTML with the server response
    return render_template('index.html', message=f'You entered: {user_input}')


def send_to_others(message):
    try:
        s.sendall(message.encode())
    except:
        print("Error sending message to server")

if __name__ == '__main__':
    app.run(debug=True)
