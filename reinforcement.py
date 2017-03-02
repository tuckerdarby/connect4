import numpy as np
import pandas as pd
from agent import RandomAgent
from graders import Grader


def state_def(board):
    return str(board.flatten())


def save_states(name, board_size, states):
    print 'saving states'
    size = len(states)
    value_df = pd.DataFrame(index=range(size), columns=['value'])
    state_df = pd.DataFrame(index=range(size), columns=range(board_size))
    for i, state in enumerate(states):
        value = states[state]
        value_df.ix[i] = value
        flat = state.replace('[', '').replace(']', '').replace('.', '').split()
        state_df.ix[i] = flat
    print 'converting to csv'
    value_df.to_csv(name+'_values.csv')
    state_df.to_csv(name + '_states.csv')
    print 'saved states:', name


def read_saved_states(name):
    states = {}
    try:
        value_df = pd.read_csv(name+'_values.csv')
        state_df = pd.read_csv(name+'_states.csv')
        for i in range(len(value_df)):
            flat = np.array(state_df.ix[i][1:])
            value = value_df.ix[i][0]
            state = str(flat)
            states[state] = value
    except:
        print 'starting new:', name
    return states


class StateAgent(RandomAgent):
    def __init__(self, name='q_agent', alpha=1, gamma=1, epsilon=1, grader=Grader, saving=False):
        super(StateAgent, self).__init__()
        self.actions = range(self._game.board_width)
        self.action_dict = {action: i for i, action in enumerate(self.actions)}
        self.Q = read_saved_states(name)
        self.c_games = 0
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.name = name
        self.saving = saving
        self.grader = grader(self.player)

    def play(self, board):
        random = np.random.random()
        if random > self.epsilon:
            super(StateAgent, self).play(board)
        else:
            self._make_action(board)
        board = self._game.get_board(self.player)
        score = self.grader.grade_board(board)
        self._update_state(board, score)

    def _update_state(self, board, reward):
        state = self._state_board(board)
        if self._game.status == 'over':
            self.Q[state] = reward
            if self.saving:
                save_states(self.name, board.shape[0] * board.shape[1], self.Q)
            return reward
        else:
            estimate = self.Q[state]
            utility = reward - self.gamma * estimate
            value = self.alpha * utility
            self.Q[state] += value
            return value

    def save_states(self, board_size=49):
        save_states(self.name, board_size, self.Q)

    def _state_board(self, board):
        state = state_def(board)
        if state not in self.Q:
            self.Q[state] = 0
        return state

    def _max_actions(self, board):
        valid_actions = []
        max_estimate = -99999
        for action in self.actions:
            top = self._game._first_open_row(action)
            # if board[action, 0] != 0:
            if top == -1:
                continue
            estimate = self._check_state(board, action, top)
            if estimate == max_estimate:
                valid_actions.append(action)
            elif estimate > max_estimate:
                valid_actions = [action]
                max_estimate = estimate
        return valid_actions

    def _check_state(self, board, action, top):
        checker = np.array(board)
        checker[top, action] = 1
        state = self._state_board(checker)
        return self.Q[state]

    def _make_action(self, board):
        action = -1
        valid = False
        while not valid:
            valid_actions = self._max_actions(board)
            if len(valid_actions) > 1:
                index = np.random.randint(0, len(valid_actions) - 1)
            elif len(valid_actions) == 1:
                index = 0
            else:
                print 'Index Error:', self._game.board
                break
            action = valid_actions[index]
            valid = self._game.play(self.player, action)
            valid_actions.remove(action)
        return action

    def _set_game(self, game):
        super(StateAgent, self).set_game(game)
        self.actions = range(self._game.board_width)
        self.action_dict = {action: i for i, action in enumerate(self.actions)}
        self.c_games += 1
        #self.alpha -= 0.0001
        #self.gamma -= 0.0001
        #self.epsilon -= 0.0001
        self.epsilon = (np.exp(-0.0018 * self.c_games))  # exploration
        self.alpha = (np.exp(-0.004 * self.c_games))  # learning


