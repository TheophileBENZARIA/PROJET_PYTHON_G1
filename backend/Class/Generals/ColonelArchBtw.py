from backend.Class.Generals.General import General
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman


class ColonelArchBtw(General) :
    def getTargets(self, map, otherArmy):
        targets=[]
        enemy_units = otherArmy.living_units()
        for unit in self.army.living_units() :
            target = None
            dist = float("inf")
            if isinstance(unit, Crossbowman) :
                for enemy in enemy_units :
                    if isinstance(enemy,Pikeman) :
                        tdist = self.__distance_sq(unit,enemy)
                        if tdist<dist :
                            target = enemy
                            dist = tdist
            elif isinstance(unit, Pikeman) :
                for enemy in enemy_units :
                    if isinstance(enemy,Knight) :
                        tdist = self.__distance_sq(unit,enemy)
                        if tdist<dist :
                            target = enemy
                            dist = tdist
            elif isinstance(unit, Knight) :
                for enemy in enemy_units :
                    if isinstance(enemy,Crossbowman) :
                        tdist = self.__distance_sq(unit,enemy)
                        if tdist<dist :
                            target = enemy
                            dist = tdist

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

        return targets

    #this function computes the squared distance between two units
    @staticmethod
    def __distance_sq(u1, u2):
        if u1.position is None or u2.position is None:
            return float("inf")
        x1, y1 = u1.position
        x2, y2 = u2.position
        return (x1 - x2) ** 2 + (y1 - y2) ** 2
