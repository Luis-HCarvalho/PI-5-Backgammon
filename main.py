from backgammon import Backgammon, Checkers
from minimax import best_move_agent_poda, first_moves

class Human():
    def __init__(self, checker):
        self.checker = checker

    def turn(self, backgammon):
        dices = backgammon.dices()

        turns = range(len(dices))

        for turn in turns: 
            current_move = (-1, -1)
            # print(backgammon.valid_moves(self.checker, dices))

            while current_move not in backgammon.valid_moves(self.checker, dices):
                print("\nValores dos dados: ")
                for dice in dices:
                    print(dice)

                print(f"\n{turn + 1}º Jogada do humano")

                position = int(input("Posição da peça a ser movida: "))
                dice = int(input("Valor do dado para movimentação: "))

                if (self.checker == Checkers.WHITE):
                    current_move = (position, position + dice)
                else:
                    current_move = (position, position - dice)

            dices.remove(dice)
            backgammon = backgammon.play(len(dices) > 0, current_move)
            print(backgammon)

        return backgammon

class MiniMax():
    def __init__(self, checker):
        self.checker = checker
    
    def turn(self, backgammon):
        dices = backgammon.dices()
        print(dices)
        while len(dices) >= 1:
            move = best_move_agent_poda(backgammon, dices, 6)
            
            used_dice = abs(move[1] - move[0])
            
            if used_dice == 24:
                used_dice = 24 - used_dice + 1

            dices.remove(used_dice)
            backgammon = backgammon.play(len(dices) > 0, move)
        
        return backgammon
    
    def first_turn(self, backgammon):
        dices = backgammon.dices()
        print(dices)
        
        return first_moves(backgammon, dices, self.checker)

if __name__ == "__main__":
    backgammon_board = Backgammon()
    human = Human(Checkers.WHITE)
    minimax = MiniMax(Checkers.BLACK)
    
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
            backgammon_board = human.turn(backgammon_board)        
            # backgammon_board = backgammon_board.play(False, human.moves[-1])
        elif turno == 1:
            backgammon_board = minimax.first_turn(backgammon_board)
        else:
            backgammon_board = minimax.turn(backgammon_board)

        if turn_player != backgammon_board.turn():
            turno += 1
        

    # print(backgammon_board.valid_moves(Checkers.BLACK, (5, 6)))