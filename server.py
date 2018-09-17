from flask import Flask, render_template, request, session, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room
import hanabi2

app = Flask(__name__, static_folder='public',static_url_path='')
socketio = SocketIO(app)

user_list = []

game_house = hanabi2.game_house

@app.route('/')
def index():
    return render_template('/index.html')

@socketio.on('connect')
def handle_on_connect():
    return

@socketio.on('client.new_game')
def new_game(max_players,mode,max_hints,max_lives):
    game_house.new_game(session["game_ID"], max_players,mode,max_hints,max_lives)


@socketio.on('user joined')
def user_joined(client_ID):
    session["game_ID"] ="living room"
    session["client_ID"] = client_ID
    join_room(session["game_ID"])

@socketio.on('client.add_player')
def add_player(name, client_ID):
    current_game().add_player(name, client_ID)

@socketio.on('client.list_players')
def list_players():
    return list(map(lambda player: player.name, current_game().player_list))

@socketio.on('client.start_game')
    #if session.id = host enable them to start
    def start_game():
         current_game.state = GAME_PLAYING

@socketio.on('client.get_hands')
    def get_hands():
        own_hand=current_player().serialize_own_hand
        other_hands=current_player().serialize_other_hands
        return own_hand,other_hands


@socketio.on('client.request_update')
def handle_request_update():
    emit("server.game_data",hanabi2.t.json)


#//////////////////////
@socketio.on('client event')
def test_message(message):
    print(message)
    emit('server response', {'data':'got it'},room = "dining room")
    print(session)
    print(request.sid)

def current_game():
    return game_house.games[session["game_ID"]]

def current_player():
    current_game.player_list[session["client_ID"]]

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')
