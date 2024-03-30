from backgammon import Backgammon, Checkers

def human_turn(backgammon):
    return 0


if __name__ == "__main__":
    backgammon_board = Backgammon()
    print(backgammon_board)
    print(backgammon_board)

    print(backgammon_board.valid_move(Checkers.BLACK, (1, 3)))