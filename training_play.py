from sklearn.neural_network import MLPRegressor

import connect_four
from agent import RandomAgent
from alpha_beta import MiniMaxAgent
from graders import ScaledGrader
from nets import NeuralAgent
from trainers import TrainingAgent

net = MLPRegressor(hidden_layer_sizes=(30, 15), max_iter=100, alpha=1e-2, random_state=1,
                                solver='sgd', tol=1e-2, learning_rate_init=0.1, warm_start=True)

n_iter = 3
learner = MiniMaxAgent(reach=1, grader=ScaledGrader)
agent1 = TrainingAgent(agent=learner, classifier=net)
agent2 = RandomAgent()
#agent2 = MiniMaxAgent(reach=3)

connect_four.run_games(agent1, agent2, n_iter)

# Neural Network
print '--- Neural Network Training ---'
agent3 = NeuralAgent()
agent3.net = agent1.clf

print '--- Neural Network Prep ---'
#train_agent(agent3, n_train=2000, n_batch=5)
#test_agent(agent3, 10)

print '--- Neural Network Trials ---'
connect_four.run_games(agent3, agent2, n_iter)
