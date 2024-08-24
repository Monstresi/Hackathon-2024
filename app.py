from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
socketio = SocketIO(app)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_ip = s.getsockname()[0]
server_ip = '207.148.86.25'
server_port = 9999
messages = []
usernames = []
result = None
username = ''

try:
    s.connect((server_ip, server_port))
    print("Connected to server")
except ConnectionRefusedError:
    print("Failed to connect to the server")

def receive_messages():
    global username
    while True:
        try:
            # Receive and broadcast messages from the server to all clients
            message = s.recv(1024).decode()
            if not message:
                break
            print(message)
            
            if message[:11] == 'PKT_MSG_VTE':
                global usernames
                usernames = message.split(';')[1].split(':')
                socketio.emit('redirect', {'url': '/voting'})
            elif message[:11] == 'PKT_MSG_RES':
                global result
                result = message.split(':')[1]
                socketio.emit('redirect', {'url': '/results'})
            elif message[:11] == 'PKT_MSG_STR':  # Start showing the image
                item_number = message.split(':')[1]
                imposter_username = message.split(':')[2]
                print("IMAGES ARE BEING DISPLAYED NOW")

                if username == imposter_username:
                    print("You are the imposter!")
                    continue
                socketio.emit('show_image', {'item_number': item_number})
                continue

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
    global usernames
    print(f"Printing usernames now: {usernames}")
    return render_template('voting.html', usernames=usernames)

@app.route('/results')
def results():
    global result
    return render_template('result.html', result=result)

@socketio.on('send_message')
def handle_send_message(data):
    global username
    message = data['msg']
    print(f"User entered: {message}")

    if username == '':
        username = message
        print(f"Username set to: {username}")
    
    # Send the message to the server
    send_to_others(message)

    # Emit the message back to all connected WebSocket clients
    socketio.emit('message', {'msg': f'You: {message}'})

@socketio.on('send_username')
def collate_usernames(data):
    username = data['usr']
    print(f"Username entered: {username}")
    protocol = 'PKT_MSG_USRVTE'
    msg_packet = f"{protocol}:{username}"
    send_to_others(msg_packet)

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
