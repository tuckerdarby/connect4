import numpy as np


def count_array(arr, player):
    count = 0
    max_count = 0
    for i in range(len(arr)):
        if arr[i] == player:
            count += 1
            max_count = max(max_count, count)
        else:
            count = 0
    return max_count


def next_states(board, player, index=False):
    states = []
    indexes = []
    for x in range(board.shape[1]):
        for y in range(board.shape[0] - 1, -1, -1):
            if board[y, x] == 0:
                state = np.array(board)
                state[y, x] = player
                states.append(state)
                indexes.append(x)
                break
    if index:
        return states, indexes
    return states


def next_state(board, player, action):
    for y in range(board.shape[0] - 1, -1, -1):
        if board[y, action] == 0:
            board[y, action] = player
    return board
