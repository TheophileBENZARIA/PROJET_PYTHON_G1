import argparse
import curses

"""
In : [f: file] <- fichier ouvert en lecture
Out : [grille: list] <- tableau 2D
A partir du fichier map elle genère la grille d'affichage et en duplicant en mirroir les troupes
"""
def genererGrille(f) -> list:
    grille = []
    # Recupèrer la longeur, la hauteur et l'orientation a la première ligne du fichier
    read = f.readline()
    dims = read.replace(" ", "").replace("\n", "").split(",")
    hauteur, longeur, orientation = int(dims[0]), int(dims[1]), dims[2]
    assert hauteur > 0
    assert longeur > 0
    assert orientation == "G" or orientation == "D" or orientation == "H" or orientation == "B"

    for i in range(hauteur):
        line = " "
        try: line = f.readline().replace(".", " ").replace("\n", " ")
        except: pass

        grille.append(list(line))
        while len(grille[i]) > longeur:
            del grille[i][-1]
        while len(grille[i]) < longeur:
            grille[i].append(' ')

        if orientation == "D": grille[i] = grille[i] + grille[i][::-1]
        if orientation == "G": grille[i] = grille[i][::-1] + grille[i]

    if orientation == "B": grille = grille + grille[::-1]
    if orientation == "H": grille = grille[::-1] + grille
    return grille






def main(stdscr):
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)  # non-blocking getch
    stdscr.keypad(True)  # enable special keys capture
    max_hauteur, max_longeur = stdscr.getmaxyx()

    # recuperation de l'argument map
    parser = argparse.ArgumentParser(description="Argument pour lancer l'affichage")
    parser.add_argument("--save", type=str, required=True, help="Fichier de sauvegarde à charger")
    parser.add_argument("--map", type=str, required=True, help="Fichier de carte à charger lié à la sauvegarde")
    args = parser.parse_args()

    # ! Tester si la map est bien la meme que celle noter dans la save

    grille = [[]]

    with open(args.map, "r") as f:
        grille = genererGrille(f)


    stdscr.addstr(0, 0, "_" * (len(grille[0]) + 2))

    for i in range(len(grille)):
        stdscr.addstr(i + 1, 0, "|")
        stdscr.addstr(i + 1, 1, "".join(grille[i]) + "|")

    stdscr.addstr(len(grille)+1, 0, "‾" * (len(grille[0]) + 2))




    #-------------------------------------------------------------------------------------
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break

        # Si c’est un événement souris
        try:
            _, x, y, _, bstate = curses.getmouse()

            # Efface la ligne du bas
            stdscr.move(curses.LINES - 1, 0)
            stdscr.clrtoeol()

            # Affiche les infos de la souris
            stdscr.addstr(
                curses.LINES - 1, 0,
                f"Souris à (x={x}, y={y}) | Boutons: {bstate}"
            )
            stdscr.refresh()
        except curses.error:
            # Erreur possible si les coords sont hors écran
            pass

    if key == -1:
        # aucune touche pressée
        pass
    else:

        stdscr.addstr(1, 0, chr(key))
    curses.napms(20)
    #-------------------------------------------------------------------------------------


if __name__ == "__main__":
    curses.wrapper(main)
