'''
Main logic module for the Tic Tac Toe game.
It is not optionized for a quality game, it simply
generates random moves and checks the result of a
move for a winning line.
Exposed Functions:
newGame()
saveGame()
restoreGame()
userMove()
botMove()
'''
import os
import random
import data


def newGame():
    return list(" " * 9)


def saveGame(game):
    data.saveGame(game)


def restoreGame():
    try:
        game = data.restoreGame()
        if len(game) == 9:
            return game
        else:
            return newGame()
    except IOError:
        return newGame()


def _generateMove(game):
    valid_moves = [x for x in range(len(game)) if game[x] == " "]
    if valid_moves:
        return random.choice(valid_moves)
    else:
        return -1


def _isWinningMove(game):
    wins = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    )

    for a, b, c in wins:
        chars = game[a] + game[b] + game[c]
        if chars in ['XXX', 'OOO']:
            return True
    return False


def userMove(game, cell):
    if game[cell] != ' ':
        raise ValueError("Invalid Cell")
    else:
        game[cell] = 'X'

    if _isWinningMove(game):
        return "X"
    else:
        return ''


def botMove(game):
    cell = _generateMove(game)
    if cell == -1:
        return 'D'
    game[cell] = 'O'

    if _isWinningMove(game):
        return "O"
    else:
        return ''


def test():
    result = ""
    game = newGame()
    while not result:
        print(game)
        try:
            result = userMove(game, _generateMove(game))
        except ValueError:
            print("That shouldn't happen")
        if not result:
            result = botMove(game)

        if not result:
            continue
        elif result == 'D':
            print("Draw")
        else:
            print("Winner is:", result)
        print(game)


if __name__ == '__main__':
    test()
