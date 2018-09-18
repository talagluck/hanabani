from random import shuffle
# from collections import counter

class Tile(object):
    def __init__(self,color,value):
        if color not in Deck.tile_colors:
            raise ValueError('Invalid color')
        if value not in Deck.tile_values.keys():
            raise ValueError('Invalid value')
        self.color = color
        self.value = int(value)
        self.name = f'{self.color},{self.value}'
        self.notes = []


    def __repr__(self):
        return self.name

    def json(self):
        return {
        'color': self.color,
        'value': self.value,
        'notes': self.notes
        }


class Deck(object):
    tiles = []
    tile_colors = ['red','blue','yellow','green','white']
    tile_values = {'1':3,'2':2,'3':2,'4':2,'5':1}

    def __init__(self):
        for color in Deck.tile_colors:
            for key, value in Deck.tile_values.items():
                for i in range(0,value):
                    tile = Tile(color, key)
                    Deck.tiles.append(tile)
        shuffle(Deck.tiles)

    def __repr__(self):
        return f'{self.count()} tiles remaining'

    def __iter__(self):
        self.n=0
        return self

    def __next__(self):
        if self.n<len(self.tiles):
            result = self.tiles[self.n]
            self.n+=1
            return result
        else:
            raise StopIteration

    def shuffle(self):
        shuffle(Deck.tiles)

    def count(self):
        return len(Deck.tiles)

    def _deal(self, number_to_deal):
        count = self.count()
        actual = min([count,number_to_deal])
        if count==0:
            raise ValueError("All tiles have been dealt")
        hand = Deck.tiles[-actual:]
        Deck.tiles = Deck.tiles[:-actual]
        return hand

    def deal_hand(self):
        return self._deal(4)

    def deal_tile(self):
        return self._deal(1)


class Player(object):
    index_letters ={0:'a',1:'b',2:'c',3:'d'}
    player_number_range=[]
    def __init__(self, game, name, client_id):
        self.client_id = client_id
        self.tile_number = 10
        self.name = name
        self.game=game
        self.deck=self.game.deck
        # Player.player_number_range.append(self.number)
        self.possible_hints={'color':set([]),'value':set([])}
        self.hand = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0
        }

        dealt = self.game.deck.deal_hand() #create initial hand and deal it out
        i=0
        for key, value in self.hand.items():
            self.hand[key]=dealt[i]
            i+=1
            # print(self.name,self.tile_number,position[1].notes, position[1])
            self.add_number_to_notes(key)


        self.populate_hints()

    def __repr__(self):
        # return str(self.hand)
        return self.name

    def display_hands(self):
        hands={}
        for player in self.game.player_list:
            hands[player.client_id]=player.hand

        return hands

    def add_number_to_notes(self,tile_key):
        tile_to_note = self.hand[tile_key]
        tile_to_note.notes.append(self.tile_number)
        self.tile_number+=1

    def populate_hints(self):
        self.possible_hints['color'].clear()
        self.possible_hints['value'].clear()
        for key,tile in self.hand.items():
            self.possible_hints['color'].add(tile.color)
            self.possible_hints['value'].add(tile.value)

    def give_tile(self, tile_key):
        given_tile = self.hand[tile_key]
        # given_tile_index = self.hand.index(given_tile)
        # given_tile = self.hand[given_tile_index].pop(1) #remove the actual played tile from the hand
        self.hand[tile_key]=0
        return given_tile,tile_key

    def receive_tile(self, tile_key):
        new_dealt_tile = self.game.deck.deal_tile()[0]
        self.hand[tile_key]=new_dealt_tile
        self.hand[tile_key].notes.append(self.tile_number)
        self.tile_number+=1
        # self.add_number_to_notes(tile_key)
        self.populate_hints()
        print(f'{self.name} drew a new tile to position {Player.index_letters[tile_key]}')

    def play_tile(self, tile_key):
        # print(self.hand)
        played_tile, played_tile_key = self.give_tile(tile_key)

        # self.parse_tile(played_tile['hidden']) #get parse_color and parse_value

        #add tile to board and deal with board_state
        if played_tile.value - 1 == board.board_state[played_tile.color]:
            #if a pile is successfully completed
            self.game.board.board_state[played_tile.color] +=1
            print(f'{self.name} successfully played the {played_tile.color} {played_tile.value}')

            #if a pile is completed
            if played_tile.value == 5:
                self.game.board.board_state[played_tile.color.upper()]=self.game.board.board_state.pop(played_tile.color)
                if self.game.board.hints < self.game.board.max_hints:
                    self.game.board.hints+=1
                print(f'Congrats! You finished the {played_tile.color} stack, and gained back a hint.')
        else:
            #if a play is not successfully completed
            self.game.board.explosions-=1
            print(f'''BOOM!\nThere was no available place on the board for the {played_tile.color} {played_tile.value}.\nYou have {board.explosions} tries remaining!''')
            self.game.board.discard_pile.append(played_tile)
        self.receive_tile(tile_key)
        # print(self.hand)
        return('')


    def discard_tile(self, tile_key):
        print(self.hand)
        discarded_tile, discarded_tile_key = self.give_tile(tile_key)

        self.game.board.discard_pile.append(discarded_tile)
        if self.game.board.hints < self.game.board.max_hints:
            self.game.board.hints+=1
        print(f'{self.name} discarded a {discarded_tile.color} {discarded_tile.value}, and gained back a hint.')
        print(f'Discard pile consists of {self.game.board.discard_pile}')
        self.receive_tile(discarded_tile_key)
        # print(self.hand)
        return('')

    def give_hint(self,player,hint):
        if board.hints>0:
            for key,tile in player.hand.items():
                if tile.color == hint:
                    tile.notes.append(hint)
                if tile.value == hint:
                    tile.notes.append(hint)
            self.game.board.hints-=1
        else:
            print("No hints remain. Please discard a tile to regain a hint, or play a tile.")


    def serialize_hand(self):
        serialized_hand=[]
        for key, tile in self.hand.items():
            self.hand.append(tile.json())
        return serialized_hand

    def serialize_other_hands(self):
        serialized_hands=[]
        for player in self.game.player_list:
            if player.client_id != self.client_id:
                serialized_hands.append(player.serialize_hand())
        return serialized_hands

    def serialize_own_hand(self):
        serialized_own_hand=[]
        for key,tile in self.hand.items():
            serialized_own_hand.append({key: tile.notes})
        return serialized_own_hand

    def take_turn(self, board): #can play a tile, discard a tile, or give a hint
        while True:
            print(f"It's {self.name}'s turn. You can:")
            print("1. Give a hint")
            print("2. Discard a tile")
            print("3. Play a tile")
            turnType = int(input("What'll it be?\n"))
            if turnType not in [1,2,3]:
                print("Please enter 1, 2, or 3\n")
            else:
                if turnType == 1:
                    while True:
                        confirm = input("Are you sure you want to give a hint? y/n\n")
                        if confirm not in ["y","n"]:
                            print("Please enter y or n\n")
                        else:
                            while True:
                                print("You can see the following players and their hands\n")
                                for player in board.player_list:
                                    print(player, player.hand)
                                player_to_hint = input("To whom would you like to give a hint?\n")
                                if player_to_hint not in board.player_name_list:
                                    print("Not a valid player. Please enter a valid player.\n")
                                else:
                                    while True:
                                        hint_nums = [1]
                                        print("You can give the following hints:")
