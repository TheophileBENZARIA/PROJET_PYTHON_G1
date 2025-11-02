import math

class BaseUnit:
    def __init__(self, name, hp, attack, armor, pierce_armor,
                 attack_range, speed, reload_time, classes=None, bonuses=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.armor = armor
        self.pierce_armor = pierce_armor
        self.range = attack_range
        self.speed = speed
        self.reload_time = reload_time
        self.cooldown = 0.0
        self.position = (0, 0)        # now 2D (x, y)
        self.classes = classes if classes else []
        self.bonuses = bonuses if bonuses else {}
        self.target = None

    # --- Core mechanics ---
    def is_alive(self):
        return self.hp > 0

    def distance_to(self, other):
        """Manhattan distance (grid-based)"""
        x1, y1 = self.position
        x2, y2 = other.position
        return abs(x1 - x2) + abs(y1 - y2)

    def take_damage(self, dmg, dmg_type="melee"):
        """Apply armor reduction and deduct HP."""
        if dmg_type == "melee":
            dmg = max(1, dmg - self.armor)
        elif dmg_type == "pierce":
            dmg = max(1, dmg - self.pierce_armor)
        self.hp -= dmg

    def can_attack(self, target):
        """Check if within attack range."""
        return self.distance_to(target) <= self.range

    def deal_damage(self, target, dmg_type="melee"):
        """Deal damage to a target."""
        from engine.combat import compute_damage
        dmg = compute_damage(self, target, dmg_type)
        target.take_damage(dmg, dmg_type)
