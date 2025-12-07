# backend/generals.py
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from backend.pathfinding import find_path

class General(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def issue_orders(self, army, enemy_army, game_map):
        pass

    def to_dict(self):
        # save class name so we can reconstruct
        return {"class": type(self).__name__}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Restore a General from a dict produced by `to_dict`.
        Expects a dict with a `"class"` key containing the class name saved by `to_dict`.
        Falls back to returning a default general if the name is unknown.
        """
        if not isinstance(data, dict):
            raise TypeError("General.from_dict expects a dict")
        name = data.get("class") or data.get("name")
        # use the module-level registry/resolver to construct the correct subclass instance
        return general_from_name(name)


class CaptainBraindead(General):
    def __init__(self):
        super().__init__("Captain Braindead")

    def issue_orders(self, army, enemy_army, game_map):
        pass


class MajorDaft(General):
    def __init__(self):
        super().__init__("Major Daft")

    def issue_orders(self, army, enemy_army, game_map):
        for unit in army.living_units():
            enemies = enemy_army.living_units()
            if enemies:
                target = min(enemies, key=lambda e: self.distance(unit, e))
                self.move_toward(unit, target, game_map)

    def _neighbour_steps_toward(self, ux: int, uy: int, tx: int, ty: int):
        """
        Return candidate neighbor steps (nx,ny) that tend to move from (ux,uy) closer to (tx,ty).
        Kept for fallback use.
        """
        dx = 1 if tx > ux else (-1 if tx < ux else 0)
        dy = 1 if ty > uy else (-1 if ty < uy else 0)

        candidates = []
        # primary direct step
        if dx != 0 or dy != 0:
            candidates.append((ux + dx, uy + dy))
        # prefer horizontal then vertical
        if dx != 0:
            candidates.append((ux + dx, uy))
        if dy != 0:
            candidates.append((ux, uy + dy))
        # small lateral/diagonal adjustments to go around obstacles
        if dx != 0 and dy != 0:
            candidates.append((ux + dx, uy - dy))
            candidates.append((ux - dx, uy + dy))
        # fallback neighbors
        candidates.append((ux + 1, uy))
        candidates.append((ux - 1, uy))
        candidates.append((ux, uy + 1))
        candidates.append((ux, uy - 1))
        return candidates

    def move_toward(self, unit, target, game_map):
        """
        Move `unit` toward `target` using A* pathfinding to avoid buildings and occupied tiles.
        Ranged units preserve earlier behavior (hold/step away) but when they need to
        close the distance they will follow the computed path.
        """
        if unit.position is None or target.position is None:
            return

        ux, uy = unit.position
        tx, ty = target.position

        # If unit is ranged (range > 1) prefer to keep distance so the unit can shoot.
        # We only step away when strictly closer than desired (dist < unit.range).
        if getattr(unit, "range", 1) > 1:
            dist = self.distance(unit, target)

            # If the unit is strictly too close, step away one tile (preserve previous logic).
            if dist < unit.range:
                dx = 1 if ux > tx else (-1 if ux < tx else 0)
                dy = 1 if uy > ty else (-1 if uy < ty else 0)
                new_x = ux + dx
                new_y = uy + dy
                # bounds and occupancy/building checks
                if 0 <= new_x < game_map.width and 0 <= new_y < game_map.height:
                    tile = game_map.grid[new_x][new_y]
                    if tile.is_empty():
                        game_map.move_unit(unit, new_x, new_y)
                return  # after stepping away, don't move closer

            # If distance equals range, hold position so the unit can shoot consistently.
            if dist == unit.range:
                return  # hold position (don't move closer or farther)

            # otherwise (dist > unit.range) fall through to move closer using pathfinding

        # Use A* to find a path from (ux,uy) to (tx,ty)
        try:
            path = find_path(game_map, (ux, uy), (tx, ty))
        except Exception:
            path = []

        if path and len(path) >= 2:
            # move up to `unit.speed` steps along the path (path[0] == start)
            steps = min(max(1, getattr(unit, "speed", 1)), len(path) - 1)
            next_pos = path[steps]
            nx, ny = next_pos
            # final safety checks
            if 0 <= nx < game_map.width and 0 <= ny < game_map.height and game_map.grid[nx][ny].is_empty():
                game_map.move_unit(unit, nx, ny)
                return
            else:
                # If target tile became occupied, fall back to scanning the row for nearest empty
                for alt in path[1:]:
                    ax, ay = alt
                    if 0 <= ax < game_map.width and 0 <= ay < game_map.height and game_map.grid[ax][ay].is_empty():
                        game_map.move_unit(unit, ax, ay)
                        return

        # If pathfinding failed or produced no usable step, fall back to greedy neighbor scanning
        candidates = self._neighbour_steps_toward(ux, uy, tx, ty)
        for new_x, new_y in candidates:
            if not (0 <= new_x < game_map.width and 0 <= new_y < game_map.height):
                continue
            tile = game_map.grid[new_x][new_y]
            if tile.building is not None:
                continue
            if tile.is_empty():
                game_map.move_unit(unit, new_x, new_y)
                return

        # If no preferred candidate, do nothing (blocked) — rely on next tick to recompute path.

    def distance(self, u1, u2):
        x1, y1 = u1.position
        x2, y2 = u2.position
        return abs(x1 - x2) + abs(y1 - y2)


# Registry to reconstruct General from saved class name
_GENERAL_REGISTRY: Dict[str, type] = {
    "CaptainBraindead": CaptainBraindead,
    "MajorDaft": MajorDaft,
}


def general_from_name(name: str) -> General:
    cls = _GENERAL_REGISTRY.get(name)
    if cls:
        return cls()
    # fallback to a default
    return CaptainBraindead()