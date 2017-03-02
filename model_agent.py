import numpy as np
from agent import Agent
from game_helper import next_states
from graders import max_value_state


class ModelAgent(Agent):
    def __init__(self, model):
        super(ModelAgent, self).__init__()
        self.model = model

    def play(self, board):
        best_action = self._best_action(board)
        self._game.play(self.player, best_action)

    def _best_action(self, board):
        states, indexes = next_states(board, self.player, index=True)
        max_value = None
        max_indexes = []
        for state, index in zip(states, indexes):
            value = self._value_state(state)
            if max_value is None:
                max_value = value
                max_indexes = [index]
            elif value > max_value:
                max_value = value
                max_indexes = [index]
            elif value == max_value:
                max_indexes.append(index)
        size = len(max_indexes)
        r = np.random.randint(0, size)
        return max_indexes[r]

    def _value_state(self, state):
        flat = state.flatten().reshape(1, -1)
        value = self.model.predict(flat)[0]
        return value


class RevolutionModelAgent(ModelAgent):
    def __init__(self, model, shape):
        super(RevolutionModelAgent, self).__init__(model)
        self.shape = shape

    def _value_state(self, state):
        return max_value_state(self.model, self.shape, state)
