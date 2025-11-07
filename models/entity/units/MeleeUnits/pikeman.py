from entity.units.MeleeUnits.melees import *
from models.entity import units

class Pikeman(melees):
    def __init__(self):
        super().__init__(
            name="Pikeman",
            hp=55,
            attack=4,
            armor=0,
            pierce_armor=0,
            attack_range=0,
            speed=1.0,
            reload_time=3.0,
            classes=["Infantry","Spear"],
            bonuses={"Cavalry": 22, "Elephant": 25, "Camel": 18})