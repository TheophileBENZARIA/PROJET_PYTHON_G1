from abc import ABC, abstractmethod
from typing import Dict


class General(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def issue_orders(self, army, enemy_army, game_map):
        pass

    def to_dict(self):
        # save class name so we can reconstruct
        return {"class": type(self).__name__}


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

    def move_toward(self, unit, target, game_map):
        ux, uy = unit.position
        tx, ty = target.position
        new_x = ux + (1 if tx > ux else -1 if tx < ux else 0)
        new_y = uy + (1 if ty > uy else -1 if ty < uy else 0)
        if game_map.grid[new_x][new_y].is_empty():
            game_map.move_unit(unit, new_x, new_y)

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