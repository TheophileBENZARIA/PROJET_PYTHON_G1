# backend/scenarios.py
from .map import Map
from .army import Army
from .units import Knight

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
