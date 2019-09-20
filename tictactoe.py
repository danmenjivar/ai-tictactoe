from os import system
from math import inf as infinity
from random import choice
import platform
import time

'''
Assignment #4
Intro to AI
Daniel Quintana Menjivar
Inspired by: https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py 
'''

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def clean(): #  method cleans the console for better printing
    if 'windows' in platform.system().lower():
        system('cls')
    else:
        system('clear')

def render(state, aiMark, humanMark): # prints the board
    chars = {
        -1: humanMark,
        +1: aiMark,
        0: ' '
    }
    strLine = '---------------'
    print('\n' + strLine)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + strLine)

def evaluate(state): #  makes heuristic evaluation of the current state
    score = 0
    if isWinner(state, COMP):
        score += 1
    elif isWinner(state, HUMAN):
        score -= 1
    else:
        score = 0 # draw

    return score

def isWinner(state, player): #  tests if a specific player wins
    win_state = [ # either 3 rows, 3 columns, or 2 diagonals
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def isGameOver(state): #  check if AI or human player has won
    return isWinner(state, HUMAN) or isWinner(state, COMP)

def emptyCells(state): # pupulates a list of all the empty cells in the current state of the board
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

def isValidMove(x, y): # check if the passed cell coordinates are valid (i.e. an empty cell)
    if [x, y] in emptyCells(board):
        return True
    else:
        return False

def setMove(x, y, player): #  after checking if the move is valid, do so
    if isValidMove(x, y):
        board[x][y] = player
        return True
    else: 
        return False

def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or isGameOver(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in emptyCells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score #  max value
        else:
            if score[2] < best[2]:
                best = score #  min value

    return best

def aiTurn(aiMark, humanMark): #  calls the minimax function if the depth < 9, else it choices a random coordinate
    depth = len(emptyCells(board))
    if depth == 0 or isGameOver(board):
        return

    clean()
    print(f'Computer turn [{aiMark}]')
    render(board, aiMark, humanMark)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    setMove(x, y, COMP)
    time.sleep(1)

def humanTurn(aiMark, humanMark):
    depth = len(emptyCells(board))
    if depth == 0 or isGameOver(board):
        return
    move = -1
    moves = { #  dictionary of valid moves
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    clean()
    print(f'Human turn [{humanMark}]')
    render(board, aiMark, humanMark)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9: )'))
            coordinates = moves[move]
            canMove = setMove(coordinates[0], coordinates[1], HUMAN)

            if not canMove:
                print('Poor move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('exiting')
            exit()
        except(KeyError, ValueError):
            print('Bad choice')

def main():
    clean()

    humanMark = '0'
    aiMark = 'X'
    first = '' # should user go first?

    while first != 'Y' and first != 'N': # initializing whether human or agent X goes first
        try:
            first = input('Would you like to go first?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('exiting')
            exit()
        except (KeyError, ValueError):
            print("error: poor choice")
    
    while len(emptyCells(board)) > 0 and not isGameOver(board): #  Main game loop
        if first == 'N':
            aiTurn(aiMark, humanMark)
            first = '' #  terminate first condition for next iteration

        humanTurn(aiMark, humanMark)
        aiTurn(aiMark, humanMark)

    if isWinner(board, HUMAN):
        clean()
        print(f'Human turn [{humanMark}]')
        render(board, aiMark, humanMark)
        print('CONGRATULATIONS, YOU WIN!')
    elif isWinner(board, COMP):
        clean()
        print(f'Computer turn [{aiMark}]')
        render(board, aiMark, humanMark)
        print('SORRY, YOU LOSE!')
    else:
        clean()
        render(board, aiMark, humanMark)
        print('DRAW!')

    exit()

if __name__ == '__main__':
    main()