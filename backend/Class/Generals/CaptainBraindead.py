from abc import ABC

from General import General
from backend.Utils.pathfinding import find_path

class CaptainBraindead(General):
    """
    A reactive general that doesn't proactively seek enemies, but units will
    retaliate against attackers they remember (threat memory system).
    Units pursue enemies that have attacked them, even ranged attackers.
    """

    def getTargets(self, army, enemy_army, game_map):
        """
        For each unit, check if they have a threat in memory (someone who attacked them).
        If so, move toward that threat to retaliate.
        """
        for unit in army.living_units():
            if unit.position is None:
                continue

            # Check for priority threat (most recent attacker)
            threat = unit.get_priority_threat()

            if threat is not None and threat.is_alive() and threat.position is not None:
                # Unit has been attacked, pursue the attacker
                self._move_toward_threat(unit, threat, game_map)

    @property
    def name(self):
        return "Captain Braindead"


