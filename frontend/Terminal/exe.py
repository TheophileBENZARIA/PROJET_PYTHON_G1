import curses

import Screen


def start(stdsrc) :
    screen = Screen.Screen(stdsrc)
    screen.start()
    grille = []
    for i in range(50):
        grille.append([0,0,0])
    for i in range(50):
        grille.append([1,1,1])

    while True:
        screen.afficher_grille(grille)
        screen.getch()


if __name__ == '__main__':
    curses.wrapper(start)
    print("start")