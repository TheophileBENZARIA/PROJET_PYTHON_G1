
import argparse

import curses
import os

def main(stdscr):
    curses.curs_set(0)            # hide cursor
    stdscr.nodelay(True)         # non-blocking getch
    stdscr.keypad(True) # enable special keys capture
    max_hauteur, max_longeur = stdscr.getmaxyx()

    # recuperation de l'argument map
    parser = argparse.ArgumentParser(description="Argument pour lancer l'affichage")
    parser.add_argument("--mapFilePath", type=str, required=True, help="Fichier de carte à charger")
    args = parser.parse_args()

    #assert os.path.exists(args.mapFilePath)  #test si le ficher existe

    grille = []

    with open(args.mapFilePath, "r") as f:
        #Recupèrer la longeur, la hauteur et l'orientation a la première ligne du fichier
        read = f.readline()
        dims = read.replace(" ", "").split(",")
        hauteur, longeur, orientation = int(dims[0]), int(dims[1]), str(dims[2])
        assert hauteur > 0 and hauteur <= max_hauteur//2-1
        assert longeur > 0 and longeur <= max_longeur//2-1

        print(orientation, orientation=="V",ord("V"))
        #assert orientation == "V" or orientation == "H"

        for i in range(hauteur):
            line = " "
            try : line = f.readline().replace(".", " ").replace("\n", " ")
            except : pass
            print(list(line))
            grille.append(list(line))
            while len(grille[i]) < longeur:
                grille[i].append(' ')
            if orientation == "V": grille[i] += grille[i][::-1]
        if orientation == "H": grille += grille[::-1]


    stdscr.addstr(0, 0, "_" * (longeur + 2))

    for i in range(hauteur):
        stdscr.addstr(i + 1, 0, "|")
        stdscr.addstr(i + 1, 1, "".join(grille[i])+"|")

    stdscr.addstr(hauteur, 0, "_" * (longeur + 2))

    while True :
        key = stdscr.getch()





        if key == -1:
            # aucune touche pressée
            pass
        else :

            stdscr.addstr(1, 0, chr(key))
        curses.napms(20)

if __name__ == "__main__":
    curses.wrapper(main)
