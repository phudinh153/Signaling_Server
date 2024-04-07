from flask import Flask
from flask_socketio import SocketIO, emit
import socketio

app = Flask(__name__)
sio = SocketIO(app)

# Create a Socket.IO client that connects to the other server
client = socketio.Client()

@client.event
def connect():
    print("Connected to the other server!")

@client.event
def disconnect():
    print("Disconnected from the other server!")

@client.event
def ack(data):
    print('Received ack from the other server:', data)

@sio.on('connect')
def connect():
    print("A client connected!")

@sio.on('disconnect')
def disconnect():
    print("A client disconnected!")

@sio.on('login')
def login(data):
    print('User logged in with key:', data['userKey'])

@sio.on('ack')
def ack(data):
    print('Received ack:', data)
    emit('ack', data, broadcast=True)

@sio.on('join')
def join(data):
    print('User joined:', data)

if __name__ == '__main__':
    # Connect to the other server
    client.connect('http://127.0.0.1:5004')
    print('Connected to the other server')

    # Emit an 'ack' event to the other server
    client.emit('ack', {'username': 'webcam', 'room': 1})
    print('Emitted ack event to the other server')

    # Run this server

    sio.run(app, host='0.0.0.0', port=5005)