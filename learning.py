import numpy as np
from keras import Sequential, layers
from backgammon import Checkers

class Learning:
    def __init__(self, game, player_color):
        state = self._vectorize_state(game.board)
        self.state_size = len(state)
        self.player_color = player_color
        self.model = self._build_model()


    def _vectorize_state(self, state):
        # len(state) is 26
        arr = np.zeros(28, dtype=int)
        
        arr[0] = state[0][0]  #bar whites
        arr[1] = state[0][1]  #bar blacks

        for i in range(1, 25):
            if state[i] is None:
                continue

            arr[i + 1] = (
                state[i][0] if state[i][1] == Checkers.WHITE else -state[i][0]
            )
        
        arr[26] = state[25][0]  #bear off whites
        arr[27] = state[25][1]  #bear off blacks

        return arr

    def _build_model(self):
        try:
            model = keras.models.load_model("backgammon_model.h5")
        except:
            model = Sequential([
                layers.Dense(128, activation="relu", input_shape=(self.state_size)),
                layers.Dense(128, activation="relu"),
                layers.Dense(1, activation="linear")
            ])
            model.compile(optimizer=keras.optimizers.Adam(), loss="mse")

        return model
    
    def _predict_value(self, state):
        return self.model.predict(state)
    
    def _train(self, state, target):
        self.model.fit(state, target, epochs=1, verbose=0)
    
    def _reward(self, state):
        return (1 if state[-1][self.player_color] == 15 else 0)