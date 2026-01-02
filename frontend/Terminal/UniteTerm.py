# frontend/Terminal/UniteTerm.py
from typing import Optional

class UniteTerm:
    """
    Small display cell: holds what to render for a map cell.

    Attributes:
      lettre: single-character symbol to draw
      team: optional team id for colorization (1 or 2)
      vie: optional HP value (not currently rendered, kept for future)
      building: True if this cell is a building (impassable)
      elevation: integer elevation (0 = plain, >0 = hill)
    """
    BUILDING_CHAR = "O"
    HILL_CHAR = "H"
    EMPTY_CHAR = "."
    CASTLE_CHAR = "N"

    def __init__(self, lettre: str = EMPTY_CHAR, team: Optional[int] = None,
                 vie: Optional[int] = None, building: bool = False, elevation: int = 0):
        self.lettre = lettre
        self.team = team
        self.vie = vie
        self.building = building
        self.elevation = elevation

    def __str__(self):
        # If this is a building or hill tile (and no unit), prefer terrain symbol
        if self.building:
            # If a specific letter set (e.g. castle 'N'), show it; otherwise use generic BUILDING_CHAR
            if self.lettre and self.lettre != self.EMPTY_CHAR:
                return self.lettre
            return self.BUILDING_CHAR
        if self.elevation and self.lettre == self.EMPTY_CHAR:
            return self.HILL_CHAR
        return self.lettre

    def __repr__(self):
        return (f"UniteTerm(letter={self.lettre!r} team={self.team!r} hp={self.vie!r} "
                f"building={self.building!r} elevation={self.elevation!r})")

def from_unit(unit, tile=None) -> "UniteTerm":
    """
    Build a UniteTerm from a Unit object.
    If `tile` is provided it will be used to set elevation/building flags for display.
    """
    if unit is None:
        # delegate to from_tile if tile given
        if tile is not None:
            return from_tile(tile)
        return UniteTerm(UniteTerm.EMPTY_CHAR, None, None, False, 0)

    try:
        utype = unit.unit_type()
    except Exception:
        utype = getattr(unit, "unit_type", lambda: "Unit")()

    mapping = {
        "Knight": "K",
        "Pikeman": "P",
        "Crossbowman": "C",
    }
    letter = mapping.get(utype, (utype[0].upper() if utype else "?"))

    team = 1 if getattr(unit, "owner", "") == "Player1" else (2 if getattr(unit, "owner", "") == "Player2" else None)
    hp = getattr(unit, "hp", None)
    elevation = 0
    building = False
    if tile is not None:
        elevation = int(getattr(tile, "elevation", 0) or 0)
        building = getattr(tile, "building", None) is not None

    return UniteTerm(letter, team, hp, building=building, elevation=elevation)

def from_tile(tile) -> "UniteTerm":
    """
    Build a UniteTerm from a Map.Tile instance.
    - If tile.unit exists, return from_unit(tile.unit, tile)
    - Else if tile.building is present, return building char
    - Else if tile.elevation > 0, return hill char
    - Else return empty char
    """
    if tile is None:
        return UniteTerm(UniteTerm.EMPTY_CHAR, None, None, False, 0)

    unit = getattr(tile, "unit", None)
    if unit is not None:
        return from_unit(unit, tile)

    building = getattr(tile, "building", None)
    elevation = int(getattr(tile, "elevation", 0) or 0)
    if building:
        # castle building stored as dict with type 'castle'
        if isinstance(building, dict) and building.get("type") == "castle":
            owner = building.get("owner")
            team = 1 if owner == "Player1" else (2 if owner == "Player2" else None)
            hp = building.get("hp")
            return UniteTerm(UniteTerm.CASTLE_CHAR, team, hp, building=True, elevation=elevation)
        # generic building
        return UniteTerm(UniteTerm.BUILDING_CHAR, None, None, building=True, elevation=elevation)
    if elevation > 0:
        return UniteTerm(UniteTerm.HILL_CHAR, None, None, building=False, elevation=elevation)
    return UniteTerm(UniteTerm.EMPTY_CHAR, None, None, building=False, elevation=0)