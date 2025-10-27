from abc import ABC, abstractmethod
import uuid
from typing import Optional, Dict, Any


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
        self.hp -= max(1, dmg - self.armor)

    def can_attack(self) -> bool:
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.reload_time

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
        super().__init__(owner, hp=35, attack=6, armor=0,
                         speed=1, range_=5, reload_time=3, id=id)

    def unit_type(self) -> str:
        return "Crossbowman"