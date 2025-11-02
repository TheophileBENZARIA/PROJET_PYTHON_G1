from .unit import BaseUnit2

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
            classes=["Cavalry"]
            bonuses={}
        )

def __str__(self):
        return f"{self.name} (HP={self.hp}/{self.max_hp})"
