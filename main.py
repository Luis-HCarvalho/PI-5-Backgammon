from backgammon import Backgammon, Checkers
from minimax import best_move_agent_poda, first_moves

class Human():
    def __init__(self, checker):
        self.checker = checker

    def turn(self, backgammon, dices = []):
        dices = backgammon.dices() if len(dices) == 0 else dices

        turns = range(len(dices))

        for turn in turns: 
            current_move = (-1, -1)
            valid_moves = backgammon.valid_moves(self.checker, dices)
            print(valid_moves)

            if (valid_moves != []):
                while current_move not in valid_moves:
                    print("\nValores dos dados: ")
                    for dice in dices:
                        print(dice)

                    print(f"\n{turn + 1}º Jogada do humano")

                    position = int(input("Posição da peça a ser movida: "))
                    dice = int(input("Valor do dado para movimentação: "))

                    if (self.checker == Checkers.WHITE):
                        current_move = (position, position + dice)
                        out_board = position + dice > 25
                    else:
                        current_move = (position, position - dice)
                        out_board = position - dice < 1
                        if position == 0:
                            current_move = (position, 25 - dice)
                            out_board = False

                    if out_board and dice in dices:
                        current_move = (position, 25)

                dices.remove(dice)
                backgammon = backgammon.play(len(dices) > 0, current_move)
                print(backgammon)
                
                if backgammon.won():
                    break
            else:
                print("\nValores dos dados: ")
                for dice in dices:
                    print(dice)

                print("\nSem jogadas válidas, pular turno")
                backgammon = backgammon.skip_turn(backgammon)
                break

        return backgammon

class MiniMax():
    def __init__(self, checker):
        self.checker = checker
    
    def turn(self, backgammon, dices):
        dices = backgammon.dices() if len(dices) == 0 else dices
        print(dices)
        # print(backgammon.valid_moves(self.checker, dices))
        while len(dices) >= 1 and not backgammon.won():
            move = best_move_agent_poda(backgammon, dices, 4)
        
            if move == [-1, -1]:
                backgammon = backgammon.skip_turn(backgammon)
                break

            dice_used = backgammon.dice_used(move, dices)
            dices.remove(dice_used)
            backgammon = backgammon.play(len(dices) > 0, move)
        
        return backgammon
    
    def first_turn(self, backgammon, dices):
        dices = backgammon.dices() if len(dices) == 0 else dices
        print(dices)
        
        return first_moves(backgammon, dices, self.checker)

if __name__ == "__main__":
    backgammon_board = Backgammon()

    human = Human(Checkers.BLACK)
    minimax = MiniMax(Checkers.WHITE)

    first_dices = backgammon_board.start()

    print("\n== GAMÃO ==\n")
    if (human.checker == Checkers.WHITE):
        print("Humano ⚪")
        print("Computador ⚫")
    else:
        print("Humano ⚫")
        print("Computador ⚪")

    turno = 1
    while not backgammon_board.won():
        print(backgammon_board)
        turn_player = backgammon_board.turn()
        if backgammon_board.turn() == human.checker:
            backgammon_board = human.turn(backgammon_board, first_dices)        
            # backgammon_board = backgammon_board.play(False, human.moves[-1])
        elif turno == 1:
            backgammon_board = minimax.first_turn(backgammon_board, first_dices)
        else:
            backgammon_board = minimax.turn(backgammon_board, first_dices)

        first_dices = []
        if turn_player != backgammon_board.turn():
            turno += 1

    print(backgammon_board)
    print(f"{backgammon_board.turn()} ganhou!")