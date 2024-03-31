from backgammon import Backgammon, Checkers

class Human():
    def __init__(self, checker):
        self.checker = checker

    def turn(self, backgammon):
        dices = backgammon.dices()

        print("Valores dos dados: ")
        for dice in dices:
            print(dice)

        turns = range(len(dices))

        moves = []
        for turn in turns: 
            current_move = (-1, -1)
            print(backgammon.valid_moves(self.checker, dices))

            while current_move not in backgammon.valid_moves(self.checker, dices):
                print(f"{turn + 1}º Jogada do humano")

                position = int(input("Posição da peça a ser movida: "))
                dice = int(input("Valor do dado para movimentação: "))

                if (self.checker == Checkers.WHITE):
                    current_move = (position, position + dice)
                else:
                    current_move = (position, position - dice)

            dices.remove(dice)
            moves.append(current_move)

        return moves


if __name__ == "__main__":
    backgammon_board = Backgammon()
    human = Human(Checkers.WHITE)
    print(backgammon_board)
    print(human.turn(backgammon_board))

    # print(backgammon_board.valid_moves(Checkers.BLACK, (5, 6)))