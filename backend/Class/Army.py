
class Army:
    def __init__(self):
        self.battle = None
        self.general = None
        self._units = []  # list of Unit objects


    def add_unit(self, unit):
        self._units.append(unit)

    def living_units(self):
        return [u for u in self._units if u.is_alive()]




    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any], units_by_id: Dict[str, object]) -> "Army":
        army = cls(data["owner"])
        for uid in data.get("unit_ids", []):
            unit = units_by_id.get(uid)
            if unit:
                army.add_unit(unit)
        return army



    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner": self.owner,
            "unit_ids": [u.id for u in self.units],
        }

"""