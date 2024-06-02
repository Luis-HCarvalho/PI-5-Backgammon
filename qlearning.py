import pickle
from backgammon import Backgammon, Checkers
from main import MiniMax
import random

class Qlearning:
    def __init__(
        self,
        table_name = "start-table.pkl",
        load = True,
        discount = 0.90,
        tetha = 1e-6,
        alpha = 0.1
    ):
        self.theta = tetha
        self.alpha = alpha
        self.discount = discount
        self.name = table_name

        if load == True:
            with open(f"q-tables/{table_name}", 'rb') as file:
                self.Q = pickle.load(file)
        else:
            self.Q = dict()
        
    def calc_all_states(self, depth = 2):        
        possible_dices = [[x, y] for x in range(1, 7) for y in range(x + 1, 7)] # [[x, y] if x != y else [x, y] * 2 for x in range(1, 7) for y in range(x, 7)]
        self.max_depth = depth
        self.player = Checkers.WHITE
        for dices in possible_dices:
            game = Backgammon(None, self.player)
            self.update(game, dices, 1)
        
        return self.Q
    
    def calc(self, max_depth = 2, prop_random = 0.2):
        self.player = Checkers.WHITE
        game = Backgammon(None, self.player)
        dices = game.first_turn()[1]
        
        current_player = self.player
        depth = 0
        while depth < max_depth:
            while len(dices) > 0:
                valid_moves = game.valid_moves(current_player, dices)
                
                move = [-1, -1]
                
                if len(valid_moves) == 0:
                    game = game.skip_turn(game)
                    break
                elif random.random() > prop_random:
                    move = random.choice(valid_moves)
                else:
                    move = self.get_max_a(game, dices)[1]
                
                if move == [-1, -1]:
                    game = game.skip_turn(game)
                    break
                
                key = (tuple(game.board), tuple(move))
                if (not key in self.Q):
                    self.Q[key] = 0.0

                q_last = self.Q[key]

                dice_used = game.dice_used(move, dices)
                dices.remove(dice_used)
                
                next_game = game.play(len(dices) > 0, move)
                
                q_next = self.new_q(game, next_game, dices)
                # aqui acontece a atualização do Q(s,a)
                self.Q[key] += self.alpha * (q_next -  q_last)
                
                game = next_game
            
            current_player = current_player.opposite()
            depth += 1
            dices = game.dices()
            
    
    def update(self, game, dices, depth):
        valid_moves = game.valid_moves(game.turn(), dices)
        for move in valid_moves:
            key = (tuple(game.board), tuple(move))
            if (not key in self.Q):
                self.Q[key] = 0.0

            q_last = self.Q[key]

            dices_copy = list(dices)
            dice_used = game.dice_used(move, dices_copy)
            dices_copy.remove(dice_used)
            
            next_game = game.play(len(dices_copy) > 0, move)
            
            q_next = self.new_q(game, next_game, dices)
            # Q(s,a) <= Q(s,a) + α([ R(s,a,s') +  𝛾 max(a) Q(s',a') - Q(s,a)] )
            self.Q[key] += self.alpha * (q_next -  q_last)

            if len(dices_copy) > 0:
                self.update(next_game, dices_copy, depth)
            elif depth < self.max_depth:
                possible_dices = [[x, y] if x != y else [x, y] * 2 for x in range(1, 7) for y in range(x, 7)]
                for new_dices in possible_dices:
                    self.update(next_game, new_dices, depth + 1)

    def new_q(self, game, next_game, dices):
        max_a = self.get_max_a(next_game, dices)[0] # max(a) Q(s',a')
        return game.evaluate(game.turn()) + self.discount * max_a

    def get_max_a(self, game, dices):
        max_q = float("-inf")
        best_move = [-1, -1]
        player = game.turn()
        dices_copy = [list(dices)]
        
        if len(dices) == 0:
            dices_copy = [[x, y] if x != y else [x, y] * 2 for x in range(1, 7) for y in range(x, 7)]        

        for new_dices in dices_copy:
            valid_moves = game.valid_moves(player, new_dices)
            for move in valid_moves:
                key = (tuple(game.board), tuple(move))
                if (not key in self.Q):
                    self.Q[key] = 0.0
                    
                if max_q < self.Q[key]:
                    max_q = self.Q[key]
                    best_move = move
        
        return (max_q, best_move)
    
    def save(self):
        with open(f"q-tables/{self.name}", 'wb') as file:
            pickle.dump(self.Q, file, protocol=pickle.HIGHEST_PROTOCOL)       



if __name__ == "__main__":
    def train(times = 10):
        qlearning = Qlearning(table_name="start-table5.pkl", load=True)
    
        i = 0
        
        while i < times:
            print(i)
            #qlearning.calc_all_states()
            qlearning.calc(3)
            
            i += 1
        
        qlearning.save()
        
    def get_bests():
        qlearning = Qlearning(table_name="start-table5.pkl")

        possible_dices = [[x, y] for x in range(1, 7) for y in range(x + 1, 7)]
        
        for dices in possible_dices:
            dices_copy = list(dices)
            game = Backgammon(None, Checkers.WHITE)
            (max_q1, move1) = qlearning.get_max_a(game, dices)
            dice_used = game.dice_used(move1, dices)
            dices.remove(dice_used)
            next_game = game.play(dices, move1)
            (max_q2, move2) = qlearning.get_max_a(next_game, dices)
            
            print(f"Dice {dices_copy} - {move1} ({max_q1}) - {move2} ({max_q2})")
        
    get_bests()