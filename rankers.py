def rank_array(arr, player):
    ranks = []
    current_count = 0
    for i in range(len(arr)):
        if arr[i] == player:
            current_count += 1
        else:
            if current_count > 1:
                ranks.append(current_count)
            current_count = 0
    if current_count > 1:
        ranks.append(current_count)
    return ranks


def rank_verticals(board, player):
    ranks = []
    board_width = board.shape[1]
    for i in range(board_width):
        column = board[:, i]
        column_ranks = rank_array(column, player)
        ranks.extend(column_ranks)
    return ranks


def rank_horizontals(board, player):
    ranks = []
    board_height = board.shape[0]
    for i in range(board_height):
        row = board[i]
        row_ranks = rank_array(row, player)
        ranks.extend(row_ranks)
    return ranks


def rank_diagonals(board, player):
    ranks = []
    diagonals = [board[::-1, :].diagonal(i) for i in range(-board.shape[0] + 1, board.shape[1])]
    diagonals.extend(board.diagonal(i) for i in range(board.shape[1] - 1, -board.shape[0], -1))
    for diagonal in diagonals:
        diagonal_ranks = rank_array(diagonal, player)
        ranks.extend(diagonal_ranks)
    return ranks


def rank_board(board, player):
    row_ranks = rank_horizontals(board, player)
    col_ranks = rank_verticals(board, player)
    dia_ranks = rank_diagonals(board, player)
    return row_ranks, col_ranks, dia_ranks


# only counts the horizontals and verticals
def count_zeroes(board, x, y):
    amount = 0
    width = board.shape[1]
    height = board.shape[0]
    for i in range(-1, 2, 2):
        if x + i in xrange(0, width):
            if board[y, x + i] == 0:
                amount += 1
        if y + i in xrange(0, height):
            if board[y + i, x] == 0:
                amount += 1
    return amount


def count_empties(board, player=1):
    amount = 0
    for y, row in enumerate(board):
        for x in range(len(row)):
            if board[y, x] == player:
                amount += count_zeroes(board, x, y)
    return amount