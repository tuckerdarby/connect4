import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date


def visualize_dict_data(names, data):
    fig = sns.plt.figure()
    num = len(names)
    for i in range(num):
        ax = fig.add_subplot(num, 1, 1 + i)
        ax.set_title(names[i])
        values = map(lambda x: x[names[i]], data)
        ax.plot(values)
    sns.plt.show()


class Stats(object):
    def __init__(self):
        self.stats = {}
        self.tracker_list = []

    def new_tracker(self, name):
        if name not in self.tracker_list:
            self.tracker_list.append(name)
            self.stats[name] = pd.DataFrame()

    def track_stats(self, tracker_name, stat_names=()):
        for stat_name in stat_names:
            self.stats[tracker_name][stat_name] = []

    def add_stat(self, tracker_name, stat_name, stat):
        self.stats[tracker_name][stat_name].append(stat)

    def add_stats(self, tracker_name, stat_names, stats):
        for stat_name, stat in zip(stat_names, stats):
            self.stats[tracker_name][stat_name].append(stat)

    def set_stat(self, tracker_name, stat_name, stats):
        if stat_name in self.stats[tracker_name].keys():
            print tracker_name, stat_name
            self.stats[tracker_name][stat_name].append(pd.Series(stats))
        else:
            self.stats[tracker_name][stat_name] = pd.Series(stats)

    def get_stat(self, name):
        return self.stats[name]

    def _get_save_name(self, name='', iters=''):
        save_name = []
        if name != '':
            save_name.append(name)
        if iters != '':
            save_name.append(iters)
        today = str(date.today())
        save_name.append(today)
        return '-'.join(save_name)

    def save_stats(self, name='', iters='', directory='saved_stats/'):
        named = self._get_save_name(name, iters=iters)
        for tracker in self.stats.keys():
            save_name = tracker + '-' + named
            self.stats[tracker].to_csv(directory+save_name+'.csv')

    def save_all(self, name, iters='', directory='saved_stats/'):
        save_name = self._get_save_name(name, iters=iters)
        stats = self.all()
        stats.to_csv(directory+save_name+'.csv')


    def graph_stat(self, tracker_name, stat_name):
        print 'graphing'

    def correlate(self, tracker_name, stat_names=None):
        if stat_names is None:
            stat_names = self.stats[tracker_name].keys()
        stats = self.stats[tracker_name][stat_names]
        correlations = stats.corr()
        fig, ax = plt.subplots()
        sns.heatmap(correlations, square=True)
        heats = correlations.columns.get_level_values('stats')
        for i, stat_name in enumerate(heats):
            if i and stat_name != heats[i - 1]:
                ax.axhline(len(heats) -i, c="w")
                ax.axvline(i, c="w")
        fig.show()

    def snapshot(self, tracker_name):
        print self.stats[tracker_name]
        for ms in self.stats[tracker_name]:
            st = self.stats[tracker_name][ms]
            print ms, st.mean(), st[len(st) - 1]

    def all(self):
        all_df = None
        for tracker_name in self.stats.keys():
            if all_df is None:
                all_df = pd.DataFrame(self.stats[tracker_name])
            else:
                all_df = all_df.join(self.stats[tracker_name])
        return all_df


class GameStats(Stats):
    def __init__(self, player=1):
        super(GameStats, self).__init__()
        self.player = player

    def set_stat(self, tracker_name, stat_name, stats):
        wins, losses = [], []
        print stats
        for stat in stats:
            wins.append(stat[0][1])
            losses.append(stat[0][-1])
            wins.append(stat[1][-1])
            losses.append(stat[1][1])
        self.stats[tracker_name][stat_name+'_wins'] = pd.Series(wins)
        self.stats[tracker_name][stat_name + '_losses'] = pd.Series(losses)


