from backend.Class.Map import Map
from backend.Class.Units import Unit
from backend.Class.Generals import General
from backend.Class.Battle import Battle

class Army:
    def __init__(self):

        self.battle = None
        self.general = None

        self._units = []  # list of Unit objects

    def add_unit(self, unit: Unit):
        self._units.append(unit)

    def living_units(self):
        return [u for u in self._units if u.is_alive()]

    def dead_units(self):
        return [u for u in self._units if not u.is_alive()]


    def testTargets(self, targets, map: Map, otherArmy: Army):
        # Le générale donne juste des cibles, il associe une unité à une unité adverse
        # L'objectif de cette fonction est de transformer cette association en action
        # Si l'unité cible est trop loin il faut que l'unité se déplace et si elle est dans le champ d'action elle l'attaque
        # Il faut aussi verifier que l'unité peut avancer (elle n'est pas face a un mur ou une autre unité)
        #Il faut vérifier que le cooldown est a zero si on veut attaqué et si le cooldown n'est pas à 0 il faut le diminuer
        pass

    def execOrder(self, orders, otherArmy:Army):
        #Cette fonction applique les dégâts avec les bonus sur l'armée adverse et
        # déplace des unités alliées à la bonne vitesse selon les ordres.
        pass

    def fight(self,map:Map, otherArmy : Army) :

        targets = self.general.getTargets(map, otherArmy)
        orders = self.testTargets(targets,map,otherArmy)

        self.execOrder(orders, otherArmy)




    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any], units_by_id: Dict[str, object]) -> "Army":
        army = cls(data["owner"])
        for uid in data.get("unit_ids", []):
            unit = units_by_id.get(uid)
            if unit:
                army.add_unit(unit)
        return army



    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner": self.owner,
            "unit_ids": [u.id for u in self.units],
        }

"""