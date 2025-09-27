# backend/generals.py
from abc import ABC, abstractmethod

class General(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def issue_orders(self, army, enemy_army, game_map):
        pass


class CaptainBraindead(General):
    def __init__(self):
        super().__init__("Captain Braindead")

    def issue_orders(self, army, enemy_army, game_map):
        # Does nothing (units only retaliate when attacked)
        pass


class MajorDaft(General):
    def __init__(self):
        super().__init__("Major Daft")

    def issue_orders(self, army, enemy_army, game_map):
        for unit in army.living_units():
            enemies = enemy_army.living_units()
            if enemies:
                target = min(enemies, key=lambda e: self.distance(unit, e))
                print(f"{unit.unit_type()} moves toward {target.unit_type()}")

    def distance(self, u1, u2):
        x1, y1 = u1.position
        x2, y2 = u2.position
        return abs(x1 - x2) + abs(y1 - y2)
