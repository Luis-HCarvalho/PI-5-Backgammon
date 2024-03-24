class Player:
    def opposite(self):
        raise NotImplementedError("Must be implemented")

class Game():
    def turn(self):
        pass

    def play(self, localizacao):
        pass

    def valid_moves(self):
        pass

    def won(self, checkers_color):
        pass

    def draw(self):
        return (not self.won()) and (len(self.valid_moves()) == 0)

    def evaluate(self, player):
        pass

