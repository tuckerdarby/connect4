from game import Game


def run_games(agent1, agent2, n_iter=1, final=True, printing=False):
    wins = {-1: 0, 1: 0, 0: 0}

    for i in range(n_iter):
        print 'game:', i
        game = Game()
        agent1.set_game(game)
        agent2.set_game(game)
        while game.status == 'playing':
            agent1.play(game.get_board(1))
            if game.status == 'playing':
                agent2.play(game.get_board(-1))
        wins[game.winner] += 1
        print 'WINNER', game.winner
        print wins, game.winner
        print game.get_board(agent1.player)

        # print('Player', game.winner, 'has won the game in', game.turn, 'turns')
    if printing:
        print 'Player 1 Win Ratio:', (1.0*wins[1]/(1.0*wins[1]+wins[-1])) * 100.0

    # if final:
    #     agent1.end()
    #     agent2.end()

    return wins
