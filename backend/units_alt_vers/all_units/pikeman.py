from .unit import BaseUnit2

class Pikeman(BaseUnit):
    def __init__(self):
        super().__init__(
            name="Pikeman",
            hp=55,                  # base HP
            attack=4,               # base attack
            armor=0,                # melee armor
            pierce_armor=0,         # ranged armor
            attack_range=1,         # melee range (adjacent tiles)
            speed=1.0,              # movement tiles per tick
            reload_time=3.0,        # seconds per attack
            classes=["Infantry", "Spear"],
            bonuses={
                "Cavalry": 22,      # strong vs mounted units
                "Elephant": 25,
                "Camel": 18,
                "Ship": 16
            }
        )

