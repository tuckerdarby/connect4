import numpy as np
from graders import Grader
from agent import Agent
from game_helper import next_states


def collapse_state(grader, board, reach, player, ab, alpha=-999999, beta=999999, level=0):

    if reach == 0 or np.count_nonzero(board) == board.size or grader.check_board(board, player):
        return grader.grade_board(board, player=player) - level * 100

    states = next_states(board, (-1 * player))
    values = []
    for state in states:
        value = collapse_state(grader, state, (reach - 1), player, (ab * -1), alpha, beta, (level + 1))
        if ab == 2:         # Alpha Pruning
            if value > beta:
                return value
        elif ab == -2:      # Beta Pruning
            if value < alpha:
                return value
        values.append(value)
    if ab > 0:
        return max(values)
    elif ab < 0:
        return min(values)
    return


class MiniMaxAgent(Agent):
    def __init__(self, reach=3, grader=Grader):
        super(MiniMaxAgent, self).__init__()
        self.reach = reach
        self.mini_max = 0
        self.grader = grader(self.player)

    def _best_actions(self, board):
        best_value = -9999999 * self.mini_max
        states, indexes = next_states(board, self.player, index=True)
        values = []
        best_actions = []
        for state, index in zip(states, indexes):
            value = collapse_state(self.grader, state, self.reach, self.player, (self.mini_max * -1))
            values.append(value)
            if self.mini_max > 0:      # Maximize
                if value > best_value:
                    best_value = value
                    best_actions = [index]
                elif value == best_value:
                    best_actions.append(index)
            elif self.mini_max < 0:   # Minimize
                if value < best_value:
                    best_value = value
                    best_actions = [index]
                elif value == best_value:
                    best_actions.append(index)
        print 'values', values
        # if len(best_actions) == 1:
        #     return best_actions[0]
        r = np.random.randint(0, len(best_actions))
        return best_actions[r]

    def play(self, board):
        best_action = self._best_actions(board)
        self._game.play(self.player, best_action)

    def set_game(self, game):
        super(MiniMaxAgent, self).set_game(game)
        self.mini_max = 1 # self.player


class AlphaBetaAgent(Agent):
    def __init__(self, reach=3, grader=Grader):
        super(AlphaBetaAgent, self).__init__()
        self.reach = reach
        self.alpha_beta = 2 # self.player * 2
        self.grader = grader(self.player)

    def _best_actions(self, board):
        alpha, beta = -999999, 999999
        states, indexes = next_states(board, self.player, index=True)
        values = []
        potential_actions = []
        for state, index in zip(states, indexes):
            value = collapse_state(self.grader, state, self.reach, self.player, self.alpha_beta, alpha, beta)
            values.append(value)
            if self.alpha_beta > 0:        # Alpha
                if value > alpha:
                    alpha = value
                    potential_actions = [index]
                elif value == alpha:
                    potential_actions.append(index)
            elif self.alpha_beta < 0:     # Beta
                if value < beta:
                    beta = value
                    potential_actions = [index]
                elif value == beta:
                    potential_actions.append(index)
        if len(potential_actions) == 1:
            return potential_actions[0]
        r = np.random.randint(0, len(potential_actions))
        return potential_actions[r]

    def set_game(self, game):
        super(AlphaBetaAgent, self).set_game(game)
        self.alpha_beta = self.player * 2

    def play(self, board):
        best_action = self._best_actions(board)
        self._game.play(self.player, best_action)