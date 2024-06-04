from learning import Learning
from backgammon import Backgammon, Checkers

class Bot():
    def __init__(self, checker):
        self.checker = checker
        self.learning = None
    
    def turn(self, backgammon, dices):
        if self.learning == None:
            self.learning = Learning(backgammon.board, backgammon.turn())

        dices = backgammon.dices() if len(dices) == 0 else dices
        print(dices)
        # print(backgammon.valid_moves(self.checker, dices))
        while len(dices) >= 1:
            mvs = backgammon.valid_moves(backgammon.turn(), dices)
            best = (None, float("-inf"))
            for m in mvs:
                new_state = backgammon.play(True, m)
                t = self.learning.td_zero_update(backgammon.board, new_state.board)
                if t > best[1]:
                    best = (m, t)

            move = (best[0] if len(mvs) > 0 else [-1, -1])

            if move == [-1, -1]:
                backgammon = backgammon.skip_turn(backgammon)
                break

            dice_used = backgammon.dice_used(move, dices)
            dices.remove(dice_used)
            backgammon = backgammon.play(len(dices) > 0, move)
        
        if backgammon.won():
            self.learning.save_model()

        return backgammon

def play_n_episodes(n):
    def train():
        backgammon_board = Backgammon()

        player1 = Bot(Checkers.WHITE)
        player2 = Bot(Checkers.BLACK)

        first_dices = backgammon_board.start()
        turno = 1

        while not backgammon_board.won():
            # print(backgammon_board)
            player_turn = backgammon_board.turn()
            # print(f"player turn: {player_turn}")
            if player_turn == player1.checker:
                backgammon_board = player1.turn(backgammon_board, first_dices) 
            else:
                backgammon_board = player2.turn(backgammon_board, first_dices)

            first_dices = []
            if player_turn != backgammon_board.turn():
                turno += 1
        
        # print(f"{backgammon_board.turn()} ganhou!")
    count = 0
    while count < n:
        train()
        count += 1
        
if __name__ == "__main__":
    backgammon_board = Backgammon()

    player1 = Bot(Checkers.WHITE)
    player2 = Bot(Checkers.BLACK)

    first_dices = backgammon_board.start()

    print("\n== GAMÃO ==\n")

    turno = 1

    while not backgammon_board.won():
        print(backgammon_board)
        player_turn = backgammon_board.turn()
        print(f"player turn: {player_turn}")
        if player_turn == player1.checker:
            backgammon_board = player1.turn(backgammon_board, first_dices) 
        else:
            backgammon_board = player2.turn(backgammon_board, first_dices)

        first_dices = []
        if player_turn != backgammon_board.turn():
            turno += 1
    
    print(f"{backgammon_board.turn()} ganhou!")