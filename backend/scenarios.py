# backend/scenarios.py
from .map import Map
from .army import Army
from .units import Knight, Crossbowman, Pikeman

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

    return game_map, army1, army2