import numpy as np
from game_helper import count_array


class Game(object):
    def __init__(self, round_number=0):
        self.board_width = 7
        self.board_height = 7
        self.board = np.zeros(shape=(self.board_height, self.board_width))
        self.connect_win = 4
        self.turn = 0
        self.player_turn = 1
        self.status = 'setup'
        self.winner = 0
        self.reward = 1000
        self._agents = []
        self.moves = []
        self.round_number = round_number

    def add_agent(self, agent):
        self._agents.append(agent)
        player = len(self._agents)
        if player == 2:
            player = -1
            self.status = 'playing'
        return player

    def get_board(self, player):
        return player * np.array(self.board)

    def play(self, player, x):
        y = self._first_open_row(x)
        if y == -1 or self.player_turn != player or self.board[y, x] != 0 or self.status != 'playing':
            return False, 0
        self.turn += 1
        self.board[y, x] = player
        self._check_status(specific_player=player)
        if self.status == 'playing':
            self.player_turn *= -1
        return True

    def reward_agents(self):
        reward = 100
        if self.winner == 1:
            winner = self._agents[0]
            loser = self._agents[1]
        elif self.winner == -1:
            winner = self._agents[1]
            loser = self._agents[0]
        else:
            return
        winner.reward(reward)
        loser.reward(-1*reward)

    def _first_open_row(self, column):
        row = 1
        if column > 10:
            print 'YO COLUMN FKED UP NIG NOG'
            print column
        while row <= self.board_height:

            if self.board[self.board_height - row, column] == 0:
                return self.board_height - row
            row += 1
        return -1

    def _check_status(self, specific_player=None):
        unique, counts = np.unique(self.board, return_counts=True)
        if 0 not in unique:
            print 'cats game'
            print unique, counts
            self.status = 'over'
        for player, piece_count in np.asarray((unique, counts)).T:
            if player == 0 or piece_count < 4 or (specific_player is not None and player != specific_player):
                continue
            if self._check_player_status(player):
                self.status = 'over'
                self.winner = player

    def _check_player_status(self, player):
        return self._check_horizontals(player) or self._check_verticals(player) or self._check_diagonals(player)

    def _check_horizontals(self, player):
        for i in range(self.board_height):
            row = self.board[:, i]
            if count_array(row, player) >= self.connect_win:
                return True
        return False

    def _check_verticals(self, player):
        for i in range(self.board_width):
            column = self.board[i]
            if count_array(column, player) >= self.connect_win:
                return True
        return False

    def _check_diagonals(self, player):
        diagonals = [self.board[::-1, :].diagonal(i) for i in range(-self.board.shape[0] + 1, self.board.shape[1])]
        diagonals.extend(self.board.diagonal(i) for i in range(self.board.shape[1] - 1, -self.board.shape[0], -1))
        for diagonal in diagonals:
            if count_array(diagonal, player) >= self.connect_win:
                return True
        return False
