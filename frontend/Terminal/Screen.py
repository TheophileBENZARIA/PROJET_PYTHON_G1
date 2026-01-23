# frontend/Terminal/Screen.py
import curses
import sys
from time import sleep
from typing import List, Optional

from frontend.Affichage import Affichage


# The screen expects:
#  - a 2D grid (list of rows) where each cell is an object with __str__ returning a printable char (UniteTerm)
#  - and an optional list of recent event strings to render in a compact log
class Screen(Affichage):
    def __init__(self, stdsrc: curses.window):
        self.std = stdsrc
        self.x = 0  # viewport x offset
        self.y = 0  # viewport y offset

        # grid holds the last grid snapshot (list[list[...]])
        self.grille = []  # grid[y][x]

        # compact event log (list of strings). newest last.
        self.log_lines: List[str] = []

    def start(self):
        curses.curs_set(0)
        # non-blocking getch
        self.std.nodelay(True)
        self.std.keypad(True)
        # use color pair if terminal supports color
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def getch(self):
        """Handle a keypress. Returns True if the caller should exit."""
        key = self.std.getch()
        if key == curses.ERR:
            return False

        # Navigation: keep viewport in bounds when possible
        # UP
        if key == curses.KEY_UP or key == ord('k'):
            if self.y > 0:
                self.y -= 1
        # DOWN
        elif key == curses.KEY_DOWN or key == ord('j'):
            # allow always increment; caller will clamp if grid smaller
            self.y += 1
        # LEFT
        elif key == curses.KEY_LEFT or key == ord('h'):
            if self.x > 0:
                self.x -= 1
        # RIGHT
        elif key == curses.KEY_RIGHT or key == ord('l'):
            self.x += 1
        elif key == ord('q') or key == ord('Q'):
            # signal exit to caller
            return True

        return False

    def actualiser_grille(self, grille: List[List[object]]):
        """Replace the internal grid snapshot (grid indexed as [y][x])."""
        self.grille = grille

        # Clamp viewport to grid size
        if not self.grille:
            self.x = 0
            self.y = 0
            return
        height = len(self.grille)
        width = len(self.grille[0]) if height > 0 else 0
        if self.y < 0:
            self.y = 0
        if self.x < 0:
            self.x = 0

    def actualiser_log(self, lines: Optional[List[str]]):
        """Set the list of event strings (most recent last). We keep only the last N to fit screen."""
        if not lines:
            self.log_lines = []
            return
        # keep last 5 events (this is intentionally compact)
        self.log_lines = list(lines)[-5:]

    def afficher_grille(self):
        """Draw the current grid snapshot to the curses window using a viewport that fits the terminal.
           A compact event log (few lines) is displayed at the bottom without taking too much space.
        """
        self.std.erase()
        maxy, maxx = self.std.getmaxyx()

        # reserve lines:
        help_height = 1  # single-line help at very bottom
        log_height = min(5, max(0, maxy // 6))  # prefer up to 5 lines for log, adapt to small terminals
        grid_area_height = maxy - help_height - log_height - 2  # top border + bottom border

        usable_h = max(1, grid_area_height)
        usable_w = max(2, maxx - 2)

        if usable_h <= 0 or usable_w <= 0:
            try:
                self.std.addstr(0, 0, "Terminal too small")
                self.std.refresh()
            except curses.error:
                pass
            return

        # grid may be empty
        if not self.grille:
            try:
                self.std.addstr(1, 1, "." * min(usable_w, 1))
            except curses.error:
                pass
            try:
                self.std.addstr(maxy - 2, 0, "Q pour quitter")
            except curses.error:
                pass
            self.std.refresh()
            return

        grid_h = len(self.grille)
        grid_w = len(self.grille[0])

        # clamp offsets so viewport is valid
        if self.y > max(0, grid_h - usable_h):
            self.y = max(0, grid_h - usable_h)
        if self.x > max(0, grid_w - usable_w):
            self.x = max(0, grid_w - usable_w)

        min_y = self.y
        max_y = min(grid_h, self.y + usable_h)
        min_x = self.x
        max_x = min(grid_w, self.x + usable_w)

        # draw top border
        top_row = "_" * (max_x - min_x)
        try:
            self.std.addstr(0, 1, top_row[:usable_w])
        except curses.error:
            pass

        # draw grid contents
        for row_idx, y in enumerate(range(min_y, max_y), start=1):
            line = ""
            for x in range(min_x, max_x):
                cell = self.grille[y][x]
                ch = str(cell)
                if not ch:
                    ch = "."
                ch = ch[0]
                line += ch
            try:
                self.std.addstr(row_idx, 1, line[:usable_w])
            except curses.error:
                pass

        # bottom border for the grid area
        bottom_row = "‾" * (max_x - min_x)
        try:
            self.std.addstr(1 + (max_y - min_y), 1, bottom_row[:usable_w])
        except curses.error:
            pass

        # draw compact log lines below the grid area
        log_start_row = 2 + (max_y - min_y)
        for i, logline in enumerate(self.log_lines[-log_height:]):
            row = log_start_row + i
            # keep log lines concise: truncate to available width
            text = str(logline)[:usable_w]
            try:
                # use a dim attribute if available
                if curses.has_colors():
                    self.std.addstr(row, 1, text.ljust(usable_w)[:usable_w])
                else:
                    self.std.addstr(row, 1, text.ljust(usable_w)[:usable_w], curses.A_DIM)
            except curses.error:
                pass

        # UI help line
        try:
            self.std.addstr(maxy - 1, 0, " Q to quit    use arrows or hjkl to navigate ")
        except curses.error:
            pass

        self.std.refresh()