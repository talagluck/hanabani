from flask import Flask, render_template, request, session, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room
import hanabi2

app = Flask(__name__, static_folder='public',static_url_path='')
socketio = SocketIO(app)

user_list = []

game_house = hanabi2.game_house
game_house.games={}

@app.route('/')
def index():
    return render_template('/index.html')

@socketio.on('connect')
def handle_on_connect():
    return

@socketio.on('client.connected')
def connected(client_ID):
    print('user joined', client_ID)
    session["client_ID"] = client_ID
    broadcast_game_list()

    #TO DO: if this is an existing client, resume their game state

@socketio.on('client.join_game')
def user_joined(game_ID):
    session["game_ID"] = game_ID

    if session["game_ID"] not in game_house.games:
        game_house.new_game(session["game_ID"], 5,5,8,3)
        current_game().add_player("Guest " + session["client_ID"], session["client_ID"])
        current_game().host=current_player()
        broadcast_game_list()
    else:
        current_game().add_player("Guest " + session["client_ID"], session["client_ID"])


    join_room(session["game_ID"])
    print("Client " + session["client_ID"] + " joined game " + session["game_ID"])

@socketio.on('client.add_player')
def add_player(name, client_ID):
    current_game().add_player(name, client_ID)
    print("Player added: ", name)
    print("sdbjkbdjks")

@socketio.on('client.list_players')
def list_players():
    return list(map(lambda player: player.name, current_game().player_list))

@socketio.on('client.start_game')
    #if session.id = host enable them to start
def start_game():
    if not current_game().start_game():
        print("Game already started")

@socketio.on('client.get_hands')
def get_hands():
    own_hand=current_player().serialize_own_hand()
    other_hands=current_player().serialize_other_hands()
    return own_hand,other_hands


@socketio.on('client.request_update')
def handle_request_update():
    emit("server.game_data",hanabi2.t.json)


#//////////////////////

def broadcast_game_list():
    emit('server.game_list',list(game_house.games.keys()),broadcast=True)

@socketio.on('client event')
def test_message(message):
    print(message)
    emit('server response', {'data':'got it'},room = "dining room")
    print(session)
    print(request.sid)

def current_game():
    return game_house.games[session["game_ID"]]


def current_player():
    return current_game().get_player(session["client_ID"])

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', use_reloader=True, debug=True)
