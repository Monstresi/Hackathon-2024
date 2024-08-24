from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
socketio = SocketIO(app)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '10.19.254.160'
server_port = 9999
messages = []
try:
    s.connect((server_ip, server_port))
    print("Connected to server")
except ConnectionRefusedError:
    print("Failed to connect to the server")

def receive_messages():
    while True:
        try:
            # Receive and broadcast messages from the server to all clients
            message = s.recv(1024).decode()
            if not message:
                break
            print(message)
            if message == 'PKT_MSG_VTE':
                print("LIMIT REACHED")
                socketio.emit('redirect', {'url': '/voting'})
            messages.append(message)
            
            # Emit the message to all connected WebSocket clients
            socketio.emit('message', {'msg': message})
            
        except:
            print("Connection closed by the server.")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

@app.route('/')
def index(flag=False):
    if not flag:
        return render_template('index.html')

@app.route('/voting')
def vote():
    return render_template('voting.html')



@socketio.on('send_message')
def handle_send_message(data):
    message = data['msg']
    print(f"User entered: {message}")
    
    # Send the message to the server
    send_to_others(message)

    # Emit the message back to all connected WebSocket clients
    socketio.emit('message', {'msg': f'You: {message}'})

@app.route('/assets/<filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)

@app.route('/assets/items/<filename>')
def serve_static_items(filename):
    return send_from_directory('assets/items', filename)

def send_to_others(message):
    try:
        messages.append(message)
        s.sendall(message.encode())
    except:
        print("Error sending message to server")

if __name__ == '__main__':
    socketio.run(app, debug=True)