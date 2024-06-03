from backgammon import Backgammon, Checkers
from minimax import best_move_agent_poda, first_moves
from learning import Learning
import pygame
import threading
import time

class Human():
    def __init__(self, checker, window = None):
        self.checker = checker
        self.window = window

    def draw_input_box(self, window, input_box, input_text):
        font = pygame.font.SysFont(None, 36)
        text_color = (0, 0, 0)
        input_box_color = (255, 255, 255)
        input_box_outline_color = (0, 0, 0)        
        pygame.draw.rect(window, input_box_color, input_box)
        pygame.draw.rect(window, input_box_outline_color, input_box, 2)
        text_surface = font.render(input_text, True, text_color)
        window.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    def turn(self, backgammon, dices = []):
        dices = backgammon.dices() if len(dices) == 0 else dices

        turns = range(len(dices))

        for turn in turns: 
            current_move = (-1, -1)
            valid_moves = backgammon.valid_moves(self.checker, dices)
            print(backgammon.valid_moves(self.checker, dices))

            if (valid_moves != []):
                while current_move not in valid_moves:
                    print("\nValores dos dados: ")
                    for dice in dices:
                        print(dice)

                    print(f"\n{turn + 1}º Jogada do humano")
                    position, dice = -1, -1

                    if (self.window == None):
                        position = int(input("Posição da peça a ser movida: "))
                        dice = int(input("Valor do dado para movimentação: "))
                    else:
                        running = True
                        background_color = (198, 195, 191)
                        input_box = pygame.Rect(800, 800, 80, 50)
                        input_text = ""
                        while running:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        print(f"Texto digitado: {input_text}")
                                        if position == -1:
                                            position = int(input_text)
                                        elif dice == -1:
                                            dice = int(input_text)
                                        else:
                                            running = False
                                        input_text = ""
                                    elif event.key == pygame.K_BACKSPACE:
                                        input_text = input_text[:-1]
                                    else:
                                        input_text += event.unicode

                            self.window.fill(background_color)
                            backgammon.draw_board(self.window)
                            self.draw_input_box(self.window, input_box, input_text)
                            pygame.display.flip()
                            pygame.time.Clock().tick(30)

                    if (self.checker == Checkers.WHITE):
                        current_move = (position, position + dice)
                        out_board = position + dice > 25
                    else:
                        current_move = (position, position - dice)
                        out_board = position - dice < 1

                    if out_board:
                        current_move = (position, 25)

                dices.remove(dice)
                backgammon = backgammon.play(len(dices) > 0, current_move)
                if (self.window == None):
                    print(backgammon)
                else:
                    background = (198, 195, 191)
                    self.window.fill(background)
                    backgammon.draw_board(self.window)
                    pygame.display.flip()
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
    def botGame():
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
        return
    
    def usualGame():   
        backgammon_board = Backgammon()

        human = Human(Checkers.WHITE)
        minimax = MiniMax(Checkers.BLACK)

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

        
        

    def userGame():
        backgammon_board = Backgammon()

        pygame.init()

        width, height = 1250, 924
        background = (198, 195, 191)

        window = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Jogo Gamão")

        human = Human(Checkers.WHITE, window)
        minimax = MiniMax(Checkers.BLACK)

        first_dices = backgammon_board.start()

        print("\n== GAMÃO ==\n")
        if (human.checker == Checkers.WHITE):
            print("Humano ⚪")
            print("Computador ⚫")
        else:
            print("Humano ⚫")
            print("Computador ⚪")

        
        turno = 1
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

                if backgammon_board.won():
                    playing = False

                window.fill(background)
                backgammon_board.draw_board(window)
                pygame.display.flip()

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
                
                print('oi', turno)

        if backgammon_board.won():
            print(f"{backgammon_board.turn()} ganhou!")

        pygame.quit()
    
        
    userGame()
