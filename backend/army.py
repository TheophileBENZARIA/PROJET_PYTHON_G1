# backend/army.py

class Army:
    def __init__(self, owner): # owner is a string representing the army's owner
        self.owner = owner
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit) # Add a unit to the army

    def living_units(self):
        return [u for u in self.units if u.is_alive()] # Return a list of living units in the army
