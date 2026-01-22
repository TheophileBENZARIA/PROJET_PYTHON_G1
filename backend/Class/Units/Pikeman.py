import random

from Unit import Unit
from backend.Class.Army import Army


class Pikeman(Unit):


    def __init__(self, army: Army, position: tuple[float]):
        super().__init__(hp=55, attack=4, armor=0,
                         speed=1, range_=1, reload_time=3, position=position, classes=["Infantry", "Spear"], bonuses={"Cavalry": 10})

    def unit_type(self) -> str:
        return "Pikeman"

    @property
    def attack(self):
        if random.randint(1,100) >= 85 : return 0
        return self.__attack
