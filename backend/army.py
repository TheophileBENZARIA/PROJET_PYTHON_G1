# backend/army.py

class Army:
    def __init__(self, owner):
        self.owner = owner
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)

    def living_units(self):
        return [u for u in self.units if u.is_alive()]
