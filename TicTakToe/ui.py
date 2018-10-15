'''
User interface fir the tic tac toe game
Not using reusable functions.
'''
import logic
import tkinter
import tkinter.messagebox as mb

menu = [
    'Start a new game',
    'Resume game',
    'Help',
    'Quit'
]


def getMenuChoice(aMenu):
    '''
    getMenuChoice(aMenu) ->int

    takes a list of strings as input,
    displays as a numbered menu and
    loops until a valid number is selected.
    '''
    if not aMenu:
        raise ValueError('No menu content')

    while True:
        print('\n\n')
        for index, item in enumerate(aMenu, start=1):
            print(index, '\t', item)
        try:
            choice = int(input('\nChoose a menu option: '))
            if 1 <= choice <= len(aMenu):
                return choice
            else:
                print("Choose a number between 1 and", len(aMenu))
        except ValueError:
            print("Choose the number of the menu option")


def startGame():
    return logic.newGame()


def resumeGame():
    return logic.restoreGame()


def displayHelp():
    print(
        '''
        Start a new game of tic tac toe.
        Resume saved game restores the last saved game.
        Quit - quits the application
        '''
    )


def quitGame():
    print("Goodbye")
    raise SystemExit


def executeChoice(choice):
    '''
    executeChoice(int) ->None
    Executes the input choice.
    If it is a valid one, the game continues.
    '''
    dispatch = [startGame, resumeGame, displayHelp, quitGame]
    game = dispatch[(choice) - 1]()
    if game:
        playGame(game)


def printGame(game):
    display = '''
    _____________    _____________
    | 1 | 2 | 3 |    {} | {} | {} 
    |-----------|    -------------
    | 4 | 5 | 6 |    {} | {} | {} 
    |-----------|    -------------
    | 7 | 8 | 9 |    {} | {} | {} 
    _____________    _____________
    '''
    print(display.format(*game))


def playGame(game):
    result = ""
    while not result:
        printGame(game)
        choice = str(input("Cell 1-9 or q to quit: "))
        if choice.lower()[0] == 'q':
            save = mb.askyesno(
                "Save game", "Do you want to save before quitting?")
            if save:
                logic.saveGame()
            quitGame()
        else:
            try:
                cell = int(choice) - 1
                if not (0 <= cell <= 8):  # Range check
                    raise ValueError
            except ValueError:
                print("Choose from 1-9 or q to quit")
                continue

            try:
                result = logic.userMove(game, cell)
            except ValueError:
                mb.showerror("Invalid cell", "Choose an empty cell.")
                continue

            if not result:
                result = logic.botMove(game)
            if not result:
                continue
            elif result == "D":
                printGame(game)
                mb.showinfo("Result", "It's a draw")
            else:
                printGame(game)
                mb.showinfo("Winner", "The winner is {}".format(result))


def main():
    tk = tkinter.Tk()
    tk.withdraw()
    while True:
        choice = getMenuChoice(menu)
        executeChoice(choice)


if __name__ == '__main__':
    main()
