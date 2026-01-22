import Unit

class Pikeman(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        super().__init__(owner, hp=55, attack=4, armor=0,
                         speed=1, range_=1, reload_time=3, classes=["Infantry", "Spear"], bonuses={"Cavalry": 10},
                         id=id)

    def unit_type(self) -> str:
        return "Pikeman"
