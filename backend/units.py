# backend/units.py
from abc import ABC, abstractmethod

class Unit(ABC):
    def __init__(self, owner, hp, attack, armor, speed, range_, reload_time):
        self.owner = owner
        self.hp = hp
        self.attack = attack
        self.armor = armor
        self.speed = speed
        self.range = range_
        self.reload_time = reload_time
        self.position = None
        self.cooldown = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= max(1, dmg - self.armor)

    def can_attack(self):
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.reload_time

    @abstractmethod
    def unit_type(self):
        pass


class Knight(Unit):
    def __init__(self, owner):
        super().__init__(owner, hp=100, attack=10, armor=2,
                         speed=2, range_=1, reload_time=2)

    def unit_type(self):
        return "Knight"


class Pikeman(Unit):
    def __init__(self, owner):
        super().__init__(owner, hp=55, attack=4, armor=0,
                         speed=1, range_=1, reload_time=3)

    def unit_type(self):
        return "Pikeman"


class Crossbowman(Unit):
    def __init__(self, owner):
        super().__init__(owner, hp=35, attack=6, armor=0,
                         speed=1, range_=5, reload_time=3)

    def unit_type(self):
        return "Crossbowman"
