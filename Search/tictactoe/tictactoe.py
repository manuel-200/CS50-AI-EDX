"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    xcount = 0
    ocount = 0
    for i in board:
        for j in i:
            if j == X:
                xcount = xcount + 1
            elif j == O:
                ocount = ocount + 1
    if xcount > ocount:
        return O
    elif xcount == ocount:
        return X


def actions(board):
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    newB = copy.deepcopy(board)
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    else:
        newB[action[0]][action[1]] = player(board)
    return newB


def winner(board):
    for i in board:
        if i[0] == i[1] and i[1] == i[2]:
            return i[0]
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            return board[0][j]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    if winner(board) == X or winner(board) == O:
        return True
    else:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
        return True


def utility(board):
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def maxv(board):
    if terminal(board):
        return utility(board)
    v = -99999999
    for action in actions(board):
        v = max(v, minv(result(board, action)))
    return v


def minv(board):
    if terminal(board):
        return utility(board)
    v = 99999999
    for action in actions(board):
        v = min(v, maxv(result(board, action)))
    return v


def minimax(board):
    actL = list(actions(board))
    if terminal(board) == True:
        return None
    elif player(board) == X:
        minma = []
        for i in range(len(actL)):
            if terminal(result(board, actL[i])):
                if utility(result(board, actL[i])) == 1:
                    return actL[i]
            minma.append(minv(result(board, actL[i])))
        maxi = max(minma)
        return actL[minma.index(maxi)]
    elif player(board) == O:
        minma = []
        for i in range(len(actL)):
            if terminal(result(board, actL[i])):
                if utility(result(board, actL[i])) == -1:
                    return actL[i]
            minma.append(maxv(result(board, actL[i])))
        mini = min(minma)
        return actL[minma.index(mini)]