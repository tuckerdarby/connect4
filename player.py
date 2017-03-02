from agent import Agent
import numpy as np


class Player(Agent):
    def __init__(self):
        super(Player, self).__init__()

    def play(self, board):
        player_board = np.array(board)
        for row in player_board:
            for i, value in enumerate(row):
                if value == -0:
                    row[i] = 0
        print player_board
        print ' -----------------------------'
        print ' [ 0   1   2   3   4   5   6 ]'
        x = int(raw_input('select column: '))
        self._game.play(self.player, x)