from enum import Enum
from game import Game, Player
import random

class Checkers(Player, Enum):
    WHITE = 0
    BLACK = 1

    # get opposite checker
    def opposite(self):
        return Checkers.BLACK if self == Checkers.WHITE else Checkers.WHITE

class Backgammon(Game):
    def __init__(self, board = None, turn = None):
        self.board_number_of_positions = 24

        self._turn = (self.first_turn() if turn is None else turn)
        self.board = (self.initial_board() if board is None else board)

    # generate initial state of the board
    def initial_board(self):
        board = [
            (0, 0),                                                             # 0: bar (whites, blacks)
            (2, Checkers.WHITE), None, None, None, None, (5, Checkers.BLACK),   # 1-6: Black's home board
            None, (3, Checkers.BLACK), None, None, None, (5, Checkers.WHITE),   # 7-12: Outer Board
            (5, Checkers.BLACK), None, None, None, (3, Checkers.WHITE), None,   # 13-18: Outer Board
            (5, Checkers.WHITE), None, None, None, None, (2, Checkers.BLACK),   # 19-24: White's home board
            (0, 0)                                                              # 25: bear off (whites, blacks)
        ]
        return board
    
    # returns a tuple with two pseudo random d6 values
    def dices(self):
        dices = [random.randint(1, 6), random.randint(1, 6)]
        return dices if dices[0] != dices[1] else [dices[0]] * 4

    #
    def first_turn(self):
        dices = self.dices()
        return (Checkers.WHITE if dices[0] > dices[1] else Checkers.BLACK)
    
    #
    def turn(self, next=False):
        return (self._turn.opposite() if next else self._turn)
    
    #
    def won(self, checkers_color):
        if checkers_color == Checkers.WHITE:
            return (self.board[25][0] == 15)
        else:
            return (self.board[25][1] == 15)

    # according to which player and array of values ​​to be moved, an array of movement possibilities is returned [origin of the piece, destination of the piece]
    def valid_moves(self, checker, movements):
        valid_moves = []  

        if (self.board[0][checker.value]):
            valid_moves = self._valid_moves_from_bar(checker, movements)

        elif (self._bearoff_available(self.board, checker)):
            valid_moves = self._valid_moves_during_bearoff(checker, movements)

        else:
            valid_moves = self._valid_moves_across_board(checker, movements)        

        return valid_moves
    
    # possible movements of the captured checker starting from the initial quadrant
    def _valid_moves_from_bar(self, checker, movements):
        moves = []

        for movement in movements:
            if (checker == Checkers.WHITE):
                position = 0 
                new_position = position + movement
            else:
                position = 25
                new_position = position - movement

            if (self._available_position(checker, new_position)):
                moves.append((0, new_position))

        return moves
    
    # for each origin position, according to the dices number, what are the possible destination positions
    def _valid_moves_across_board(self, checker, movements):
        moves = []
        current_positions = self._current_checkers_positions(checker)

        for position in current_positions:
            for movement in movements:
                # depending on the checker to be moved, the direction on the board is different
                if (checker == Checkers.WHITE):
                    new_position = position + movement
                else:
                    new_position = position - movement

                if(self._available_position(checker, new_position)):
                    moves.append((position, new_position))
        
        return moves
    
    # possible moves considering final position rules
    def _valid_moves_during_bearoff(self, checker, movements):
        moves = []
        moves_with_score = []
        moves_out_range = []
        current_positions = self._current_checkers_positions(checker)

        
        for movement in movements:
            for position in current_positions:
                # depending on the checker to be moved, the direction on the board is different
                if (checker == Checkers.WHITE):
                    new_position = position + movement
                    if (new_position == self.board_number_of_positions + 1):
                        moves_with_score.append((position, 25))
                        moves.append((position, 25))
                    elif (new_position < self.board_number_of_positions + 1):
                        moves.append((position, new_position))
                    else:
                        moves_out_range.append(position)
                else:
                    new_position = position - movement
                    if (new_position == 0):
                        moves_with_score.append((position, 25))
                        moves.append((position, 25))
                    elif (new_position > 0):
                        moves.append((position, new_position))
                    else:
                        moves_out_range.append(position)

            if (moves_with_score == [] and moves_out_range != []):
                if (checker == Checkers.WHITE):
                    moves.append((min(moves_out_range), 25))
                else:
                    moves.append((max(moves_out_range), 25))
            
            moves_out_range = []
            moves_with_score = [] 

        return moves
    
    # possibilities of parts to be moved according to the checker (origin)
    def _current_checkers_positions(self, checker):
        positions = []

        for i in range(self.board_number_of_positions):
            position = i + 1

            if self.board[position] != None and self.board[position][1] == checker:
                positions.append(position)

        return positions

    # checks if the position is within the board and available within the rules 
    def _available_position(self, checker, position):
        if (position >= 1 and position <= self.board_number_of_positions):
            # checks if the new position no longer contains more than one piece from the enemy team
            if not (self.board[position] != None and self.board[position][1] != checker and self.board[position][0] > 1):
                return True
        
        return False
    
    # evaluate if bering off checkers is available
    def _bearoff_available(self, board, checkers_color):
        count = 0
        for i in range(0, 7):
            index = (i + 19 if checkers_color == Checkers.WHITE else i)
            if index == 0 or index == 25:
                count += board[25][1]
            elif board[index] != None and board[index][1] == checkers_color:
                count += board[index][0]
        
        return (count == 15)

    # organize visual presentation of each quadrant   
    def quadrant_checkers_positions(self, total_of_quadrant_columns, total_of_rows, start, end):
        quadrant_positions = [" 🟦 |"] * (total_of_quadrant_columns * total_of_rows)

        for position in range(start - 1, end):
            index = position - start + 1

            position_value = self.board[position + 1]

            if (position_value != None):
                if (position_value[1] == Checkers.WHITE):
                    checker = " ⚪ |"
                else:
                    checker = " ⚫ |"

                # if the number of checkers is less than the set number of lines, normally add the representation to the list
                if (position_value[0] <= total_of_rows):   
                    for row_index in range(position_value[0]):
                        quadrant_positions[index + total_of_quadrant_columns * (row_index)] = checker
                # otherwise, in the last available line, place the value of the difference between represented checkers and checkers that are actually in that position
                else:
                    for row_index in range(total_of_rows):      
                        if (row_index == total_of_rows - 1):
                            row_value = " +" + str(position_value[0] - total_of_rows + 1) + " |"
                        else:
                            row_value = checker
                        quadrant_positions[index + total_of_quadrant_columns * (row_index)] = row_value
            
        return quadrant_positions
    
    # return the current state of the board
    def __str__(self):
        final_state = ""

        # variables for readability and maintenance of base values ​​used
        total_of_rows = 7
        total_of_quadrant_columns = int(self.board_number_of_positions / 4)
        total_of_positions = self.board_number_of_positions * total_of_rows
        total_of_positions_top = total_of_positions_bottom = int(total_of_positions / 2)

        # lists of quadrant presentations being divided by the top of the board and the bottom
        positions_top = []
        positions_bottom = []

        positions_top.append(self.quadrant_checkers_positions(total_of_quadrant_columns, total_of_rows, 13, 18))
        positions_top.append(self.quadrant_checkers_positions(total_of_quadrant_columns, total_of_rows, 19, 24))
        
        # as the board is mirrored between the top and bottom,the bottom part was inverted to achieve this effect
        positions_bottom.append(self.quadrant_checkers_positions(total_of_quadrant_columns, total_of_rows, 7, 12)[::-1])
        positions_bottom.append(self.quadrant_checkers_positions(total_of_quadrant_columns, total_of_rows, 1, 6)[::-1])
    
        board_top = [None] * total_of_positions_top
        board_bottom = [None] * total_of_positions_bottom
        
        # merging the quadrants into a single list, for this purpose manipulating the indexes so that when placing them in the output, they maintain the correct order
        for column in range(total_of_quadrant_columns):
            for row in range(total_of_rows):
                board_top[column + (2 * total_of_quadrant_columns * row)] = positions_top[0][total_of_quadrant_columns * row + column]
                board_top[column + (2 * total_of_quadrant_columns * row) + total_of_quadrant_columns] = positions_top[1][total_of_quadrant_columns * row + column]

                board_bottom[column + (12 * row)] = positions_bottom[0][6*row + column]
                board_bottom[column + (12 * row)+6] = positions_bottom[1][6*row + column]


        # construct the final state string with proper formatting
        final_state += "\n\n||============================================================||\n"

        for position in range(total_of_positions_top):
            if (position % (2 * total_of_quadrant_columns) == 0):
                final_state += "||"
            elif (position % total_of_quadrant_columns == 0):
                final_state += "|"

            final_state += board_top[position]

            if ((position + 1) % (2 * total_of_quadrant_columns) == 0 and position !=0):
                final_state += "|\n"

        final_state += "||============================================================||\n"

        for position in range(total_of_positions_bottom):
            if (position % (2 * total_of_quadrant_columns) == 0):
                final_state += "||"
            elif (position % total_of_quadrant_columns == 0):
                final_state += "|"

            final_state += board_bottom[position]

            if ((position + 1) % (2 * total_of_quadrant_columns) == 0 and position !=0):
                final_state += "|\n"

        final_state += "||============================================================||\n\n"

        final_state += f"Peças tomadas [ ⚪ : {self.board[0][0]} ] [ ⚫ : {self.board[0][1]} ]\n\n"

        final_state += f"Peças pontuadas [ ⚪ : {self.board[25][0]} ] [ ⚫ : {self.board[25][1]} ]\n\n"

        return final_state
    