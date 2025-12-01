# backend/scenarios.py
from .map import Map
from .army import Army
from .units import Knight, Crossbowman

def simple_knight_duel():
    """Creates a map with 1 Knight vs 1 Knight"""
    game_map = Map(20, 20)

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