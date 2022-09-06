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
    """ if board == [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]:
            return X
    else: """
    xcount = 0
    ocount = 0
    for i in board:
        for j in i:
            if j == X: 
                xcount = xcount +1
            elif j == O:
                ocount= ocount +1
    if xcount>ocount:
        return O
    elif xcount==ocount:
        return X


def actions(board):
    actions = set()
    for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY: 
                    actions.add((i,j))
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
        if i[0] == i[1] and i[1]== i[2]:
            return i[0]
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j]== board[2][j]:
            return board[0][j]
    if board[0][0] == board[1][1] and board[1][1]== board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1]== board[2][0]:
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
    if terminal (board):
        return utility(board)
    v=-99999999
    for action in actions(board):
        v=max(v,minv(result(board,action)))
    return v

def minv(board):
    if terminal (board):
        return utility(board)
    v=99999999
    for action in actions(board):
        v=min(v,maxv(result(board,action)))
    return v

def minimax(board):
    if terminal(board) == True:
        return None
    elif player(board)==X:
        v=-99999999
        actM=(0,0)
        for acti in actions(board):
            if terminal(result(board,acti)):
                if utility(result(board,acti))==1:
                    return acti
        for actio in actions(board):
            newB = copy.deepcopy(board)
            newB[actio[0]][actio[1]] = O
            if terminal(newB):
                utility(newB) == -1
                return actio
        for action in actions(board):
            if v< maxv(result(board,action)):
                v = maxv(result(board,action))
                actM = action
        return actM
    elif player(board)==O:
        v=99999999
        actB=(0,0)
        for acti in actions(board):
            if terminal(result(board,acti)):
                if utility(result(board,acti))==-1:
                    return acti
        for actio in actions(board):
            newB = copy.deepcopy(board)
            newB[actio[0]][actio[1]] = X
            if terminal(newB):
                utility(newB) == 1
                return actio
        for action in actions(board):
            if v > minv(result(board,action)):
                v = minv(result(board,action))
                actB = action
        return actB