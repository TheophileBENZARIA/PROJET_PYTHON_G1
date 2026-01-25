from backend.Class.Generals.General import General
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Monk import Monk
from backend.Class.Units.Pikeman import Pikeman


class ColonelArchBtw(General) :
    def getTargets(self, map, otherArmy):
        targets=[]
        enemy_units = otherArmy.living_units()
        for unit in self.army.living_units() :
            target = None
            #if unit.last_attacked and unit.last_attacked.is_alive() :
            #    targets.append((unit, unit.last_attacked))
            #else :
            if isinstance(unit, Crossbowman):
                pikemans = [e for e in enemy_units if isinstance(e, Pikeman)]
                target = self.enemy_in_range(unit, pikemans)
            elif isinstance(unit, Pikeman):
                knights = [e for e in enemy_units if isinstance(e, Knight)]
                target = self.enemy_in_range(unit, knights)
            elif isinstance(unit, Knight):
                my_cross = [e for e in self.army.living_units() if isinstance(e, Crossbowman)]
                if self.enemy_in_range(unit, my_cross, 5):
                    crossbowmans = [e for e in enemy_units if isinstance(e, Crossbowman)]
                    target = self.enemy_in_range(unit, crossbowmans)
                else:
                    target = self.enemy_in_range(unit, enemy_units)



            if target is not None :
                targets.append((unit, target))
            else:

                last_attacker = getattr(unit, "last_attacker", None)
                if last_attacker in enemy_units:
                    targets.append((unit, last_attacker))
                else:

                    target = min(
                        enemy_units,
                        key=lambda enemy: self.__distance_sq(unit, enemy),
                        default=None,
                    )
                    if target is not None :
                        targets.append((unit, target))

            if isinstance(unit,Monk):
                allies = [a for a in self.army.living_units() if a.hp < a.max_hp]
                if allies:
                    target = min(allies, key=lambda allie: self.__distance_sq(unit, allie))
                    targets.append((unit, target))

        return targets

    def enemy_in_range(self,unit, enemy_units, range=0):
        target = min(
            enemy_units,
            key=lambda enemy: self.__distance_sq(unit, enemy),
            default=None,
        )
        if not range or (target and self.__distance_sq(unit, target) < range ** 2):
            return target
        return None


    #this function computes the squared distance between two units
    @staticmethod
    def __distance_sq(u1, u2):
        if u1.position is None or u2.position is None:
            return float("inf")
        x1, y1 = u1.position
        x2, y2 = u2.position
        return (x1 - x2) ** 2 + (y1 - y2) ** 2
