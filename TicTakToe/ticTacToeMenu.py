import tkinter as tk
import tkinter.messagebox as mb
import logic


top = tk.Tk()


def buildMenu(parent):
    menus = (
        ("File", (
            ("New", evNew),
            ("Resume", evResume),
            ("Save", evSave),
            ("Exit", evExit)
        )
        ),
        ("Help", (
            ("Help", evHelp),
            ("About", evAbout)
        )
        )
    )

    menubar = tk.Menu(parent)
    for menu in menus:
        m = tk.Menu(parent)
        for item in menu[1]:
            m.add_command(label=item[0], command=item[1])
        menubar.add_cascade(label=menu[0], menu=m)

    return menubar


def evNew():
    status["text"] = "Playing the game"
    game2cells(logic.newGame())


def evSave():
    status["text"] = "Saving game..."
    game = cells2Game()
    logic.saveGame(game)


def evResume():
    status["text"] = "Playing the game"
    game = logic.restoreGame()
    game2cells(game)


def evExit():
    if status["text"] == "Playing the game":
        if mb.askyesno("Quitting?", "Do you want to save before you quit?"):
            evSave()
    top.quit()


def evHelp():
    mb.showinfo("You want some help?",
                '''
                File -> New - starts a new game
                File -> Resume - resumes last saved game
                File -> Save - saves current game progress
                File -> Exit - quits the game
                Help -> help - shows this page
                Help - > About - shows info about the program
                '''
                )


def evAbout():
    mb.showinfo("About", "Tic tac toe game")


def evClick(row, col):
    if status["text"] == "Game over":
        mb.showerror("Game over", "Game over!")
        return
    game = cells2Game()
    index = (3*row) + col
    result = logic.userMove(game, index)
    game2cells(game)

    if not result:
        result = logic.botMove(game)
        game2cells(game)
    if result == "D":
        mb.showinfo("Result", "It's a draw!")
        status["text"] = "Game over"
    else:
        if result == "X" or result == "O":
            mb.showinfo("We have a winner!",
                        "The winner is: {}".format(result))
            status["text"] = "Game over"


def game2cells(game):
    table = board.pack_slaves()[0]
    for row in range(3):
        for col in range(3):
            table.grid_slaves(row=row, column=col)[0]["text"] = game[3*row+col]


def cells2Game():
    values = []
    table = board.pack_slaves()[0]
    for row in range(3):
        for col in range(3):
            values.append(table.grid_slaves(row=row, column=col)[0]["text"])
    return values


def buildBoard(parent):
    outer = tk.Frame(parent, border=2, relief="sunken")
    inner = tk.Frame(outer)
    inner.pack()

    for row in range(3):
        for col in range(3):
            cell = tk.Button(inner, text=" ", width=5, heigh=2,
                             command=lambda r=row, c=col: evClick(r, c)
                             )
            cell.grid(row=row, column=col)
    return outer


mbar = buildMenu(top)
top["menu"] = mbar

board = buildBoard(top)
board.pack()
status = tk.Label(
    top, text="Playing game", border=0,
    background="lightgrey", foreground="red"
)
status.pack(anchor="s", fill="x", expand=True)

tk.mainloop()
