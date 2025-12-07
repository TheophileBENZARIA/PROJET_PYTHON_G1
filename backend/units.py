# backend/units.py
from abc import ABC, abstractmethod
import uuid
from typing import Optional, Dict, Any, Tuple
import random
import logging

logger = logging.getLogger(__name__)


class Unit(ABC):
    def __init__(self, owner: str, hp: int, attack: int, armor: int,
                 speed: int, range_: int, reload_time: int, classes=None, bonuses=None, id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.owner = owner
        self.hp = hp
        self.attack = attack
        self.armor = armor
        self.speed = speed
        self.range = range_
        self.reload_time = reload_time
        self.position = None  # (x, y) or None
        self.classes = classes if classes else []
        self.bonuses = bonuses if bonuses else {}
        self.cooldown = 0

        # per-unit "order" set by the general each tick: usually a reference to an enemy unit
        self.current_target = None  # Optional[Unit]

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, dmg: int):
        # shared damage application (considers armor)
        applied = max(1, dmg - self.armor)
        self.hp -= applied
        if self.hp < 0:
            self.hp = 0
        logger.debug("%s took %d damage (after armor=%d) hp now=%d",
                     getattr(self, "unit_type", lambda: "unit")(), applied, self.armor, self.hp)
        return applied

    def can_attack(self) -> bool:
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.reload_time

    def compute_bonus(self, target) -> int:
        """Return the attack bonuses against the target based on its classes."""
        total = 0
        for cls in target.classes:
            if cls in self.bonuses:
                total += self.bonuses[cls]
        return total

    def attack_unit(self, target) -> Tuple[int, Optional[str]]:
        """
        Default attack - used by melee and by default for subclasses that don't override.
        Returns (applied_damage, optional_message)
        """
        if not target.is_alive():
            return 0, None
        # compute total damage including bonuses (do not mutate self.attack permanently)
        bonus = self.compute_bonus(target)
        raw = max(1, (self.attack + bonus) - target.armor)
        applied = target.take_damage(raw)
        self.cooldown = self.reload_time
        # no custom message by default
        return applied, None

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
            "classes":  self.classes,
            "bonuses":  self.bonuses,
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


# -------------------------
# Per-unit movement AI & concrete units
# -------------------------
class Knight(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        super().__init__(owner, hp=100, attack=10, armor=2,
                         speed=2, range_=1, reload_time=2, classes=["Cavalry"], bonuses={"Infantry": 2}, id=id)

    def unit_type(self) -> str:
        return "Knight"


class Pikeman(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        super().__init__(owner, hp=55, attack=4, armor=0,
                         speed=1, range_=1, reload_time=3, classes=["Infantry", "Spear"], bonuses={"Cavalry": 10}, id=id)

    def unit_type(self) -> str:
        return "Pikeman"


class Crossbowman(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        # longer range, slower reload, decent attack
        super().__init__(owner, hp=35, attack=6, armor=0,
                         speed=1, range_=5, reload_time=3, classes=["Archer"], bonuses={"Spear": 3, "Building": 0}, id=id)

    def unit_type(self) -> str:
        return "Crossbowman"

    def attack_unit(self, target) -> Tuple[int, Optional[str]]:
        """
        Ranged "shoot" attack with a small chance for the target to dodge.
        Returns (applied_damage, message) where message is a short human-readable string
        that will be added to the battle's compact event log.
        """
        if not target.is_alive():
            return 0, None

        # base dodge chance for ranged shots (tunable)
        base_miss = 0.10  # base 10% miss chance
        # scale with target speed, but keep within reasonable bounds
        speed_factor = 0.02 * max(0, (target.speed - 1))  # each extra speed adds 2% dodge
        dodge_chance = min(0.25, base_miss + speed_factor)  # clamp at 25%

        roll = random.random()
        if roll < dodge_chance:
            # Miss / dodge
            self.cooldown = self.reload_time
            msg = f"{self.owner}'s {self.unit_type()} fires at {target.owner}'s {target.unit_type()} but it dodges!"
            logger.debug(msg + f" (roll={roll:.3f} dodge={dodge_chance:.3f})")
            return 0, msg

        # Hit: compute damage using same formula and route through take_damage()
        bonus = self.compute_bonus(target)
        raw = max(1, (self.attack + bonus) - target.armor)
        applied = target.take_damage(raw)
        self.cooldown = self.reload_time
        msg = f"{self.owner}'s {self.unit_type()} shoots {target.owner}'s {target.unit_type()} for {applied} dmg (HP={target.hp})"
        logger.debug("%s", msg)
        return applied, msg