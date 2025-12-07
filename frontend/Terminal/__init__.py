# frontend/Terminal/__init__.py
from typing import Callable
import curses
from .Screen import Screen
from .UniteTerm import from_unit, UniteTerm, from_tile

def _map_to_grid(game_map):
    """
    Convert backend.map.Map into a grid[y][x] of UniteTerm objects.
    Uses UniteTerm.from_tile(tile) so terrain (buildings/hills) and units are handled consistently.
    """
    if game_map is None:
        return []

    width = game_map.width
    height = game_map.height
    rows = [[UniteTerm(UniteTerm.EMPTY_CHAR) for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            tile = game_map.grid[x][y]
            rows[y][x] = from_tile(tile)
    return rows

def run_battle_with_curses(battle, delay: float = 0.5):
    def _curses_main(stdscr):
        screen = Screen(stdscr)
        screen.start()

        def display_callback(game_map):
            grid = _map_to_grid(game_map)
            screen.actualiser_grille(grid)
            try:
                log_snapshot = list(battle.event_log)
            except Exception:
                log_snapshot = []
            screen.actualiser_log(log_snapshot)
            screen.afficher_grille()
            if screen.getch():
                raise KeyboardInterrupt()

        try:
            battle.run(delay=delay, display_callback=display_callback)
        except KeyboardInterrupt:
            pass
        finally:
            grid = _map_to_grid(battle.map)
            screen.actualiser_grille(grid)
            screen.actualiser_log(list(battle.event_log))
            screen.afficher_grille()
            stdscr.nodelay(False)
            stdscr.getch()

    try:
        curses.wrapper(_curses_main)
    except Exception as e:
        print("Curses display closed or failed:", e)