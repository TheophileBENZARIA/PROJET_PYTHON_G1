import curses
from .Screen import Screen
from .UniteTerm import UniteTerm, from_tile

UNIT_TYPES = ["knight", "pikeman", "crossbowman"]
UNIT_LETTERS = {
    "knight": "K",
    "pikeman": "P",
    "crossbowman": "C"
}

def curses_placement_editor(game_map):
    """
    Ouvre un éditeur curses qui permet :
    - de déplacer un curseur avec flèches / hjkl
    - de choisir le type d’unité (1/2/3)
    - de placer (espace)
    - de supprimer (backspace)
    - de valider (entrée)
    Renvoie un dict:
        { "knight":[(x,y),...], "pikeman":[], "crossbowman":[] }
    """

    height = game_map.height
    width = game_map.width

    positions = {t: [] for t in UNIT_TYPES}

    def main(stdscr):
        screen = Screen(stdscr)
        screen.start()
        cx, cy = 0, 0  # curseur
        selected = 0  # index de UNITS_TYPES

        while True:
            # Construire la grille affichée
            grid = []
            for y in range(height):
                row = []
                for x in range(width):
                    tile = game_map.grid[x][y]
                    cell = from_tile(tile)

                    # si une unité Player1 est placée ici
                    placed_letter = None
                    for t in UNIT_TYPES:
                        if (x, y) in positions[t]:
                            placed_letter = UNIT_LETTERS[t]

                    if placed_letter:
                        row.append(UniteTerm(placed_letter, team=1))
                    else:
                        row.append(cell)
                grid.append(row)

            # afficher le curseur
            grid[cy][cx].lettre = "@"

            # envoyer à l’écran
            screen.actualiser_grille(grid)
            screen.actualiser_log([f"Selected: {UNIT_TYPES[selected]}"])
            screen.afficher_grille()

            # input
            key = screen.std.getch()

            # Quitter
            if key == ord('q'):
                raise KeyboardInterrupt()

            # Déplacements curseur
            if key in (curses.KEY_UP, ord('k')) and cy > 0:
                cy -= 1
            elif key in (curses.KEY_DOWN, ord('j')) and cy < height - 1:
                cy += 1
            elif key in (curses.KEY_LEFT, ord('h')) and cx > 0:
                cx -= 1
            elif key in (curses.KEY_RIGHT, ord('l')) and cx < width - 1:
                cx += 1

            # Choisir type d’unité
            elif key == ord('1'):
                selected = 0
            elif key == ord('2'):
                selected = 1
            elif key == ord('3'):
                selected = 2

            # Placer une unité
            elif key == ord(' '):
                unit = UNIT_TYPES[selected]
                if (cx, cy) not in positions[unit]:
                    positions[unit].append((cx, cy))

            # Supprimer
            elif key in (127, curses.KEY_BACKSPACE):
                for t in UNIT_TYPES:
                    if (cx, cy) in positions[t]:
                        positions[t].remove((cx, cy))

            # Valider
            elif key == ord("\n"):
                return positions

    try:
        return curses.wrapper(main)
    except KeyboardInterrupt:
        return {t: [] for t in UNIT_TYPES}