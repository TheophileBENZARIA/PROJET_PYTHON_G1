# backend/map_loader.py
"""
Simple ASCII map loader.

Map file format (example):
####################
#A..............B..#
#..h..H....b.......#
#..................#
####################

Legend (example):
  . = empty plain tile
  # = impassable (treated as building/wall)
  h = hill (elevation +1)
  H = high hill (elevation +2)
  b = building (provides cover)
  A = spawn Player1 unit (placed as Knight by default)
  B = spawn Player2 unit

This loader returns a Map instance and optionally lists of spawned units.
"""
from .map import Map, Tile
from .units import Knight
from .army import Army

CHAR_LEGEND = {
    ".": {"elevation": 0, "building": None},
    "#": {"elevation": 0, "building": "wall"},
    "h": {"elevation": 1, "building": None},
    "H": {"elevation": 2, "building": None},
    "b": {"elevation": 0, "building": "building"},
    "A": {"elevation": 0, "spawn": ("Player1", "Knight")},
    "B": {"elevation": 0, "spawn": ("Player2", "Knight")},
}

def load_map_from_text(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines() if line.strip() != ""]

    height = len(lines)
    width = max(len(line) for line in lines)
    game_map = Map(width, height)

    army1 = Army("Player1")
    army2 = Army("Player2")

    for y, line in enumerate(lines):
        for x, ch in enumerate(line.ljust(width, ".")):
            info = CHAR_LEGEND.get(ch, CHAR_LEGEND["."])
            tile = game_map.grid[x][y]
            tile.elevation = info.get("elevation", 0)
            tile.building = info.get("building", None)
            spawn = info.get("spawn")
            if spawn:
                owner, unit_type = spawn
                # spawn a Knight by default; extend for more unit types later
                unit = Knight(owner)
                game_map.place_unit(unit, x, y)
                if owner == "Player1":
                    army1.add_unit(unit)
                else:
                    army2.add_unit(unit)

    return game_map, army1, army2