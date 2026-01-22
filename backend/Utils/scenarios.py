# backend/scenarios.py
from backend.Class.map import Map
from backend.Class.army import Army
from backend.Class.Units import Knight, Crossbowman, Pikeman
import math
from typing import Tuple

CASTLE_HP = 300

def _add_sample_terrain(game_map: Map):
    """Add a few buildings and hills to the provided map for scenario testing."""
    w, h = game_map.width, game_map.height
    # small building cluster near center
    buildings = [
        (w // 2 - 1, h // 2),
        (w // 2,     h // 2),
        (w // 2 + 1, h // 2),
    ]
    for x, y in buildings:
        if 0 <= x < w and 0 <= y < h:
            game_map.grid[x][y].building = "building"

    # hills around map quadrants
    hills = [
        (3, 4),
        (w - 4, 4),
        (3, h - 5),
        (w - 4, h - 5),
    ]
    for i, (x, y) in enumerate(hills):
        if 0 <= x < w and 0 <= y < h:
            game_map.grid[x][y].elevation = 1 + (i % 2)

def _place_castles(game_map: Map, p1_x: int, p1_y: int, p2_x: int, p2_y: int):
    """Place castle tiles (as building dicts) at provided coordinates for both players."""
    # Player1 castle
    if 0 <= p1_x < game_map.width and 0 <= p1_y < game_map.height:
        game_map.grid[p1_x][p1_y].building = {"type": "castle", "owner": "Player1", "hp": CASTLE_HP, "max_hp": CASTLE_HP}
    # Player2 castle
    if 0 <= p2_x < game_map.width and 0 <= p2_y < game_map.height:
        game_map.grid[p2_x][p2_y].building = {"type": "castle", "owner": "Player2", "hp": CASTLE_HP, "max_hp": CASTLE_HP}

def simple_knight_duel():
    """Creates a map with 1 Knight vs 1 Knight"""
    game_map = Map(20, 20)

    # add terrain for testing
    _add_sample_terrain(game_map)

    army1 = Army("Player1")
    army2 = Army("Player2")

    k1 = Knight("Player1")
    k2 = Knight("Player2")

    game_map.place_unit(k1, 5, 5)
    game_map.place_unit(k2, 5, 15)

    army1.add_unit(k1)
    army2.add_unit(k2)

    # place castles behind troops
    _place_castles(game_map, 5, 1, 5, 18)

    return game_map, army1, army2


def mirrored_knight_crossbow_duel():
    """
    Creates a mirrored scenario:
      - Player1: 1 Knight + 1 Crossbowman
      - Player2: 1 Knight + 1 Crossbowman
    Units are placed symmetrically so both sides have identical starting setups.
    Useful to test crossbow shooting vs melee behavior.
    """
    game_map = Map(20, 20)

    # add terrain for testing
    _add_sample_terrain(game_map)

    army1 = Army("Player1")
    army2 = Army("Player2")

    # Player1 units (upper area)
    k1 = Knight("Player1")
    c1 = Crossbowman("Player1")

    # Player2 units (mirrored in lower area)
    k2 = Knight("Player2")
    c2 = Crossbowman("Player2")

    # Place Player1 units
    game_map.place_unit(k1, 5, 5)   # Knight slightly left
    game_map.place_unit(c1, 6, 5)   # Crossbowman next to the knight

    # Place Player2 units mirrored on the Y axis (same X, mirrored Y)
    game_map.place_unit(k2, 5, 15)  # Knight mirrored vertically
    game_map.place_unit(c2, 6, 15)  # Crossbowman mirrored vertically

    # Register units with armies
    army1.add_unit(k1)
    army1.add_unit(c1)

    army2.add_unit(k2)
    army2.add_unit(c2)

    # place castles behind sides
    _place_castles(game_map, game_map.width // 2, 1, game_map.width // 2, game_map.height - 2)

    return game_map, army1, army2


def mirrored_triplet_pikeman_knight_crossbow_duel():
    """
    Creates a mirrored scenario with three units per side:
      - Player1: Pikeman, Knight, Crossbowman
      - Player2: Pikeman, Knight, Crossbowman
    Units are positioned symmetrically so both sides have identical starting setups.
    Use this to test interactions between melee, spears, and ranged units.
    """
    game_map = Map(20, 20)

    # add terrain for testing
    _add_sample_terrain(game_map)

    army1 = Army("Player1")
    army2 = Army("Player2")

    # Player1 units (upper area)
    p1 = Pikeman("Player1")
    k1 = Knight("Player1")
    c1 = Crossbowman("Player1")

    # Player2 units (mirrored in lower area)
    p2 = Pikeman("Player2")
    k2 = Knight("Player2")
    c2 = Crossbowman("Player2")

    # Place Player1 units (clustered but not overlapping)
    # x positions: 4,5,6 ; y = 5
    game_map.place_unit(p1, 4, 5)   # Pikeman left
    game_map.place_unit(k1, 5, 5)   # Knight center
    game_map.place_unit(c1, 6, 5)   # Crossbowman right

    # Place Player2 units mirrored on the Y axis (same X, mirrored Y)
    # choose y = 14 (mirror of 5 in 20-high map => 19 - 5 = 14) or simply 15 to match previous scenarios
    game_map.place_unit(p2, 4, 15)  # Pikeman left
    game_map.place_unit(k2, 5, 15)  # Knight center
    game_map.place_unit(c2, 6, 15)  # Crossbowman mirrored vertically

    # Register units with armies
    army1.add_unit(p1)
    army1.add_unit(k1)
    army1.add_unit(c1)

    army2.add_unit(p2)
    army2.add_unit(k2)
    army2.add_unit(c2)

    # place castles behind sides
    _place_castles(game_map, game_map.width // 2, 1, game_map.width // 2, game_map.height - 2)

    return game_map, army1, army2


# ----------------------------
# Lanchester scenario generator
# ----------------------------
def lanchester(unit_type: str, N: int, width: int = 40, height: int = 20) -> Tuple[Map, Army, Army]:
    """
    Build a Lanchester-style scenario for testing Lanchester's Laws.

    Parameters:
      unit_type: 'melee' or 'archer' (case-insensitive). 'melee' uses Knight,
                 'archer' uses Crossbowman.
      N: base number of units on the weaker side. The opposing side will have 2*N.
      width, height: map size.

    Returns (game_map, army1, army2) where:
      - army1 (Player1) has N units
      - army2 (Player2) has 2*N units
    Units are placed facing each other with spacing chosen so both sides can engage immediately
    according to the rules for melee/ranged (melee placed adjacent rows, archers within range).
    """
    if unit_type.lower() not in ("melee", "archer"):
        raise ValueError("unit_type must be 'melee' or 'archer'")

    game_map = Map(width, height)
    _add_sample_terrain(game_map)

    army1 = Army("Player1")
    army2 = Army("Player2")

    # choose class
    if unit_type.lower() == "melee":
        UnitCls = Knight
        # melee need adjacent rows to immediately fight -> small vertical gap
        p1_row = height // 2 - 1
        p2_row = height // 2
    else:
        UnitCls = Crossbowman
        # archers should be within shooting range of each other; Crossbowman.range is typically 5
        # place them a few tiles apart but within range so they shoot from the start
        p1_row = height // 2 - 3
        p2_row = height // 2 + 3

    # determine columns per side (fit N units centered)
    def place_row_count(count, row_y, owner, army):
        if count <= 0:
            return
        cols = min(count, max(1, width - 4))
        # we will create as many rows as needed
        rows_needed = math.ceil(count / cols)
        placed = 0
        for r in range(rows_needed):
            y = row_y + r  # for Player1 rows go downward; for Player2 caller may pass appropriate start
            if y < 0 or y >= height:
                # try shift up/down within bounds
                y = max(0, min(height - 1, y))
            to_place = min(cols, count - placed)
            start_x = max(2, (width - to_place) // 2)
            for i in range(to_place):
                x = start_x + i
                # ensure tile not occupied (terrain may be present); scan nearby if needed
                if not (0 <= x < width and 0 <= y < height):
                    continue
                tile = game_map.grid[x][y]
                if tile.is_empty():
                    u = UnitCls(owner)
                    game_map.place_unit(u, x, y)
                    army.add_unit(u)
                    placed += 1
                else:
                    # scan row for nearest empty
                    found = False
                    for d in range(1, width):
                        for candidate in (x + d, x - d):
                            if 0 <= candidate < width and game_map.grid[candidate][y].is_empty():
                                u = UnitCls(owner)
                                game_map.place_unit(u, candidate, y)
                                army.add_unit(u)
                                placed += 1
                                found = True
                                break
                        if found:
                            break
            if placed >= count:
                break

    # Player1 (weaker) N units
    place_row_count(N, p1_row, "Player1", army1)

    # Player2 (stronger) 2*N units - place mirrored vertically around center to face Player1
    place_row_count(2 * N, p2_row, "Player2", army2)

    # place castles behind each army: behind Player1 -> nearer top; behind Player2 -> bottom
    _place_castles(game_map, width // 2, max(0, p1_row - 2), width // 2, min(height - 1, p2_row + 2))

    return game_map, army1, army2