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
        self.notes = ''

    def __repr__(self):
        return f'{self.color},{self.value}'

class Deck(object):
    tiles = []
    tile_colors = ['red','blue','yellow','green','white']
    tile_values = {'1':3,'2':2,'3':2,'4':2,'5':1}

    def __init__(self):
        for color in Deck.tile_colors:
            for key, value in Deck.tile_values.items():
                # print(color,value)
                tile = Tile(color, key)
                for i in range(0,value):
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
#
# class Hand(dict):
#     def __init__(self, dealt):
#         self.hand = [[{'label':'a'}],
#                     [{'label':'b'}],
#                     [{'label':'c'}],
#                     [{'label':'d'}]]
#
#         for i, position in enumerate(self.hand):
#             position.append(dealt[i])
#
#     def __repr__(self):
#         return self.hand


class Player(object):
    def __init__(self, deck, name):
        # self.hand = Hand(deck.deal_hand()).hand
        self.hand = [[{'label':'a'}],
                    [{'label':'b'}],
                    [{'label':'c'}],
                    [{'label':'d'}]]

        self.name = name
        dealt = deck.deal_hand()
        i=0
        for i, position in enumerate(self.hand):
            position.append(dealt[i])
            i+=1

    def __repr__(self):
        # return str(self.hand)
        return self.name
    #
    # def parse_tile(self, tile):
    #     self.parse_color,self.parse_value = tile.split(',')
    #     self.parse_value = int(self.parse_value)

    def give_tile(self, tile_letter):
        given_tile = [tile for tile in self.hand if tile[0]['label'] == tile_letter][0]
        given_tile_index = self.hand.index(given_tile)
        given_tile = self.hand[given_tile_index].pop(1) #remove the actual played tile from the hand
        return given_tile, given_tile_index

    def receive_tile(self, deck, idx, letter):
        new_dealt_tile = deck.deal_tile()[0]
        self.hand[idx].append(new_dealt_tile)
        print(f'{self.name} drew a new tile to position {letter}')

    def play_tile(self, tile_letter, deck, board):
        print(self.hand)
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

        #deal a new tile
        # new_dealt_tile = {'known':'','hidden':deck.deal_tile()[0]}
        # self.hand[played_tile_index].append(new_dealt_tile)
        # print(f'{self.name} drew a new tile to position {tile_letter}')
        self.receive_tile(deck, played_tile_index, tile_letter)
        print(self.hand)
        return('')


    def discard_tile(self, tile_letter, deck, board):
        print(self.hand)
        discarded_tile, discarded_tile_index = self.give_tile(tile_letter)

        board.discard_pile.append(discarded_tile)
        print(f'{self.name} discarded a {discarded_tile.color} {discarded_tile.value}.')
        print(f'Discard pile consists of {board.discard_pile}')
        self.receive_tile(deck, discarded_tile_index, tile_letter)
        print(self.hand)
        return('')

    def give_hint(self,player,hint):
        for tile in player.hand:
            self.parse_tile(tile[1])



    def take_turn(self, action): #can play a tile, discard a tile, or give a hint
        pass

    def reorder_tiles(self, swap_from, swap_to):
        pass

class Board(object):
    max_hints = 8

    def __init__(self, deck):
        self.deck = deck
        self.discard_pile = []
        self.explosions = 3
        self.hints = self.max_hints
        self.board_state = {}
        for color in Deck.tile_colors:
            self.board_state[color]=0

    def __repr__(self):
        return f'''board: {self.board_state}\nexplosions remaining: {self.explosions}\nhints remaining: {self.hints}\ntiles remaining: {self.deck.count()}'''

#add methods/attributes to the Tile class:
#color
#value
# name: color + value
# so that a hand is just a dictionary of indices (a,b,c,d) and tile objects

# # tile = Tile('red','5')
# # print(tile)
d = Deck()
for i in d:
    print(i)
# # print(d)
# # h = Hand(d.deal_hand())
# # h = h.hand
# # print(h)
# # print(type(h.hand))

# # for i,j in h.hand.items():
# #     print(i,j)
# # print(h2)
tom = Player(d, "tom")
print(tom.hand)

# ren = Player(d, "ren")
# #
# # # print(tom.known_hand)
# # # print(ren.hand)
# #
b= Board(d)
print(tom.play_tile('a',d,b))
# # # print(b)
print(tom.discard_tile('a',d,b))
# print(tom.discard_tile('b',d,b))
# print(tom.hidden_hand[0][1])
# # print(b)
