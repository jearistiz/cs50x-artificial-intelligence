"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from typing import List, Literal, Optional


X = "X"
O = "O"
EMPTY = None

winning_states = set(
    (
        ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)),
        ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
    )
)


def initial_state() -> list:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: List[List]) -> str:
    """
    Returns player who has the next turn on a board.
    """
    nx = sum(line.count(X) for line in board)
    no = sum(line.count(O) for line in board)
    return O if nx > no else X


def actions(board: list) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    N = len(board)
    actions_set = set((i, j) for i in range(N) for j in range(N) if not board[i][j])
    return actions_set


def result(board: list, action: tuple) -> list:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('Not a possible action on board')

    result = deepcopy(board)
    next_player = player(board)
    i, j = action
    result[i][j] = next_player

    return result


def winner(board: list) -> Optional[str]:
    """
    Returns the winner of the game, if there is one.
    """
    for winning_state in winning_states:
        possible_win = list(board[i][j] for i, j in winning_state)
        ref = possible_win[0]
        win = all((value == ref and value) for value in possible_win)
        if win:
            return X if possible_win[0] == X else O

    return None


def terminal(board: list) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    board_full = all(all(line) for line in board)
    return board_full or winner(board)


def utility(board: list) -> Literal[1, 0, -1]:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    wins = winner(board)
    if wins == X:
        return 1
    elif wins == O:
        return -1
    else:
        return 0


def minimax(board: list):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -10
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = 10
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    if terminal(board):
        return None

    possible_actions = list(actions(board))
    utility_values = []

    if player(board) == X:
        for action in possible_actions:
            new_board = result(board, action)
            utility_values.append(min_value(new_board))
        i = utility_values.index(max(utility_values))
    else:
        for action in possible_actions:
            new_board = result(board, action)
            utility_values.append(max_value(new_board))
        i = utility_values.index(min(utility_values))

    return possible_actions[i]
