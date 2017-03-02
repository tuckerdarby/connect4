import connect_four
from data_samples import create_samples
from model_help import test_score_net
from model_agent import ModelAgent, RevolutionModelAgent
from alpha_beta import MiniMaxAgent
from graders import Grader
from net_help import load_net, save_net
from stats import Stats, GameStats


def name_stat(model_name, dims, realistic, nick=''):
    if realistic:
        real_name = 'mock'
    else:
        real_name = 'noise'
    dim_name = 'x'.join(map(str, dims))
    if nick != '':
        model_name = '-'.join([model_name, nick])
    stat_name = '-'.join([model_name, dim_name, real_name])
    return stat_name


def agent_trial(model, shape, batch):
    if shape[0] == 7 and shape[1] == 7:  # Full board model
        agent = ModelAgent(model)
    else:
        agent = RevolutionModelAgent(model, shape)
    enemy = MiniMaxAgent(reach=1)
    results1 = connect_four.run_games(agent, enemy, batch, final=False)
    results2 = connect_four.run_games(enemy, agent, batch, final=True)
    return results1, results2


class Pipe(object):
    def __init__(self, model, name, title='', batch=1000, iters=3, agent_batch=0, agent_monitor=True,
                 model_params=None, fresh=True, save=False, grader=None):
        self.model = model
        self.name = name
        self.title = title
        self.batch = batch
        self.iters = iters
        self.agent_batch = agent_batch
        self.agent_monitor = agent_monitor
        self.fresh = fresh
        self.save = save
        self.stats = {}
        self.stat_list = []
        self.model_stats = Stats()
        self.game_stats = GameStats()
        if model_params is None:
            self.model_params = [('', {})]
        else:
            self.model_params = model_params
        if title == '':
            self.title = name
        else:
            self.title = title
        if grader is None:
            self.grader = Grader()
        else:
            self.grader = grader
        self.model_stats.new_tracker(self.name)
        self.game_stats.new_tracker(self.name)

    def run_models(self, model_shape, realistic):
        for param_name, model_params in self.model_params:
            # get model name based on inputs
            if self.fresh:
                model = self.model(**model_params)
            else:
                model_name = self._name_model(model_shape, realistic, param_name)
                model = load_net(model_name)
            scores = self._model_trial(model, model_shape, realistic)
            self._log_run(model, model_shape, realistic, param_name, scores)
        self._save_stats()

    def _log_run(self, model, model_shape, realistic, param_name, scores):
        model_name = self._name_model(model_shape, realistic, param_name)
        model_scores, game_scores = scores
        stats_name = '-'.join([model_name, param_name])
        self.model_stats.set_stat(self.name, stats_name, model_scores)
        self.game_stats.set_stat(self.name, stats_name, game_scores)
        self._save_model(model, model_name)

    def _name_model(self, model_shape, realistic, param_name):
        shape_tag = 'S' + 'x'.join(map(str, model_shape))
        realism = 'mock'
        if not realistic:
            realism = 'rndm'
        name_tags = [self.name, shape_tag, realism]
        if param_name != '':
            param_tag = 'P_' + param_name
            name_tags.append(param_tag)
        return '-'.join(name_tags)

    def _save_stats(self):
        iters = 'x'.join(map(str, [self.iters, self.batch]))
        self.model_stats.save_stats(name='model', iters=iters)
        game_iters = 'x'.join(map(str, [self.iters, self.batch]))
        self.game_stats.save_stats(name='game', iters=game_iters)

    def _save_model(self, model, model_name):
        if not self.save:
            return
        save_net(model, model_name)

    def _model_trial(self, model, model_shape, realistic):
        # Train Model Against Sample Data
        model_scores = []
        agent_scores = []
        for i in range(self.iters):
            states, grades = create_samples(self.grader, self.batch, sample_shape=model_shape, realistic=realistic)
            # Check if the trial is batch training
            if self.iters > 1:
                # Partially fit the model since this will occur self.iters times
                print 'training model: %', (i * 100.0 / self.iters)
                model.partial_fit(states, grades)
            else:
                model.fit(states, grades)
            # Score Net mid-training
            model_score = test_score_net(model, self.batch, sample_shape=model_shape, realistic=realistic)
            model_scores.append(model_score)
            # Check if agent trials should occur mid-training
            if self.agent_monitor and self.agent_batch > 0:
                # Do mid-training agent trials
                agent_results = agent_trial(model, model_shape, self.agent_batch)
                agent_scores.append(agent_results)
        # Full Agent Trial
        if self.agent_batch > 0:
            agent_results = agent_trial(model, model_shape, self.agent_batch)
            agent_scores.append(agent_results)
        return model_scores, agent_scores
