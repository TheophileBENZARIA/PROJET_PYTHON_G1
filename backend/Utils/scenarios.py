"""
Scenario builders used by the CLI.

This module intentionally keeps scenarios programmable (see project brief) so that
we can script formations without relying on a visual editor.  Each helper returns
``(game_map, army1, army2)`` and the caller can plug the result straight into the
game loop.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Tuple

from backend.Class.Army import Army
from backend.Class.Map import Map
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman


# --------------------------------------------------------------------------- #
# Tiles / map construction helpers
# --------------------------------------------------------------------------- #


@dataclass
class _Tile:
    x: int
    y: int
    elevation: int = 0
    building: object | None = None
    unit: object | None = None

    def is_empty(self) -> bool:
        return self.unit is None and self.building is None


def _empty_map(width: int, height: int) -> Map:
    """Create a minimal Map instance with a rectangular grid."""
    game_map = Map()
    game_map.width = width
    game_map.height = height
    game_map.grid = [[_Tile(x, y) for y in range(height)] for x in range(width)]
    game_map.spawn_points = {"Player1": [], "Player2": []}
    # ``Map`` currently only exposes obstacles; keep the attribute consistent.
    if not hasattr(game_map, "obstacles"):
        game_map.obstacles = set()
    return game_map


def _spawn(unit_cls, army: Army, x: int, y: int):
    """Instantiate ``unit_cls`` on (x, y) and register it in ``army``."""
    unit = unit_cls(army, (float(x), float(y)))
    army.add_unit(unit)
    return unit


def _spread_positions(width: int, count: int, margin: int = 2) -> Iterable[int]:
    """Evenly spread ``count`` columns across ``width``."""
    usable = max(1, width - margin * 2)
    if count <= 1:
        offset = width // 2
        yield offset
        return
    step = max(1, usable // (count - 1))
    start = margin
    for i in range(count):
        yield min(width - 1 - margin, start + i * step)


# --------------------------------------------------------------------------- #
# Scenario implementations
# --------------------------------------------------------------------------- #


def mirrored_knight_duel(width: int = 120, height: int = 120) -> Tuple[Map, Army, Army]:
    """
    Small scenario with a single Knight per side facing each other.
    Useful smoketest for melee behaviour.
    """
    game_map = _empty_map(width, height)
    army1 = Army()
    army2 = Army()

    y1 = height // 4
    y2 = height - y1 - 1
    x = width // 2
    _spawn(Knight, army1, x, y1)
    _spawn(Knight, army2, x, y2)
    return game_map, army1, army2


def mirrored_triplet(width: int = 120, height: int = 120) -> Tuple[Map, Army, Army]:
    """
    Three units per side: Pikeman, Knight, Crossbowman.
    Layout mirrors across the horizontal axis.
    """
    game_map = _empty_map(width, height)
    army1 = Army()
    army2 = Army()

    y_top = height // 4
    y_bottom = height - y_top - 1
    start_x = width // 2 - 1
    slots = [start_x - 1, start_x, start_x + 1]
    classes = (Pikeman, Knight, Crossbowman)

    for cls, col in zip(classes, slots):
        _spawn(cls, army1, col, y_top)
        _spawn(cls, army2, col, y_bottom)

    return game_map, army1, army2


def lanchester(unit_type: str, n: int, width: int = 32, height: int = 16) -> Tuple[Map, Army, Army]:
    """
    Build a scenario for testing Lanchester's laws.

    ``unit_type``: "melee" (Knights) or "archer" (Crossbowmen).
    ``n``: number of units on the weaker side. The stronger side will receive ``2*n``.

    Units are positioned in two opposing ranks so that they are within engagement
    range from the very first tick.
    """
    if n <= 0:
        raise ValueError("N must be positive")

    unit_type = unit_type.lower()
    if unit_type not in {"melee", "archer"}:
        raise ValueError("unit_type must be 'melee' or 'archer'")

    UnitCls = Knight if unit_type == "melee" else Crossbowman
    game_map = _empty_map(width, height)
    army1 = Army()
    army2 = Army()

    row1 = height // 2 - 2
    row2 = height // 2 + 2
    for x in _spread_positions(width, n):
        _spawn(UnitCls, army1, x, row1)
    for x in _spread_positions(width, 2 * n):
        _spawn(UnitCls, army2, x, row2)

    return game_map, army1, army2


# Registry handy for CLI / tests.
SCENARIO_REGISTRY: Dict[str, Callable[[], Tuple[Map, Army, Army]]] = {
    "knight_duel": mirrored_knight_duel,
    "triplet": mirrored_triplet,
}
