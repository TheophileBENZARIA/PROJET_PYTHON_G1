import Unit
class Knight(Unit):
    def __init__(self, owner: str, id: Optional[str] = None):
        super().__init__(owner, hp=100, attack=10, armor=2,
                         speed=2, range_=1, reload_time=2, classes=["Cavalry"], bonuses={"Infantry": 2}, id=id)

    def unit_type(self) -> str:
        return "Knight"
