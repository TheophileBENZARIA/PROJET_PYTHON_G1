# backend/battle.py
from backend.army import Army
from backend.generals import General
from backend.units import Unit
import time
from frontend.terminal_view import print_map

class Battle:
    def __init__(self, game_map, army1, general1, army2, general2):
        self.map = game_map
        self.army1 = army1
        self.army2 = army2
        self.general1 = general1
        self.general2 = general2
        self.tick = 0

    def run(self, max_ticks=10):
        while (self.tick < max_ticks
               and self.army1.living_units()
               and self.army2.living_units()):
            self.tick += 1
            print(f"\n--- Tick {self.tick} ---")

            self.general1.issue_orders(self.army1, self.army2, self.map)
            self.general2.issue_orders(self.army2, self.army1, self.map)

            # update game state
            self.update_units()

            # 🔹 Print the map every tick
            print_map(self.map)
            time.sleep(0.5)  # slow down so you can see updates

        # final result
        if self.army1.living_units() and not self.army2.living_units():
            return f"{self.general1.name} wins!"
        elif self.army2.living_units() and not self.army1.living_units():
            return f"{self.general2.name} wins!"
        else:
            return "Draw!"

    def update_units(self):
        for unit in self.army1.living_units() + self.army2.living_units():
            if unit.cooldown > 0:
                unit.cooldown -= 1
