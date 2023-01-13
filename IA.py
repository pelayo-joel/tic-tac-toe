import random

"""The code for both AI, an easy one and an impossible one"""

"""EasyIA just plays randomly"""
def EasyIA(board):
    pos = ["A", "B", "C"]
    position = ""
    while True:        
        x = random.randint(0, 2)
        y = random.randint(0, 2)

        if board[x][y] == " ":
            position = pos[x] + str(y+1)
            break
            
    return position

"""DrawIA uses the Minimax algorithm to win or draw if its opponent plays optimally as well"""
def DrawIA(board, sign):
    pos = ["A", "B", "C"]
    bestVal = -10
    bestPos = ""

    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = sign
                moveVal = Minimax(board, sign, 0, False)
                board[row][col] = " "
                if moveVal > bestVal:
                    bestPos = pos[row] + str(col+1)
                    bestVal = moveVal

    return bestPos


"""The Minimax algorithm itself"""
def Minimax(board, sign, depth, isMax):
    opponent = ""
    if sign == "X":
        opponent = "O"
    else:
        opponent = "X"

    moveValue = WinCheck(board, sign)
    if moveValue == 1:
        return moveValue
    elif moveValue == -1:
        return moveValue

    if AvailableBox(board) == False:
        return 0

    if isMax:
        best = -10
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = sign
                    best = max(best, Minimax(board, sign, depth+1, not isMax))
                    board[row][col] = " "
        return best
    else:
        best = 10
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = opponent
                    best = min(best, Minimax(board, sign, depth+1, not isMax))
                    board[row][col] = " "
        return best

"""Utility for minimax function, basically checks if the boad is is a draw state"""
def AvailableBox(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return True
    return False

"""Utility for minimax, checks if the board is in a winning or losing state, returns 0 if none and that means that the game isn't finished"""
def WinCheck(board, sign):
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == sign:
            return 1
        elif board[0][col] == board[1][col] == board[2][col] != " " != sign:
            return -1
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == sign:
            return 1
        elif board[row][0] == board[row][1] == board[row][2] != " " != sign:
            return -1
    if ((board[0][0] == board[1][1] == board[2][2] == sign) or
        (board[2][0] == board[1][1] == board[0][2] == sign)):
        return 1
    elif ((board[0][0] == board[1][1] == board[2][2] != " " != sign) or
        (board[2][0] == board[1][1] == board[0][2] != " " != sign)):
        return -1
    return 0