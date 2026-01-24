from backend.Class.Map import Map
from backend.Class.Units import Unit
from backend.Class.Action import Action


class Army:
    def __init__(self):

        self.gameMode=None
        self.general = None
        self.units = []  # list of Unit objects

    def add_unit(self, unit: Unit):
        unit.army = self
        self.units.append(unit)


    def isEmpty(self):
        return len(self.living_units()) <= 0

    def living_units(self):
        return [u for u in self.units if u.is_alive()]

    def dead_units(self):
        return [u for u in self.units if not u.is_alive()]


    def testTargets(self, targets, map: Map, otherArmy ):
        # Le générale donne juste des cibles, il associe une unité à une unité adverse
        # L'objectif de cette fonction est de transformer cette association en action
        # Si l'unité cible est trop loin il faut que l'unité se déplace et si elle est dans le champ d'action elle l'attaque
        # Il faut aussi verifier que l'unité peut avancer (elle n'est pas face a un mur ou une autre unité)
        #Il faut vérifier que le cooldown est a zero si on veut attaqué et si le cooldown n'est pas à 0 il faut le diminuer
        actions = []

        if isinstance(targets, list):
            targets = {u: t for u, t in targets}

        for unit, target in targets.items():
            if unit.is_alive() and target.is_alive():
                ux, uy = unit.position
                tx, ty = target.position

                dx = tx - ux
                dy = ty - uy
                dist2 = dx * dx + dy * dy

                #print(unit, target, dist2, unit.range,dist2 <= unit.range **2)

                # ATTAQUE
                if dist2 <= unit.range **2 :
                    if unit.cooldown <= 0:
                        actions.append(Action(unit, "attack", target))
                else:
                    vector = (ux+dx/(dist2**0.5)*unit.speed, uy+dy/(dist2**0.5)*unit.speed)
                    """
                    # DÉPLACEMENT (A*)
                    path = find_path(
                        map,
                        unit.position,
                        target.position,
                        unit,
                        self,  # armée alliée
                        otherArmy  # armée ennemie
                    )
                    """


                    actions.append(
                        Action(unit, "move", vector)
                    )





        return actions

    def execOrder(self, orders: Action, otherArmy):
        for unit in self.units :
            if unit.cooldown > 0 : unit.cooldown-=1
        #Cette fonction applique les dégâts avec les bonus sur l'armée adverse et
        # déplace des unités alliées à la bonne vitesse selon les ordres.
        """
        Applique les actions décidées par testTargets :
        - attaque : dégâts + cooldown
        - déplacement : mise à jour de la position
        """

        for action in orders:

            unit = action.unit
            
            # ATTAQUE
            if action.kind == "attack":
                target = action.target

                bonus = 0
                for classe in target.classes :
                    bonus += unit.bonuses.get(classe,0)
                if target.armor - bonus - unit.attack < 0:
                    target.hp+=target.armor - bonus - unit.attack
                unit.cooldown = unit.reload_time
                target.last_attacker = unit
                """
                # la cible peut être morte entre temps
                if target.is_alive():continue

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
                
                """
            # DÉPLACEMENT
            elif action.kind == "move":
                new_pos = action.target
                # Clamp position to map bounds if map has dimensions
                if unit.army and unit.army.gameMode and unit.army.gameMode.map:
                    game_map = unit.army.gameMode.map
                    if hasattr(game_map, 'width') and hasattr(game_map, 'height'):
                        new_x = max(0, min(new_pos[0], game_map.width - 1))
                        new_y = max(0, min(new_pos[1], game_map.height - 1))
                        unit.position = (new_x, new_y)
                    else:
                        unit.position = new_pos
                else:
                    unit.position = new_pos

            

    def fight(self,map:Map, otherArmy ) :
        #print("me",len(self.living_units()), len(otherArmy.living_units()))

        targets = self.general.getTargets(map, otherArmy)
        #print("me", len(self.living_units()), len(otherArmy.living_units()))
        #print("targets" ,targets)
        orders = self.testTargets(targets,map,otherArmy)
        #print("me", len(self.living_units()), len(otherArmy.living_units()))
        #print("orders", orders)
        self.execOrder(orders, otherArmy)
        #print("me", len(self.living_units()), len(otherArmy.living_units()))
        #print("executer")


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
