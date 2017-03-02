import numpy as np
from graders import ScaledGrader
from agent import RandomAgent


def generate_examples(grader, n_examples=100, scores=True, sparse=False, board_size=(7, 7)):
    # Do not use - replaced with net_train.create_samples() #
    states = []
    values = []  # np.array([], dtype='int64')
    for i in range(n_examples):
        state = np.random.random_integers(-1, 1, board_size[0] * board_size[1])
        if sparse:
            for r in range(len(state)):
                if np.random.randint(0, 2) > 0:
                    state[r] = 0
        states.append(state)
        board = state.reshape(board_size)
#        print board
        if scores:
            value = grader.grade_board(board, 1)
            values.append(value)
    if scores:
        return states, values
    return states


class TrainingAgent(object):
    def __init__(self, agent, classifier):
        self.agent = agent
        self.clf = classifier
        self.agent.__init__()
        self.player = 0

    def play(self, board):
        state = board.flatten().reshape((1, -1))
        value = self.agent.grader.grade_board(board, self.agent.player)
        self.clf.fit(state, [value])
        self.agent.play(board)
        played = self.agent._game.get_board(self.agent.player)  # uh oh
        played_state = played.flatten().reshape((1, -1))
        played_value = self.agent.grader.grade_board(played, self.agent.player)
        self.clf.fit(played_state, [played_value])
        # print played_state, played_value

    def set_game(self, game):
        self.agent.set_game(game)
        self.player = self.agent.player

    def end(self):
        self.agent.end()
