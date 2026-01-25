from backend.Class.Units.Unit import Unit


class Monk(Unit):
    def __init__(self, position: tuple[float]):
        super().__init__(hp=30, attack=4, armor=0,
                         speed=1, range_=9, reload_time=62, ligne_of_sight=11,position=position, classes=[], bonuses={})

    def unit_type(self) -> str:
        return "Monk"
