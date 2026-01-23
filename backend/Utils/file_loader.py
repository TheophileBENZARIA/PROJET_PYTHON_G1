"""
ASCII loaders for armies and maps.

Two ultra-simple formats are supported:

Army files:
    WIDTH;HEIGHT
    rows of characters (K, P, C, or .)
The army is mirrored vertically (Player1 uses the original layout and Player2
uses the vertical mirror).

Map files:
    WIDTH;HEIGHT
    rows of characters (., #, h, H, b, 1, 2, etc.)
See ``_MAP_CHARS`` for the legend.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from backend.Class.Army import Army
from backend.Class.Map import Map
from backend.Class.Obstacles.Obstacle import Obstacle
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman


@dataclass
class _Tile:
    x: int
    y: int
    elevation: int = 0
    unit: object | None = None

    def is_empty(self) -> bool:
        return self.unit is None and self.building is None


def _read_ascii_payload(path: Path) -> Tuple[int, int, List[str]]:
    raw = path.read_text(encoding="utf-8").splitlines()
    header = next((line.strip() for line in raw if line.strip()), None)
    if not header:
        raise ValueError(f"{path} does not contain a header")
    try:
        width_str, height_str = header.split(";")
        width, height = int(width_str), int(height_str)
    except Exception as exc:
        raise ValueError(f"Invalid header '{header}' in {path}") from exc
    payload = [line.rstrip() for line in raw[1:] if line.strip()]
    return width, height, payload


# --------------------------------------------------------------------------- #
# Army loader
# --------------------------------------------------------------------------- #

_UNIT_SYMBOLS = {
    "K": Knight,
    "P": Pikeman,
    "C": Crossbowman,
}


def load_mirrored_army_from_file(path: str) -> tuple[Army, Army]:
    path_obj = Path(path)
    width, height, payload = _read_ascii_payload(path_obj)

    army1 = Army()
    army2 = Army()

    for y in range(height):
        row = payload[y] if y < len(payload) else ""
        for x in range(width):
            char = row[x] if x < len(row) else "."
            unit_cls = _UNIT_SYMBOLS.get(char.upper())
            if unit_cls is None:
                continue

            unit1 = unit_cls(army1, (float(x), float(y)))
            army1.add_unit(unit1)

            mirror_y = height - 1 - y
            unit2 = unit_cls(army2, (float(x), float(mirror_y)))
            army2.add_unit(unit2)

    return army1, army2


# --------------------------------------------------------------------------- #
# Map loader
# --------------------------------------------------------------------------- #

_MAP_CHARS: Dict[str, Dict[str, object]] = {
    ".": {},
    " ": {},
    "#": {"obstacle": {"size": 0.9}},
    "b": {"obstacle": {"size": 0.7}},
    "B": {"obstacle": {"size": 1.2}},
    "h": {"elevation": 1},
    "H": {"elevation": 2},
}


def load_map_from_file(path: str) -> Map:
    path_obj = Path(path)
    width, height, payload = _read_ascii_payload(path_obj)

    game_map = Map()
    game_map.width = width
    game_map.height = height
    game_map.grid = [[_Tile(x, y) for y in range(height)] for x in range(width)]
    if not hasattr(game_map, "obstacles"):
        game_map.obstacles = set()

    for y in range(height):
        row = payload[y] if y < len(payload) else ""
        for x in range(width):
            char = row[x] if x < len(row) else "."
            info = _MAP_CHARS.get(char, {})
            tile = game_map.grid[x][y]
            tile.elevation = int(info.get("elevation", 0))
            obstacle_info = info.get("obstacle")
            if obstacle_info:
                obs = Obstacle((float(x), float(y)), float(obstacle_info.get("size", 1.0)))
                obs.map = game_map
                game_map.obstacles.add(obs)

    return game_map
