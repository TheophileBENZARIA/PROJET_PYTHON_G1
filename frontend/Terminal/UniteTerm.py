# frontend/Terminal/UniteTerm.py
"""
Small adapter class used by the curses Screen to display a single cell.
Provides a factory to create a display cell from a project Unit instance.
"""
from typing import Optional

class UniteTerm:
    def __init__(self, lettre: str = ".", team: Optional[int] = None, vie: Optional[int] = None):
        self.lettre = lettre
        self.team = team
        self.vie = vie

    def __str__(self):
        return self.lettre

    def __repr__(self):
        return f"UniteTerm(letter={self.lettre!r} team={self.team!r} hp={self.vie!r})"

def from_unit(unit) -> "UniteTerm":
    """
    Build a UniteTerm from a Unit object from backend.units.
    - letter: single-character marker for unit type (K, P, C, ?)
    - team: 1 for Player1, 2 for Player2 (None if unknown)
    - vie: current HP
    """
    if unit is None:
        return UniteTerm(".", None, None)

    # unit_type() may be a method on Unit classes
    try:
        utype = unit.unit_type()
    except Exception:
        utype = getattr(unit, "unit_type", lambda: "Unit")()

    # choose letter
    mapping = {
        "Knight": "K",
        "Pikeman": "P",
        "Crossbowman": "C",
    }
    letter = mapping.get(utype, utype[0].upper() if utype else "?")

    # team number
    team = 1 if getattr(unit, "owner", "") == "Player1" else (2 if getattr(unit, "owner", "") == "Player2" else None)

    hp = getattr(unit, "hp", None)
    return UniteTerm(letter, team, hp)