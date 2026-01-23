# backend/generals.py
from abc import ABC, abstractmethod

class General(ABC):

    def __init__(self):
        self.army = None


    @abstractmethod
    def getTargets(self, map, otherArmy):
        #C'est ici le la stratégie du générale s'opère, cette fonction ne fait qu'assigné une unité alliée à une unité ennemie,
        # selon des critères propres
        pass





"""
    @abstractmethod
    def issue_orders(self, army, enemy_army, game_map):
        pass

    def to_dict(self):
        # save class name so we can reconstruct
        return {"class": type(self).__name__}

    @classmethod
    def from_dict(cls, data:  dict):
        
        #Restore a General from a dict produced by `to_dict`.
        #Expects a dict with a `"class"` key containing the class name saved by `to_dict`.
        #Falls back to returning a default general if the name is unknown.
        
        if not isinstance(data, dict):
            raise TypeError("General.from_dict expects a dict")
        name = data.get("class") or data.get("name")
        return general_from_name(name)


def _manhattan(a: Optional[Tuple[int, int]], b:  Optional[Tuple[int, int]]) -> int:
    #Manhattan distance between two positions, handling None safely.
    if a is None or b is None:
        return 10 ** 9
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Registry to reconstruct General from saved class name





"""