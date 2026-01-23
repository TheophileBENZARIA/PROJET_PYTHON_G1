from General import General
from backend.Class.Army import Army
from backend.Class.Map import Map


class CaptainBraindead(General):
    """
    This general gives no proactive orders: a unit only retaliates against the
    last enemy that hit it. If no one attacked the unit yet, it receives no target.
    """

    def getTargets(self, map: Map, otherArmy: Army):
        targets = []

        enemy_units = set(otherArmy.living_units())

        for unit in self.army.living_units():
            last_attacker = getattr(unit, "last_attacker", None)
            if last_attacker in enemy_units:
                targets.append((unit, last_attacker))
            else:
                # Clean up stale references so next ticks don't keep checking dead enemies
                if hasattr(unit, "last_attacker") and unit.last_attacker not in enemy_units:
                    unit.last_attacker = None

        return targets
