import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from pipes import Pipe


def classifier_reports(pipes, board_shapes, realities):
    print 'Running Report...'
    for pipe in pipes:
        for model_shape in board_shapes:
            for realistic in realities:
                pipe.run_models(model_shape, realistic)


def trial_report():
    # Hard Coded for Report

    rf = RandomForestRegressor
    rf_info = Pipe(rf, 'rf', iters=1)

    mlp = MLPRegressor
    mlp_params = [
        # ('0', {'hidden_layer_sizes': (49, )}),
        # ('1', {'hidden_layer_sizes': (49, 16)}),
        ('2', {'hidden_layer_sizes': (49, 49)}),
        ('hls_49x49x49', {'hidden_layer_sizes': (49, 49, 49)}),
        # ('test_49x49x16', {'hidden_layer_sizes': (49, 49, 16)}),
        # ('3D', {'hidden_layer_sizes': (49, 49, 32)}),
        # ('3E', {'hidden_layer_sizes': (49, 49, 80)}),
        # ('5A', {'hidden_layer_sizes': (80, 20)}),
        # ('5B', {'hidden_layer_sizes': (80, 40)}),
        # ('6C', {'hidden_layer_sizes': (80, 80)}),
        # ('7A', {'hidden_layer_sizes': (100, 100)}),
        # ('7B', {'hidden_layer_sizes': (100, 80)}),
        # ('7C', {'hidden_layer_sizes': (100, 120)}),
        # ('7D', {'hidden_layer_sizes': (100, 100, 49)}),
        # ('7E', {'hidden_layer_sizes': (100, 100, 80)}),
        # ('7F', {'hidden_layer_sizes': (100, 100, 100)}),
        # ('7G', {'hidden_layer_sizes': (100, 100, 100, 49)}),
        # ('7H', {'hidden_layer_sizes': (100, 100, 100, 100)}),
        # ('8', {'hidden_layer_sizes': (120, 120, 100, 49)}),
        # ('9', {'hidden_layer_sizes': (160, 200, 160, 49)}),
        # ('10', {'hidden_layer_sizes': (200, 200, 100, 49)}),
        # ('11', {'hidden_layer_sizes': (150, 200, 150, 50)}),
        # ('12A', {'hidden_layer_sizes': (300, 400, 200, 100)}),
        # ('12B', {'hidden_layer_sizes': (400, 400, 300, 200)}),
        # ('12C', {'hidden_layer_sizes': (400, 500, 200, 200)}),
        # ('DIM7_A', {'hidden_layer_sizes': (2000, 3000, 3000, 2000, 1000, 600, 600)}),
        # ('DIM7_B', {'hidden_layer_sizes': (1600, 2000, 2000, 1600, 1000, 600, 600)})
    ]
    mlp_info = Pipe(mlp, 'mlp', iters=10, batch=1000, agent_batch=0,
                    agent_monitor=False, model_params=mlp_params, save=True, fresh=False)
    mdls = [rf_info, mlp_info]

    b = [(4, 4), (6, 6)]
    rs = [True, False]
    classifier_reports(mdls, b, rs)

    return mdls


model_pipes = trial_report()  # Returns stats for model and game

M = model_pipes[1].model_stats.all()
G = model_pipes[1].game_stats.all()


print M
print G
sns.heatmap(M)
# sns.heatmap(G.stats['mlp'])

sns.plt.show()


# Notes


# # Report Loop
# Repeat for Model Classifiers:
#    Repeat for [Board Sizes -> Standard vs. Revolution]:
#      Repeat for [Realistic, Non-realistic]:
#          Train Model Against Sample Data
#              ->Potential for testing Agent performance here as well
#          Test Model Against Sample Data *Make sure to save model too
#          Init Appropriate Model Agent (Standard vs. Revolution) ~ Possibly not needed

#          Repeat for Agent as [Player 1, Player 2]:
#              Play against Minimax agent
#      Save Stats
