from .unit import BaseUnit2

class Crossbowman(BaseUnit):
    def __init__(self):
        super().__init__(
            name="Crossbowman",
            hp=35,
            attack=5,
            armor=0,
            pierce_armor=0,
            attack_range=5,         # ranged attack
            speed=0.96,
            reload_time=2.0,
            classes=["Archer"],
            bonuses={
                "Spear": 3,         # minor bonus vs spear-type infantry
                "Building": 0       # placeholder for consistency
            }
        )

    def __str__(self):
        return f"{self.name} (HP={self.hp}/{self.max_hp})"
