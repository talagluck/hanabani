from flask import Flask, render_template, request, session, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room
# import hanabi2

app = Flask(__name__, static_folder='public',static_url_path='')
socketio = SocketIO(app)

user_list = []


@app.route('/')
def index():
    return render_template('/index.html')

@socketio.on('connect')
def handle_on_connect():
    return

@socketio.on('user joined')
def user_joined(user_id):
    session["user_id"] = user_id
    session["abc"] = "abcabcabc"
    join_room("living room")
    print(request.sid)

@socketio.on('client event')
def test_message(message):
    print(message)
    emit('server response', {'data':'got it'},room = "dining room")
    print(session)
    print(request.sid)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')
