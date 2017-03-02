from graders import Grader
from data_samples import create_samples


grader = Grader()
# grader = ScaledGrader()


def batch_train(mdl, amount=10000, batch=1000, n_iter=-1, sample_shape=(4, 4), realistic=True):
    if n_iter == -1:
        n_iter = amount/batch
        # print n_iter
    for i in range(n_iter):
        if n_iter > 1:
            print (i * 100.0 / n_iter)
        states, grades = create_samples(grader, batch, sample_shape=sample_shape, realistic=realistic)
        try:
            mdl.partial_fit(states, grades)
        except Exception:
            mdl.fit(states, grades)
    return mdl


def test_score_net(mdl, amount=1000, sample_shape=(4, 4), realistic=True):
    # Test net and return score
    test_states, test_grades = create_samples(grader, amount, sample_shape=sample_shape, realistic=realistic)
    score = mdl.score(test_states, test_grades)
    return score
