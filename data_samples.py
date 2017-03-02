import numpy as np


def create_samples(grader, amount, sample_shape=(7, 7), realistic=True, margin=0):
    states = []
    grades = []
    sample_size = int(sample_shape[0] * sample_shape[1])
    for i in range(amount):
        if realistic:
            area = mock_board(sample_shape, margin=margin)
            state = area.flatten()
        else:
            area, state = random_board(sample_size, sample_shape)
        grade = grader.grade_board(area, 1)
        states.append(state)
        grades.append(grade)
    return states, grades


def random_board(size=49, shape=(7, 7)):
    state = np.random.random_integers(-1, 1, size)
    area = state.reshape(shape)
    return area, state


def mock_board(shape=(7, 7), margin=0):
    mat = np.zeros(shape)
    for row in mat:
        width = mat.shape[1]
        if np.random.randint(0, 2) == 0:
            fillable = [-1, 1]
        else:
            fillable = [1, -1]
        row_fill_to = np.random.randint(0, width - margin)
        for i in range(row_fill_to):
            v = np.random.randint(0, 2)
            row[i] = fillable[v]
    return np.rot90(mat, 1)
