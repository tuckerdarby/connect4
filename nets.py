import numpy as np
from sklearn.neural_network import MLPRegressor
from game_helper import next_states
from agent import Agent
from graders import ScaledGrader
from graders import max_value_state


class NeuralAgent(Agent):
    def __init__(self, grader=ScaledGrader, net=None):
        super(NeuralAgent, self).__init__()
        if net is None:
            self.net = MLPRegressor(hidden_layer_sizes=(30, 15), max_iter=50,
                                    alpha=1e-4, random_state=1,
                                    solver='sgd', tol=1e-2,
                                    learning_rate_init=0.1, warm_start=True)
        else:
            self.net = net
        self.fitted = False
        self.training = True
        self.grader = grader(self.player)

    def load_net(self, net, fitted=True, training=False):
        self.net = net
        self.fitted = fitted
        self.training = training

    def play(self, board):
        best_action = self._best_action(board)
        self._game.play(self.player, best_action)
        if self.training:
            board = self._game.get_board(self.player)
            score = self.grader.grade_board(board)
            state = np.array(board.flatten(), dtype='int64')
            self.net.partial_fit([state], [score])
            self.fitted = True

    def _value_state(self, state):
        flat = state.flatten().reshape(1, -1)
        value = self.net.predict(flat)[0]
        return value

    def _best_action(self, board):
        states, indexes = next_states(board, self.player, index=True)
        if not self.fitted:
            r = np.random.randint(0, len(indexes))
            return indexes[r]
        max_value = None
        max_indexes = []
        for state, index in zip(states, indexes):
            value = self._value_state(state)
            # print 'predict score:', value
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


class SubsampleNeuralAgent(NeuralAgent):
    def __init__(self, net, sample_size=(4, 4)):
        super(SubsampleNeuralAgent, self).__init__(net=net)
        self.sample_size = sample_size
        self.training = False
        self.fitted = True

    def _value_state(self, state):
        return max_value_state(self.net, self.sample_size, state)
