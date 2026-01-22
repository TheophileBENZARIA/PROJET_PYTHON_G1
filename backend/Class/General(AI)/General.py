# backend/generals.py
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional, List
from backend.pathfinding import find_path


def _manhattan(a: Optional[Tuple[int, int]], b:  Optional[Tuple[int, int]]) -> int:
    """Manhattan distance between two positions, handling None safely."""
    if a is None or b is None:
        return 10 ** 9
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
    def from_dict(cls, data:  dict):
        """
        Restore a General from a dict produced by `to_dict`.
        Expects a dict with a `"class"` key containing the class name saved by `to_dict`.
        Falls back to returning a default general if the name is unknown.
        """
        if not isinstance(data, dict):
            raise TypeError("General.from_dict expects a dict")
        name = data.get("class") or data.get("name")
        return general_from_name(name)




# Registry to reconstruct General from saved class name
_GENERAL_REGISTRY:  Dict[str, type] = {
    "CaptainBraindead": CaptainBraindead,
    "MajorDaft": MajorDaft,
    "GeneralClever": GeneralClever,
}


def general_from_name(name:  str) -> General:
    cls = _GENERAL_REGISTRY.get(name)
    if cls:
        return cls()
    # fallback to a default
    return CaptainBraindead()