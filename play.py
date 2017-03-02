import connect_four
import net_help
from alpha_beta import MiniMaxAgent
from graders import SubsampleNetGrader

net_name = 'mlp-S6x6-mock'
#net_name = 'D4x4_mlp_net_L32x32'
sample_size = (6, 6)

n_iter = 20
#agent1 = MiniMaxAgent(reach=1)
#agent1 = SubsampleNeuralAgent(net, sample_size=sample_size)
agent1 = MiniMaxAgent(reach=1)
net = net_help.load_net(net_name)

net_grader = SubsampleNetGrader(net, sample_size)
agent1.grader = net_grader
# agent2 = SubsampleNeuralAgent(net, sample_size=sample_size)
# agent2 = RandomAgent()
# agent2 = Player()

agent2 = MiniMaxAgent(reach=0)

# net2 = rev_train.load_net(net_name2)
# net_grader2 = SubsampleNetGrader(net2, sample_size)
# agent2.grader = net_grader2

connect_four.run_games(agent2, agent1, n_iter)
