from backend.Class.Map import Map
from backend.Class.Units import Unit
from backend.Utils.pathfinding import find_path
from backend.Class.Action import Action


class Army:
    def __init__(self):

        self.gameMode=None
        self.general = None
        self.__units = []  # list of Unit objects

    def add_unit(self, unit: Unit):
        unit.army = self
        self.__units.append(unit)

    def isEmpty(self):
        return len(self.living_units()) <= 0

    def living_units(self):
        return [u for u in self.__units if u.is_alive()]

    def dead_units(self):
        return [u for u in self.__units if not u.is_alive()]


    def testTargets(self, targets, map: Map, otherArmy: object ):
        # Le générale donne juste des cibles, il associe une unité à une unité adverse
        # L'objectif de cette fonction est de transformer cette association en action
        # Si l'unité cible est trop loin il faut que l'unité se déplace et si elle est dans le champ d'action elle l'attaque
        # Il faut aussi verifier que l'unité peut avancer (elle n'est pas face a un mur ou une autre unité)
        #Il faut vérifier que le cooldown est a zero si on veut attaqué et si le cooldown n'est pas à 0 il faut le diminuer
        actions = []

        if isinstance(targets, list):
            targets = {u: t for u, t in targets}

        for unit, target in targets.items():

            if unit not in self.living_units():
                continue
            if target not in otherArmy.living_units():
                continue

            ux, uy = unit.position
            tx, ty = target.position

            dx = tx - ux
            dy = ty - uy
            dist2 = dx * dx + dy * dy

            
            # ATTAQUE
            if dist2 <= unit.range * unit.range:
                if unit.cooldown == 0:
                    actions.append(
                        Action(unit=unit, kind="attack", target=target)
                    )
                else:
                    unit.cooldown -= 1
                continue

            
            # DÉPLACEMENT (A*)
            path = find_path(
                map,
                unit.position,
                target.position,
                unit,
                self,          # armée alliée
                otherArmy      # armée ennemie
            )

            if not path or len(path) < 2:
                continue

            next_pos = path[1]

            actions.append(
                Action(unit=unit, kind="move", target=next_pos)
            )

        return actions

    def execOrder(self, orders: Action, otherArmy: object):
        #Cette fonction applique les dégâts avec les bonus sur l'armée adverse et
        # déplace des unités alliées à la bonne vitesse selon les ordres.
        """
        Applique les actions décidées par testTargets :
        - attaque : dégâts + cooldown
        - déplacement : mise à jour de la position
        """

        for action in orders:

            unit = action.unit

            if unit not in self.living_units():
                continue
            
            # ATTAQUE
            if action.kind == "attack":
                target = action.target

                # la cible peut être morte entre temps
                if target not in otherArmy.living_units():
                    continue

                # calcul des dégâts (inclut bonus de classe si disponible)
                bonus = 0
                if hasattr(unit, "compute_bonus") and callable(getattr(unit, "compute_bonus")):
                    try:
                        bonus = unit.compute_bonus(target)
                    except Exception:
                        bonus = 0

                damage = max(0, (unit.attack + bonus) - target.armor)
                target.hp -= damage
                target.last_attacker = unit

                # reset du cooldown
                unit.cooldown = unit.reload_time

            # DÉPLACEMENT
            elif action.kind == "move":
                new_pos = action.target
                unit.position = new_pos
                unit.cooldown -= 1

    def fight(self,map:Map, otherArmy: object ) :

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
