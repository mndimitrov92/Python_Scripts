'''
Main logic module for the Tic Tac Toe game.
It is not optionized for a quality game, it simply
generates random moves and checks the result of a
move for a winning line. Rewritten with class.
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


class Game():
    def __init__(self):
        self.board = list(" " * 9)

    def saveGame(self, game):
        data.saveGame(self.board)

    def restoreGame(self):
        try:
            self.board = data.restoreGame()
            if len(self.board) != 9:
                self.board = list(" " * 9)
            return self.board
        except IOError:
            self.board = list(" " * 9)
            return self.board

    def _generateMove(self):
        valid_moves = [x for x in range(
            len(self.board)) if self.board[x] == " "]
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return -1

    def _isWinningMove(self):
        wins = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )
        game = self.board
        for a, b, c in wins:
            chars = game[a] + game[b] + game[c]
            if chars in ['XXX', 'OOO']:
                return True
        return False

    def userMove(self, cell):
        if self.board[cell] != ' ':
            raise ValueError("Invalid Cell")
        else:
            self.board[cell] = 'X'

        if self._isWinningMove():
            return "X"
        else:
            return ''

    def botMove(self):
        cell = self._generateMove()
        if cell == -1:
            return 'D'
        self.board[cell] = "O"

        if self._isWinningMove():
            return "O"
        else:
            return ''


def test():
    result = ""
    game = Game()
    while not result:
        print(game.board)
        try:
            result = game.userMove(game._generateMove())
        except ValueError:
            print("That shouldn't happen")
        if not result:
            result = game.botMove()

        if not result:
            continue
        elif result == 'D':
            print("Draw")
        else:
            print("Winner is:", result)
        print(game.board)


if __name__ == '__main__':
    test()
