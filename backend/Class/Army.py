from typing import List, Dict, Any


class Army:
    def __init__(self, owner: str):
        self.owner = owner
        self.units = []  # list of Unit objects

    def add_unit(self, unit):
        self.units.append(unit)

    def living_units(self):
        return [u for u in self.units if u.is_alive()]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner": self.owner,
            "unit_ids": [u.id for u in self.units],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], units_by_id: Dict[str, object]) -> "Army":
        army = cls(data["owner"])
        for uid in data.get("unit_ids", []):
            unit = units_by_id.get(uid)
            if unit:
                army.add_unit(unit)
        return army