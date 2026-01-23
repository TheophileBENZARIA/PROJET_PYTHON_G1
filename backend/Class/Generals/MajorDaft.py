from General import General
from backend.Class.Army import Army
from backend.Class.Map import Map


class MajorDaft(General):
    """
    An aggressive general that always moves units toward the nearest enemy.
    """

    def getTargets(self, map: Map, otherArmy: Army):
        targets = []
        for unit in self.army.living_units():
            enemies = otherArmy.living_units()

            if enemies:
                target = min(enemies, key=lambda e: self.__distance(unit, e))
                targets.append((unit,target))
            else :
                return None
        return targets

    @property
    def name(self):
        return "MajorDaft"

    @staticmethod
    def __distance(u1, u2):
        x1, y1 = u1.position
        x2, y2 = u2.position
        return (x1 - x2)**2 + (y1 - y2)**2

    """
    def __init__(self):
        super().__init__("Major Daft")

    def issue_orders(self, army, enemy_army, game_map):
        for unit in army.living_units():
            enemies = enemy_army. living_units()
            if enemies:
                target = min(enemies, key=lambda e:  self. distance(unit, e))
                self. move_toward(unit, target, game_map)

    def _neighbour_steps_toward(self, ux:  int, uy:  int, tx: int, ty:  int):
        
        #Return candidate neighbor steps (nx,ny) that tend to move from (ux,uy) closer to (tx,ty).
        
        dx = 1 if tx > ux else (-1 if tx < ux else 0)
        dy = 1 if ty > uy else (-1 if ty < uy else 0)

        candidates = []
        if dx != 0 or dy != 0:
            candidates.append((ux + dx, uy + dy))
        if dx != 0:
            candidates.append((ux + dx, uy))
        if dy != 0:
            candidates.append((ux, uy + dy))
        if dx != 0 and dy != 0:
            candidates.append((ux + dx, uy - dy))
            candidates.append((ux - dx, uy + dy))
        candidates.append((ux + 1, uy))
        candidates. append((ux - 1, uy))
        candidates.append((ux, uy + 1))
        candidates.append((ux, uy - 1))
        return candidates

    def move_toward(self, unit, target, game_map):
        
        #Move `unit` toward `target` using A* pathfinding to avoid buildings and occupied tiles.
        #Ranged units prefer to keep distance so they can shoot.
        
        if unit.position is None or target.position is None:
            return

        ux, uy = unit.position
        tx, ty = target. position

        if getattr(unit, "range", 1) > 1:
            dist = self.distance(unit, target)

            if dist < unit.range:
                dx = 1 if ux > tx else (-1 if ux < tx else 0)
                dy = 1 if uy > ty else (-1 if uy < ty else 0)
                new_x = ux + dx
                new_y = uy + dy
                if 0 <= new_x < game_map.width and 0 <= new_y < game_map.height:
                    tile = game_map. grid[new_x][new_y]
                    if tile.is_empty():
                        game_map.move_unit(unit, new_x, new_y)
                return

            if dist == unit.range:
                return

        try:
            path = find_path(game_map, (ux, uy), (tx, ty))
        except Exception:
            path = []

        if path and len(path) >= 2:
            steps = min(max(1, getattr(unit, "speed", 1)), len(path) - 1)
            next_pos = path[steps]
            nx, ny = next_pos
            if 0 <= nx < game_map.width and 0 <= ny < game_map.height and game_map.grid[nx][ny]. is_empty():
                game_map. move_unit(unit, nx, ny)
                return
            else:
                for alt in path[1:]:
                    ax, ay = alt
                    if 0 <= ax < game_map.width and 0 <= ay < game_map.height and game_map. grid[ax][ay].is_empty():
                        game_map.move_unit(unit, ax, ay)
                        return

        candidates = self._neighbour_steps_toward(ux, uy, tx, ty)
        for new_x, new_y in candidates:
            if not (0 <= new_x < game_map.width and 0 <= new_y < game_map. height):
                continue
            tile = game_map.grid[new_x][new_y]
            if tile.building is not None:
                continue
            if tile.is_empty():
                game_map.move_unit(unit, new_x, new_y)
                return

    
"""

