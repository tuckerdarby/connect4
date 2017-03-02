from __future__ import division

import numpy as np
from rankers import rank_board
from data_processing import get_areas
# from model_help import max_value_state
game_reward = 1000


def state_values(net, sample_size, state):
    state_areas = get_areas(state, sample_size, padding=False)
    values = []
    for area_index, area in enumerate(state_areas):
        flat = area.flatten().reshape(1, -1)
        area_value = net.predict(flat)[0]
        values.append(area_value)
    return values


def min_value_state(net, sample_size, state):
    min_area_value = min(state_values(net, sample_size, state))
    return min_area_value


def max_value_state(net, sample_size, state):
    max_area_value = max(state_values(net, sample_size, state))
    return max_area_value


class Grader(object):
    def __init__(self, player=0, reward=game_reward, goal=4):
        self.reward = reward
        self.goal = goal

    def grade_board(self, board, player=0):
        gains, won = self._rank_player(board, player)
        if won:
            return self.reward
        losses, lost = self._rank_player(board, (player * -1))
        if lost:
            return -self.reward
        gain = self._score_ranks(gains)
        loss = self._score_ranks(losses)
        return gain - loss

    def check_board(self, board, player):
        ranks = rank_board(board, player)
        return self._check_goal(ranks)
    
    def _rank_player(self, board, player):
        ranks = rank_board(board, player)
        goal = self._check_goal(ranks)
        return ranks, goal

    def _check_goal(self, ranks):
        return ranks[0].count(self.goal) > 0 or ranks[1].count(self.goal) > 0 or ranks[2].count(self.goal) > 0
    
    def _score_ranks(self, ranks):
        score = 0
        for i, dim in enumerate(ranks):
            for rank in dim:
                if i < 2:
                    score += 5**(rank-1)
                else:
                    score += 2**(rank-1)
        return score


class ScaledGrader(Grader):
    def __init__(self, reward=10, goal=4, factor=4):
        super(ScaledGrader, self).__init__(reward=reward, goal=goal)
        self.factor = factor
        self.grade = 0

    def grade_board(self, board, player=0):
        score = super(ScaledGrader, self).grade_board(board, player)
        score = score / (self.goal * 10 ** (self.factor - 1))
        return score


class SubsampleNetGrader(Grader):
    def __init__(self, net, sample_size):
        super(SubsampleNetGrader, self).__init__(reward=0, goal=0)
        self.net = net
        self.sample_size = sample_size

    def grade_board(self, board, player=0):
        max_score = max_value_state(self.net, self.sample_size, board)
        enemy_score = max_value_state(self.net, self.sample_size, np.multiply(board, np.array([-1 * player])))
        return max_score - enemy_score
