import curses

import Screen


def start(stdsrc) :
    screen = Screen.Screen(stdsrc)
    screen.start()

    while True :
        screen.afficher_grille([[0,0,0],[1,1,1]])
        screen.getch()


if __name__ == '__main__':
    curses.wrapper(start)