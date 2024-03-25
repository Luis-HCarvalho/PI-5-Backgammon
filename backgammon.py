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
            (0, 0)                                                              # 0: bar (whites, blacks)
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
    
    #
    def play(self, new_board_state):
        return Backgammon(new_board_state, self.turn(True))
    
    #
    def valid_moves(self, dices, checkers_color):
        def possible_moves(dices, checkers_color, last_move, moves):
            if len(dices) == 0:
                return moves
            
            for i in range(1, 24):
                if (last_move[i] != None and last_move[i][1] == checkers_color):
                    move = last_move.copy()
                    for i, d in enumerate(dices):
                        if last_move[d + i] > 24:
                            move[25][checkers_color] += 1
                        elif last_move[d + i] is None or last_move[d + i][0] <= 1:
                            move[d + i] = (1, checkers_color)
                        elif last_move[d + i][1] == checkers_color:                 
                            move[d + i][0] += 1
                        else:
                            continue

                        if move[i][0] == 1:
                            move[i] = None
                        else:
                            move[i][0] -= 1

                        moves.insert(move)
                        dices.pop(0)
                        tmp = possible_moves(dices, checkers_color, move, moves)
                        moves = [*moves, *tmp]
            
            return moves
        
        return possible_moves(dices, checkers_color, self.board.copy(), [])