# !!!!!! change player to player_to_hint - access player object through player_to_hint name
                                        for hint_category, specific_hint in player.possible_hints.items():
                                            for hint in specific_hint:
                                                print(hint_nums[len(hint_nums)-1], hint)
                                                hint_nums.append(hint_nums[len(hint_nums)-1]+1)
                                        hint_to_give = input("Please enter the number of the hint you would like to give.\n")
                                        if hint_to_give not in hint_nums:
                                            print("Please enter a valid hint number.\n")
                                        else:
                                            self.give_hint(player, hint_to_give, board)
                                            print(f"You told {player} about their {hint_to_give} tiles")
                                            break
                                    break
                            break
                    break

                    self.give_hint()

                if turnType == 2:
                    self.discard_tile()

                if turnType == 3:
                    self.play_tile()

                break



class Board(object):

    def __init__(self):
        self.max_hints = 8
        self.discard_pile = []
        self.explosions = 3
        self.hints = self.max_hints
        self.board_state = {}
        self.player_list=[]
        self.player_name_list =[]
        for color in Deck.tile_colors:
            self.board_state[color]=0

    def __repr__(self):
        return f'''board: {self.board_state}\nexplosions remaining: {self.explosions}\nhints remaining: {self.hints}\n'''
#add deck to player



class Game(object):
    GAME_CREATED=1
    GAME_PLAYING=2
    GAME_LAST_TURN = 3
    GAME_LOST_DECK_DEPLETED=4
    GAME_LOST_EXPLODED=5
    GAME_WON=6

    def __init__(self,game_ID, max_players,mode,max_hints,max_lives):
        self.game_ID = game_ID
        self.max_players = max_players
        self.max_hints = max_hints
        self.max_lives = max_lives
        self.mode = mode
        self.deck = Deck()
        self.board = Board()
        self.player_list=[]
        self.state = Game.GAME_CREATED

    def add_player(self,name,client_id):
        player = Player(self, name, client_id)
        self.player_list.append(player)

    def get_player(self,client_id):
        player = [player for player in self.player_list if player.client_id==client_id][0]
        return player

    def start_game(self):
        if self.state != Game.GAME_PLAYING:
            self.state = Game.GAME_PLAYING
            return True
        else:
            return False

class Game_House(object):
    def __init__(self):
        self.games = {}

    def new_game(self, game_ID, max_players,mode,max_hints,max_lives):
        game = Game(game_ID, max_players,mode,max_hints,max_lives)
        self.games[game_ID] = game






#add methods/attributes to the Tile class:
#color
#value
# name: color + value
# so that a hand is just a dictionary of indices (a,b,c,d) and tile objects

# # tile = Tile('red','5')
# # print(tile)

#
# tom = Player(d, "tom",1)
#
# ren = Player(d, "ren",2)
# # print(ren.possible_hints)
#
game_house = Game_House()


d=Deck()
b= Board()
t = Tile('red','5')
g = Game("game_ID", "max_players","mode","max_hints","max_lives")
tom = Player(g,"tom",22323)
print(tom.hand)
for key,value in tom.hand.items():
    print(value.notes)


# b.start_game(2)
