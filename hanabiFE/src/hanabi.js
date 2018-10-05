import openSocket from 'socket.io-client';
const socket = openSocket('http://localhost:5000');


const Hanabi = {
    getCookieValue: function (a) {
        var b = document.cookie.match('(^|;)\\s*' + a + '\\s*=\\s*([^;]+)');
        return b ? b.pop() : '';
    },
    connect: function (callback) {
        console.log("Hanabi.connect")
        if (Hanabi.getCookieValue("hanabi_client_id") === "") {
            document.cookie = "hanabi_client_id=" + btoa(Math.random()).substr(5, 10);
        }
        
        var clientId = Hanabi.getCookieValue("hanabi_client_id");
        socket.emit("client.connected", clientId);
        console.log("1 connected, client id: " + clientId);
        callback(clientId);
    },
    newGame: function (maxPlayers, mode, maxHints, maxLives) {
        socket.emit("client.new_game", maxPlayers, mode, maxHints, maxLives)
        console.log("new game")
    },
    startGame: function () {
        socket.emit("client.start_game")
    },

    joinGame: function (game_ID) {
        console.log("JOIN GAME: ",game_ID)
        socket.emit("client.join_game", game_ID)
    },
    getHands: function () {
        socket.emit("client.getHands", function (own_hand, other_hands) {
            console.log(own_hand);
            console.log(other_hands);
        });
    },
    subscribeGameListUpdate: function(callback) {
        socket.on("server.game_list",
            gamesList => callback(gamesList)
        );
    }
}








export default Hanabi;