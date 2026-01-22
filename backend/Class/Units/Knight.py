from Unit import Unit
from backend.Class.Army import Army


class Knight(Unit):
    def __init__(self, army: Army, position: tuple[float]):
        super().__init__(hp=100, attack=10, armor=2,
                         speed=2, range_=1, reload_time=2,position=position, classes=["Cavalry"], bonuses={"Infantry": 2})

    def unit_type(self) -> str:
        return "Knight"
