# SKLearn
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostRegressor
# Connect4
from model_help import create_samples
from model_help import batch_train
from stats import Stats

stats = Stats()
models = [
    ('SVR', SVR()),
    ('RF', RandomForestRegressor()),
    ('NB', GaussianNB()),
    ('Ada', AdaBoostRegressor())
]
model_names = [model[0] for model in models]

for name, model in models:
    stats.new_tracker(name)
    stats.track_stats(name, ('Trained', 'Score'))


def train_test(mdl, amount, train_percent=0.8, batch=1000, sample_shape=(4, 4)):
    n_train = int(train_percent * amount)
    batch_train(mdl, n_train, batch=batch, sample_shape=sample_shape)
    states, values = create_samples(amount - n_train, sample_shape=sample_shape)
    try:
         score = mdl.score(states, values)
         return score
    except Exception:
        print 'no scoring function'


def train_test_score(mdl, amount, batch=1000, train_percent=0.8, sample_shape=(4, 4)):
    n_batches = int(amount/batch)
    scores = []
    batch_amount = int(train_percent * batch)
    for i in range(n_batches):
        print 'batch', i
        score = train_test(mdl, batch, train_percent=train_percent, batch=batch_amount, sample_shape=sample_shape)
        print 'running score', score
        scores.append(score)

n_iter = 100000
shape = (4, 4)

svr = SVR()
rfr = RandomForestRegressor(n_estimators=100, warm_start=True)

train_test_score(rfr, n_iter, sample_shape=shape)


