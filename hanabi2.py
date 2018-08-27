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
        return f'{self.color},{self.value}'

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
    def __init__(self, deck, name, number):
        self.tile_number = 10
        self.name = name
        self.number = number
        Player.player_number_range.append(self.number)
        self.possible_hints={'color':set([]),'value':set([])}
        self.hand = [[{'label':'a'}],
                    [{'label':'b'}],
                    [{'label':'c'}],
                    [{'label':'d'}]]

        dealt = deck.deal_hand() #create initial hand and deal it out
        # i=0
        for i, position in enumerate(self.hand):
            position.append(dealt[i])
            # print(self.name,self.tile_number,position[1].notes, position[1])
            self.add_number_to_notes(i)


        self.populate_hints()

    def __repr__(self):
        # return str(self.hand)
        return self.name

    def add_number_to_notes(self,tile_index):
        tile_to_note = self.hand[tile_index][1]
        tile_to_note.notes.append(self.tile_number)
        self.tile_number+=1

    def populate_hints(self):
        for tile in self.hand:
            self.possible_hints['color'].add(tile[1].color)
            self.possible_hints['value'].add(tile[1].value)

    def give_tile(self, tile_letter):
        given_tile = [tile for tile in self.hand if tile[0]['label'] == tile_letter][0]
        given_tile_index = self.hand.index(given_tile)
        given_tile = self.hand[given_tile_index].pop(1) #remove the actual played tile from the hand
        self.possible_hints['color'].clear()
        self.possible_hints['value'].clear()
        return given_tile, given_tile_index

    def receive_tile(self, deck, idx, letter):
        new_dealt_tile = deck.deal_tile()[0]
        self.hand[idx].append(new_dealt_tile)
        self.add_number_to_notes(idx)
        self.populate_hints()
        print(f'{self.name} drew a new tile to position {Player.index_letters[idx]}')

    def play_tile(self, tile_letter, deck, board):
        # print(self.hand)
        played_tile, played_tile_index = self.give_tile(tile_letter)

        # self.parse_tile(played_tile['hidden']) #get parse_color and parse_value

        #add tile to board and deal with board_state
        if played_tile.value - 1 == board.board_state[played_tile.color]:
            #if a pile is successfully completed
            board.board_state[played_tile.color] +=1
            print(f'{self.name} successfully played the {played_tile.color} {played_tile.value}')

            #if a pile is completed
            if played_tile.value == 5:
                board.board_state[played_tile.color.upper()]=board.board_state.pop(played_tile.color)
                if board.hints < board.max_hints:
                    board.hints+=1
                print(f'Congrats! You finished the {played_tile.color} stack, and gained back a hint.')
        else:
            #if a play is not successfully completed
            board.explosions-=1
            print(f'''BOOM!\nThere was no available place on the board for the {played_tile.color} {played_tile.value}.\nYou have {board.explosions} tries remaining!''')

        self.receive_tile(deck, played_tile_index, tile_letter)
        # print(self.hand)
        return('')


    def discard_tile(self, tile_letter, deck, board):
        print(self.hand)
        discarded_tile, discarded_tile_index = self.give_tile(tile_letter)

        board.discard_pile.append(discarded_tile)
        if board.hints < board.max_hints:
            board.hints+=1
        print(f'{self.name} discarded a {discarded_tile.color} {discarded_tile.value}, and gained back a hint.')
        print(f'Discard pile consists of {board.discard_pile}')
        self.receive_tile(deck, discarded_tile_index, tile_letter)
        # print(self.hand)
        return('')

    def give_hint(self,player,hint,board):
        if board.hints>0:
            for tile in player.hand:
                if tile[1].color == hint:
                    tile[1].notes.append(hint)
                if tile[1].value == hint:
                    tile[1].notes.append(hint)
            board.hints-=1
        else:
            print("No hints remain. Please discard a tile to regain a hint, or play a tile.")


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

    def __init__(self, deck):
        self.max_hints = 8
        self.deck = deck
        self.discard_pile = []
        self.explosions = 3
        self.hints = self.max_hints
        self.board_state = {}
        self.player_list=[]
        self.player_name_list =[]
        for color in Deck.tile_colors:
            self.board_state[color]=0

    def __repr__(self):
        return f'''board: {self.board_state}\nexplosions remaining: {self.explosions}\nhints remaining: {self.hints}\ntiles remaining: {self.deck.count()}'''

    def start_game(self,number_of_players):
        for i in range(0,number_of_players):
            name = input(f'Please enter the name of Player {i+1}')
            player = Player(self.deck, name, i+1)
            self.player_list.append(player)
            self.player_name_list.append(player.name)

        while True:
            for player in self.player_list:
                player.take_turn(self)




#add methods/attributes to the Tile class:
#color
#value
# name: color + value
# so that a hand is just a dictionary of indices (a,b,c,d) and tile objects

# # tile = Tile('red','5')
# # print(tile)
d = Deck()

tom = Player(d, "tom",1)

ren = Player(d, "ren",2)
# print(ren.possible_hints)

b= Board(d)4
b.start_game(3)
