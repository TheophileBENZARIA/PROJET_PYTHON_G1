"""
Utilities to load armies and maps from lightweight ASCII files.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from backend.Class.Army import Army
from backend.Class.Map import Map

DEFAULT_CASTLE_HP = 300


@dataclass
class _Tile:
    """Simple tile representation used by the loader."""

    x: int
    y: int
    elevation: int = 0
    building: Optional[object] = None
    unit: Optional[object] = None

    def is_empty(self) -> bool:
        return self.unit is None and self.building is None


_MAP_CHAR_LEGEND: Dict[str, Dict[str, object]] = {
    ".": {},
    " ": {},
    "#": {"building": "wall"},
    "b": {"building": "building"},
    "B": {"building": "building"},
    "~": {"building": "water"},
    "h": {"elevation": 1},
    "H": {"elevation": 2},
    "1": {
        "building": {
            "type": "castle",
            "owner": "Player1",
            "hp": DEFAULT_CASTLE_HP,
            "max_hp": DEFAULT_CASTLE_HP,
        }
    },
    "2": {
        "building": {
            "type": "castle",
            "owner": "Player2",
            "hp": DEFAULT_CASTLE_HP,
            "max_hp": DEFAULT_CASTLE_HP,
        }
    },
}


def _read_ascii_file(path: Path) -> Tuple[int, int, List[str]]:
    """Parse 'width;height' header and payload lines from the given file."""
    if not path.exists():
        raise FileNotFoundError(f"Unable to find '{path}'")

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    header_line = None
    header_index = -1

    for idx, line in enumerate(raw_lines):
        if line.strip():
            header_line = line.strip()
            header_index = idx
            break

    if header_line is None:
        raise ValueError(f"File '{path}' does not contain a valid 'width;height' header")

    try:
        width_str, height_str = header_line.split(";")
        width, height = int(width_str), int(height_str)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Invalid header line '{header_line}' in '{path}'") from exc

    payload = [line.rstrip() for line in raw_lines[header_index + 1 :] if line.strip()]

    return width, height, payload


def _unit_factories():
    """Lazy import to avoid circular import issues."""
    from backend.Class.Units.Crossbowman import Crossbowman
    from backend.Class.Units.Knight import Knight
    from backend.Class.Units.Pikeman import Pikeman

    return {
        "K": Knight,
        "P": Pikeman,
        "C": Crossbowman,
    }


def _spawn_unit(char: str, army: Army, position: Tuple[float, float]):
    """Instantiate the unit mapped by `char` and add it to `army`."""
    factories = _unit_factories()
    unit_cls = factories.get(char.upper())
    if not unit_cls:
        return None

    unit = unit_cls(army, position)
    army.add_unit(unit)
    return unit


def load_mirrored_army_from_file(path: str) -> tuple[Army, Army]:
    """
    Load an army layout for Player1 and mirror it vertically for Player2.

    File format:
        WIDTH;ROWS
        layout line 1
        layout line 2
        ...

    Supported symbols: K (Knight), P (Pikeman), C (Crossbowman), '.' or space for empty tiles.
    """
    width, rows, payload = _read_ascii_file(Path(path))

    if len(payload) < rows:
        raise ValueError(
            f"Army layout in '{path}' only has {len(payload)} rows (expected {rows})"
        )

    army1 = Army()
    army2 = Army()

    for y in range(rows):
        row = payload[y]
        for x in range(width):
            char = row[x] if x < len(row) else "."
            if char.upper() not in {"K", "P", "C"}:
                continue

            pos1 = (float(x), float(y))
            spawned = _spawn_unit(char, army1, pos1)
            if spawned is None:
                continue

            mirror_y = rows - 1 - y
            mirror_pos = (float(x), float(mirror_y))
            _spawn_unit(char, army2, mirror_pos)

    return army1, army2


def load_map_from_file(path: str) -> Map:
    """
    Load a rectangular map described by ASCII characters.

    The first non-empty line must contain "width;height".
    The following `height` lines describe the terrain using symbols defined in `_MAP_CHAR_LEGEND`.
    """
    width, height, payload = _read_ascii_file(Path(path))

    if len(payload) < height:
        raise ValueError(
            f"Map layout in '{path}' only has {len(payload)} rows (expected {height})"
        )

    game_map = Map()
    game_map.width = width
    game_map.height = height
    game_map.grid = [[_Tile(x, y) for y in range(height)] for x in range(width)]
    game_map.tiles = game_map.grid  # compatibility with saved battle format
    game_map.spawn_points = {"Player1": [], "Player2": []}

    for y in range(height):
        row = payload[y]
        for x in range(width):
            tile = game_map.grid[x][y]
            char = row[x] if x < len(row) else "."
            info = _MAP_CHAR_LEGEND.get(char, {})

            tile.elevation = int(info.get("elevation", 0))
            building = info.get("building")
            if isinstance(building, dict):
                tile.building = deepcopy(building)
            else:
                tile.building = building

            spawn_owner = info.get("spawn_owner")
            if spawn_owner:
                game_map.spawn_points.setdefault(spawn_owner, []).append((x, y))

    return game_map


if __name__ == "__main__":  # pragma: no cover - manual testing helper
    load_map_from_file("../test.carte")
