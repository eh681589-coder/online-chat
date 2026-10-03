from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Клиент подключился')
    for msg in messages:
        emit('message', msg)

@socketio.on('send_message')
def handle_message(data):
    print('Получено:', data['text'])
    messages.append(data)
    emit('message', data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Клиент отключился')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)