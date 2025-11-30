# backend/units.py
from abc import ABC, abstractmethod
import uuid
from typing import Optional, Dict, Any
import random
import logging

logger = logging.getLogger(__name__)


class Unit(ABC):
    def __init__(self, owner: str, hp: int, attack: int, armor: int,
                 speed: int, range_: int, reload_time: int, id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.owner = owner
        self.hp = hp
        self.attack = attack
        self.armor = armor
        self.speed = speed
        self.range = range_
        self.reload_time = reload_time
        self.position = None  # (x, y) or None
        self.cooldown = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, dmg: int):
        # shared damage application (considers armor)
        applied = max(1, dmg - self.armor)
        self.hp -= applied
        if self.hp < 0:
            self.hp = 0
        logger.debug("%s took %d damage (after armor=%d) hp now=%d", getattr(self, "unit_type", lambda: "unit")(), applied, self.armor, self.hp)
        return applied

    def can_attack(self) -> bool:
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.reload_time

    def attack_unit(self, target):
        """Default attack - used by melee and by default for subclasses that don't override."""
        if not target.is_alive():
            return 0
        dmg = max(1, self.attack - target.armor)
        # apply damage through take_damage to keep behavior consistent
        applied = target.take_damage(dmg)
        self.cooldown = self.reload_time
        return applied

    @abstractmethod
    def unit_type(self) -> str:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "owner": self.owner,
            "hp": self.hp,
            "attack": self.attack,
            "armor": self.armor,
            "speed": self.speed,
            "range": self.range,
            "reload_time": self.reload_time,
            "position": list(self.position) if self.position is not None else None,
            "cooldown": self.cooldown,
            "unit_type": self.unit_type(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Unit":
        unit_type = data.get("unit_type")
        owner = data["owner"]
        # instantiate right subclass
        if unit_type == "Knight":
            unit = Knight(owner, id=data.get("id"))
        elif unit_type == "Pikeman":
            unit = Pikeman(owner, id=data.get("id"))
        elif unit_type == "Crossbowman":
            unit = Crossbowman(owner, id=data.get("id"))
        else:
            # Fallback: basic Unit-like object via generic subclass
            raise ValueError(f"Unknown unit_type: {unit_type}")

        # restore mutable state
        unit.hp = data.get("hp", unit.hp)
        unit.cooldown = data.get("cooldown", 0)
        pos = data.get("position")
        unit.position = tuple(pos) if pos is not None else None
        return unit


class Knight(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        super().__init__(owner, hp=100, attack=10, armor=2,
                         speed=2, range_=1, reload_time=2, id=id)

    def unit_type(self) -> str:
        return "Knight"


class Pikeman(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        super().__init__(owner, hp=55, attack=4, armor=0,
                         speed=1, range_=1, reload_time=3, id=id)

    def unit_type(self) -> str:
        return "Pikeman"


class Crossbowman(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        # longer range, slower reload, decent attack
        super().__init__(owner, hp=35, attack=6, armor=0,
                         speed=1, range_=5, reload_time=3, id=id)

    def unit_type(self) -> str:
        return "Crossbowman"

    def attack_unit(self, target):
        """
        Ranged "shoot" attack with a small chance for the target to dodge.
        - Dodge probability depends on target.speed (faster units dodge a bit more)
        - Dodge is clamped so it never becomes too frequent.
        - On a miss, damage applied = 0 but cooldown is still consumed.
        """
        if not target.is_alive():
            return 0

        # base dodge chance for ranged shots (tunable)
        base_miss = 0.10  # base 10% miss chance
        # scale with target speed, but keep within reasonable bounds
        speed_factor = 0.02 * max(0, (target.speed - 1))  # each extra speed adds 2% dodge
        dodge_chance = min(0.25, base_miss + speed_factor)  # clamp at 25%

        roll = random.random()
        if roll < dodge_chance:
            # Miss / dodge
            logger.debug("%s shot by %s missed (roll=%.3f < dodge=%.3f)", getattr(target, "unit_type", lambda: "unit")(), getattr(self, "unit_type", lambda: "unit")(), roll, dodge_chance)
            # still consume cooldown
            self.cooldown = self.reload_time
            # small 'glancing' effect could be added here; keep it simple: 0 applied damage
            # print to terminal so user can see misses
            print(f"{self.owner}'s {self.unit_type()} fires at {target.owner}'s {target.unit_type()} but it dodges!")
            return 0

        # Hit: compute damage using same formula and route through take_damage()
        raw_dmg = max(1, self.attack - target.armor)
        applied = target.take_damage(raw_dmg)
        self.cooldown = self.reload_time
        print(f"{self.owner}'s {self.unit_type()} shoots {target.owner}'s {target.unit_type()} for {applied} dmg (HP={target.hp})")
        logger.debug("%s shot %s for %d (hp after=%d)", self.unit_type(), target.unit_type(), applied, target.hp)
        return applied