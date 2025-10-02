from .unit import BaseUnit

class Knight(BaseUnit):
    def __init__(self):
        super().__init__(
            name="Knight",
            hp=100,
            attack=10,
            armor=2,
            pierce_armor=2,
            attack_range=0,
            speed=1.5,
            reload_time=1.8,
            classes=["Cavalry"],
        )

class Pikeman(BaseUnit):
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
            bonuses={"Cavalry": 22, "Elephant": 25, "Camel": 18}
        )

class Crossbowman(BaseUnit):
    def __init__(self):
        super().__init__(
            name="Crossbowman",
            hp=35,
            attack=5,
            armor=0,
            pierce_armor=0,
            attack_range=5,
            speed=0.96,
            reload_time=2.0,
            classes=["Archer"],
            bonuses={"Spear": 3}
        )
