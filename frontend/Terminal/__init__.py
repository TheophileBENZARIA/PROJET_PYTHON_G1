# frontend/Terminal/__init__.py
"""
Terminal package to run the curses display for a Battle/map.

Main exported function:
    run_battle_with_curses(battle, delay=0.5)
"""
from typing import Callable
import curses
from .Screen import Screen
from .UniteTerm import from_unit, UniteTerm

def _map_to_grid(game_map):
    """
    Convert backend.map.Map into a grid[y][x] of UniteTerm objects.
    The Map.grid in the project is indexed as grid[x][y], so we must transpose.
    """
    if game_map is None:
        return []

    width = game_map.width
    height = game_map.height
    # create empty grid as list of rows
    rows = [[UniteTerm(".") for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            tile = game_map.grid[x][y]
            unit = getattr(tile, "unit", None)
            if unit is None:
                rows[y][x] = UniteTerm(".")
            else:
                rows[y][x] = from_unit(unit)
    return rows

def run_battle_with_curses(battle, delay: float = 0.5):
    """
    Run the given Battle while driving a curses screen.
    This will call battle.run(delay=delay, display_callback=callback) where callback(map)
    updates the curses Screen with the current map state and a compact event log.
    """
    def _curses_main(stdscr):
        screen = Screen(stdscr)
        screen.start()

        # callback called each tick with game_map
        def display_callback(game_map):
            # map grid snapshot
            grid = _map_to_grid(game_map)
            screen.actualiser_grille(grid)
            # take a snapshot of the battle's event_log (battle closure is available)
            # show only the most recent events; battle.event_log is a deque
            try:
                log_snapshot = list(battle.event_log)
            except Exception:
                log_snapshot = []
            screen.actualiser_log(log_snapshot)
            screen.afficher_grille()
            # allow user to press q to abort; check keypress without blocking
            if screen.getch():
                # user requested exit: stop the battle by raising an exception the battle.run can catch
                raise KeyboardInterrupt()

        try:
            # run the battle; Battle.run must accept display_callback parameter
            battle.run(delay=delay, display_callback=display_callback)
        except KeyboardInterrupt:
            # graceful exit requested by user
            pass
        finally:
            # final draw so user sees end state (and final log)
            grid = _map_to_grid(battle.map)
            screen.actualiser_grille(grid)
            screen.actualiser_log(list(battle.event_log))
            screen.afficher_grille()
            # wait for a key before leaving
            stdscr.nodelay(False)
            stdscr.getch()

    try:
        curses.wrapper(_curses_main)
    except Exception as e:
        # If curses cannot initialize or user aborts, print a helpful message.
        print("Curses display closed or failed:", e)