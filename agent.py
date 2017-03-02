import numpy as np
from game import Game


class Agent(object):
    def __init__(self):
        self._game = Game()
        self.player = 0

    def play(self, board):
        print('base agent does not play', self.player)
        return -1

    def reward(self, amount):
        return self.player

    def set_game(self, game):
        self._game = game
        self.player = self._game.add_agent(self)

    def end(self):
        return


class RandomAgent(Agent):
    def __init__(self):
        super(RandomAgent, self).__init__()

    def play(self, board):
        random = np.random.randint(0, self._game.board_width)
        move = self._game.play(self.player, random)
        while move is False:
            random = np.random.randint(0, self._game.board_width)
            move = self._game.play(self.player, random)
        return random
