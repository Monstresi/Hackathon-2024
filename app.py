from flask import Flask, request, render_template
import requests
import socket

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    print(f"User entered: {user_input}")

    send_to_others(f"User entered: {user_input}")
    
    # Render the HTML with the server response
    return render_template('index.html', message=f'You entered: {user_input}')

def send_to_others(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the IP address and port number of the server
    server_ip = '10.19.254.160'
    server_port = 9999
    try:
        # Connect to the server
        s.connect((server_ip, server_port))
        # Send the message to the server
        s.sendall(message.encode())
        # Receive the response from the server
        #response = s.recv(1024).decode()
        #print(f"Received response: {response}")
    except ConnectionRefusedError:
        print("Failed to connect to the server")
    finally:
        # Close the socket
        s.close()

if __name__ == '__main__':
    app.run(debug=True)
