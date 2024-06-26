import re
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'random secret key!'
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('join')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print('RoomEvent: {} has joined the room {}\n'.format(username, room))
    emit('ready', {username: username}, to=room, skip_sid=request.sid)
    print('Emitted ready event to room {} with data: {}'.format(room, {'username': username}))

@socketio.on('ack')
def handle_ack(data):
    print('Event acknowledged:', data)
    join_room(data['room'])
    print('Emitted ready event to room {} with data: {}'.format(data['room'], {'username': data['username']}))
    emit('ack', data, to=data['room'])

@socketio.on('data')
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print('DataEvent: {} has sent the data:\n {}\n'.format(username, data))
    emit('data', data, to=room, skip_sid=request.sid)

@socketio.on('offer')
def offer(data):
    print('OfferEvent:', data)
    username = data['username']
    room = data['room']
    emit('offer', data, to=room, skip_sid=request.sid)
    print('Emitted offer event to room {} with data: {}'.format(room, data))

@socketio.on('answer')
def answer(data):
    print('AnswerEvent:', data)
    username = data['username']
    room = data['room']
    emit('answer', data, to=room, skip_sid=request.sid)
    print('Emitted answer event to room {} with data: {}'.format(room, data))

@app.route('/')
def index():
    return 'ok', 200

@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5004)
