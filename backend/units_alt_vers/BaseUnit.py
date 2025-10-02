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
        self.position = 0  # simple 1D position
        self.classes = classes if classes else [] #class type (cavalry,archer,etc)
        self.bonuses = bonuses if bonuses else {} #bonus damage against certain classes

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg, dmg_type="melee"):
        if dmg_type == "melee":
            dmg = max(1, dmg - self.armor)
        elif dmg_type == "pierce":
            dmg = max(1, dmg - self.pierce_armor)
        self.hp -= dmg
