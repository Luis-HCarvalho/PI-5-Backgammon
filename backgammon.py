from enum import Enum
from game import Game
import random

class Checkers(Enum):
    WHITE = 0
    BLACK = 1

class Backgammon(Game):
    def __init__(self, board = None, turn = None):
        self._turn = (self.first_turn() if turn is None else turn)
        self.board = (self.initial_board() if board is None else board)

    # generate initial state of the board
    def initial_board(self):
        board = [
            (0, 0),                                                              # 0: bar (whites, blacks)
            (2, Checkers.WHITE), None, None, None, None, (5, Checkers.BLACK),   # 1-6: Black's home board
            None, (3, Checkers.BLACK), None, None, None, (5, Checkers.WHITE),   # 7-12: Outer Board
            (5, Checkers.BLACK), None, None, None, (3, Checkers.WHITE), None,   # 13-18: Outer Board
            (5, Checkers.WHITE), None, None, None, None, (2, Checkers.BLACK),   # 19-24: White's home board
            (0, 0)                                                              # 25: bear off (whites, blacks)
        ]
        return board
    
    # returns a tuple with two pseudo random d6 values
    def dices(self):
        return (random.randint(1, 6), random.randint(1, 6))

    #
    def first_turn(self):
        dices = self.dices()
        return (Checkers.WHITE if dices[0] > dices[1] else Checkers.BLACK)
    
    #
    def turn(self, next=False):
        return (self._turn ^ 1 if next else self._turn)
    
    #
    def won(self, checkers_color):
        if checkers_color == Checkers.WHITE:
            return (self.board[25][0] == 15)
        else:
            return (self.board[25][1] == 15)
        