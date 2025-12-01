import time
import copy
from pathfinding import Unit as SteeringUnit
from units import Baseunit



TICK_RATE = 10
TICK_TIME = 1 / TICK_RATE


class Game:
    def __init__(self):
        self.units = []
        self.history = []   # store snapshots of the game state


    # ADD UNITS
    def add_unit(self, unit, x, y):
        unit.position = (x, y)
        unit.mover = SteeringUnit(
            name = unit.name + "_mover",
            x = x,
            y = y,
            radius = 0.5,          
            speed = unit.speed,    # same speed as RTS unit
            is_static = False
        )

        self.units.append(unit)


    # MAIN UPDATE LOOP
    def update(self, dt):
        for u in self.units:
            if not u.is_alive():
                continue

            # Decrease cooldown
            u.reload_left = max(0, u.reload_left - dt)

            # Try to find enemy
            target = self.find_target(u)
            if target:
                # Attack?
                if u.can_attack(target) and u.reload_left == 0:
                    u.deal_damage(target)
                    u.reload_left = u.reload_time
                else:
                    # Move toward target
                    self.move_toward(u, target, dt)

        # Remove dead units
        self.units = [u for u in self.units if u.is_alive()]

        # IMPORTANT: record the state for replay
        self.save_snapshot()


    # AI: Find closest target
    def find_target(self, unit):
        enemies = [
            u for u in self.units
            if u.team != unit.team and u.is_alive()
        ]
        if not enemies:
            return None
        return min(enemies, key=lambda e: unit.distance_to(e))



    # MOVEMENT (Manhattan-like)
    
    def move_toward(self, unit, target, dt):
        tx, ty = target.position

        # tell steering AI where to go
        unit.mover.set_target(tx, ty)

        # obstacles = other units' movers
        obstacles = [other.mover for other in self.units if other is not unit]

        # update movement using the steering algorithm
        unit.mover.update(obstacles)

        # sync RTS unit position with steering position
        unit.position = (
            unit.mover.position.x,
            unit.mover.position.y
        )




    # SAVE SNAPSHOT 
    def save_snapshot(self):
        snapshot = []

        for u in self.units:
            snapshot.append({
                "name": u.name,
                "hp": u.hp,
                "max_hp": u.max_hp,
                "position": u.position,
                "reload_left": u.reload_left,
                "target": u.target.name if u.target else None,
                "armor": u.armor,
                "pierce_armor": u.pierce_armor,
            })

        # deep copy ensures history is immutable
        self.history.append(copy.deepcopy(snapshot))