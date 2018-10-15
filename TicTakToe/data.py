'''
Tic Tac Toe data layer
It saves and restores the game board. The functions are:
    saveGame(game) -> None
    restoreGame(game) -> game
There are no limites on the size of the data.
The game implementation is
responsible for validating all data in an out
'''
import os.path
game_file = ".ticTakToe.dat"


def _getPath():
    '''
    getPath -> string
    Returns a valid path for data file.
    Tries to use the home folder
    '''
    try:
        game_path = os.environ['HOMEPATH'] or os.environ['HOME']
        if not os.path.exists(game_path):
            game_path = os.getcwd()
    except (KeyError, TypeError):
        game_path = os.getcwd()
    return game_path


def saveGame(game):
    '''
    saveGame(game) -> None
    Saves a game object in the datafile in th users homefolder.
    No checking is done on the input which is expeced to be a
    list of characters
    '''
    path = os.path.join(_getPath(), game_file)
    try:
        with open(path, 'w') as gf:
            game_str = ''.join(game)
            gf.write(game_str)
    except FileNotFoundError:
        print("Failed to save file.")


def restoreGame():
    '''
    restoreGame() -> game
    Restores a game from the datafile.
    The game object us a list of characers.
    '''
    path = os.path.join(_getPath(), game_file)
    with open(path) as gf:
        game_str = gf.read()
        return list(game_str)


def test():
    print("Path = ", _getPath())
    saveGame("XO XO OX")
    print(restoreGame())


if __name__ == "__main__":
    test()
