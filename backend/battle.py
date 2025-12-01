# File: `backend/battle.py`
# python
from typing import Dict, List, Any
from dataclasses import dataclass
from backend.army import Army
from backend.generals import General
import time
from frontend.terminal_view import print_map
import logging

logger = logging.getLogger(__name__)
MAX_TICKS = 100 # Valeur déjà définie

@dataclass
class BattleResult:
    winner: str
    surviving_units: Dict[str, List[Dict[str, Any]]]
    ticks: int

    def __repr__(self) -> str:
        return f"BattleResult(winner={self.winner!r}, ticks={self.ticks}, surviving_units={{...}})"

class Battle:
    def __init__(self, game_map, army1: Army, general1: General, army2: Army, general2: General):
        self.map = game_map
        self.army1 = army1
        self.army2 = army2
        self.general1 = general1
        self.general2 = general2
        self.tick = 0

    def run(self, delay: float = 0.5) -> BattleResult:
        """
        Run the battle.

        - Runs until one/both armies are destroyed or a fixed maximum of MAX_TICKS is reached.
        - delay: seconds to sleep after each tick (set to 0 for no sleep / headless).

        Returns:
            BattleResult(winner, surviving_units, ticks)
        """
        # Mise à jour: utilise MAX_TICKS pour l'arrêt
        while (self.tick < MAX_TICKS 
               and self.army1.living_units() 
               and self.army2.living_units()):
            self.tick += 1
            logger.debug("=== Tick %d starting ===", self.tick)
            print(f"\n--- Tick {self.tick} ---")


            # Issue orders (move/attack planning)
            self.general1.issue_orders(self.army1, self.army2, self.map)
            self.general2.issue_orders(self.army2, self.army1, self.map)

            logger.debug("About to call update_units (tick=%d)", self.tick)

            # update game state (movement, attacks, cooldowns, death cleanup)
            self.update_units()

            logger.debug("Returned from update_units (tick=%d)", self.tick)

            # Print the map every tick
            print_map(self.map)
            self.debug_print_tick()

            if delay and delay > 0:
                time.sleep(delay)  # slow down so you can see updates

        # determine winner
        army1_alive = bool(self.army1.living_units())
        army2_alive = bool(self.army2.living_units())

        if army1_alive and not army2_alive:
            winner = self.general1.name
        elif army2_alive and not army1_alive:
            winner = self.general2.name
        else:
            winner = "Draw"

        # collect surviving units as serializable dicts
        surviving_units: Dict[str, List[Dict[str, Any]]] = {}
        for army in (self.army1, self.army2):
            surviving_units[army.owner] = [u.to_dict() for u in army.living_units()]

        #self.debug_print_tick()

        return BattleResult(winner=winner, surviving_units=surviving_units, ticks=self.tick)

    # python
    def debug_print_tick(self):
        """Print per-tick unit HP/position to debug death/damage logic."""
        print(f"--- Tick {self.tick} ---")
        for side_name, army in (("Player1", getattr(self, "army1", None)), ("Player2", getattr(self, "army2", None))):
            if army is None:
                print(f"{side_name}: <no army>")
                continue
            units = getattr(army, "units", None) or getattr(army, "soldiers", None) or []
            print(f"{side_name} units: {len(units)}")
            for u in units:
                uid = getattr(u, "id", getattr(u, "uid", None)) or getattr(u, "__class__", type(u)).__name__
                pos = getattr(u, "position", None)
                hp = getattr(u, "hp", getattr(u, "health", getattr(u, "hitpoints", None)))
                alive = getattr(u, "is_alive", None)
                alive_str = alive() if callable(alive) else (hp is None or hp > 0)
                print(f"  {uid} pos={pos} hp={hp} alive={alive_str}")
        print("---------------------")

    def update_units(self):

        logger.debug("entered update_units tick=%d: army1=%s army2=%s",
                     self.tick,
                     len(self.army1.living_units()) if self.army1 else 0,
                     len(self.army2.living_units()) if self.army2 else 0)

        all_units = self.army1.living_units() + self.army2.living_units()
        
        # --- NOUVELLE ÉTAPE 1: MOUVEMENT ---
        
        # 0) Préparation pour le mouvement (utilise la méthode move_unit dans Map pour déplacer sur la grille)
        # Chaque unité doit déterminer sa prochaine position (x, y)
        for unit in all_units:
            if not unit.is_alive() or unit.position is None:
                continue

            # Tente d'obtenir la position cible du pathfinding
            new_pos = getattr(unit, "get_next_position", lambda m, a: None)(self.map, all_units)
            if new_pos is not None:
                try:
                    # La carte gère la mise à jour des positions
                    self.map.move_unit(unit, new_pos[0], new_pos[1])
                    logger.debug("%s moved from %s to %s", unit.unit_type(), unit.position, new_pos)
                except ValueError as e:
                    logger.debug("Move failed for %s: %s", unit.unit_type(), e)


        # 1) Cooldown management
        # Remarque: Les unités qui ont attaqué (attaque_unit) ont leur cooldown mis à jour
        for unit in all_units:
            if unit.cooldown > 0:
                unit.cooldown -= 1

        # 2) Handle melee/ranged combat
        all_units = self.army1.living_units() + self.army2.living_units() # rafraîchir la liste après mouvement

        for unit in all_units:
            if not unit.is_alive() or unit.position is None:
                continue
            
            # Déterminer l'armée adverse
            enemy_army = self.army2 if unit.owner == self.army1.owner else self.army1
            enemies = enemy_army.living_units()
            if not enemies:
                continue

            # Trouver tous les ennemis à portée d'attaque
            enemies_in_range = [
                e for e in enemies
                if e.position and self.distance(unit, e) <= unit.range
            ]
            if not enemies_in_range:
                continue

            # Choisir l'ennemi le plus proche à attaquer
            target = min(enemies_in_range, key=lambda e: self.distance(unit, e))

            # Attaque si le cooldown le permet
            if unit.can_attack():
                dmg = unit.attack_unit(target)
                logger.debug("%s attacked %s for %d dmg (target hp=%s)",
                             getattr(unit, "unit_type", lambda: "unit")(),
                             getattr(target, "unit_type", lambda: "unit")(),
                             dmg,
                             getattr(target, "hp", None))
                print("target hp after attack:", target.hp)
                print(f"{unit.owner}'s {unit.unit_type()} attacks {target.owner}'s "
                      f"{target.unit_type()} for {dmg} dmg (HP={target.hp})")

                # Si la cible meurt, la retirer immédiatement
                if not target.is_alive():
                    self.remove_unit(target)
                    logger.debug("%s died (owner=%s)", getattr(target, "unit_type", lambda: "unit")(), target.owner)
                    print(f"💀 {target.owner}'s {target.unit_type()} has died!")
            
        # 3) Defensive cleanup (in case of simultaneous deaths)
        for army in [self.army1, self.army2]:
            army.units = army.living_units()

    def distance(self, u1, u2):
        """Return Manhattan distance between two units."""
        x1, y1 = u1.position
        x2, y2 = u2.position
        return abs(x1 - x2) + abs(y1 - y2)

    def remove_unit(self, unit):
        """Remove dead unit from map and clear its position."""
        if unit.position is None:
            return
        x, y = unit.position
        try:
            tile = self.map.grid[x][y]
            if tile.unit is unit:
                tile.unit = None
        except Exception:
            pass
        unit.position = None

    # python
    def to_dict(self) -> dict:
        """
        Return a JSON-serializable representation of this Battle.
        Delegates to .to_dict() on sub-objects (map, armies, generals) if available.
        Raises TypeError with a helpful message if a sub-object is not serializable.
        """
        def _serialize(obj):
            if obj is None or isinstance(obj, (str, int, float, bool)):
                return obj
            if isinstance(obj, list):
                return [_serialize(x) for x in obj]
            if isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
                return obj.to_dict()
            raise TypeError(f"Cannot serialize object of type {type(obj).__name__}; "
                            f"implement `to_dict()` on that class.")

        return {
            "map": _serialize(self.map),
            "army1": _serialize(self.army1),
            "army2": _serialize(self.army2),
            "general1": _serialize(self.general1),
            "general2": _serialize(self.general2),
            "tick": self.tick,
        }
    # python

    @classmethod
    def from_dict(cls, data: dict):
        """
        Recreate a Battle from a dict produced by Battle.to_dict().
        Handles Army.from_dict signatures that require a `units_by_id` dict by
        attempting to reconstruct units first using backend.units.Unit.from_dict.
        """
        import inspect

        if not isinstance(data, dict):
            raise TypeError("Battle.from_dict expects a dict")

        def _restore(obj_data, cls_type, label, extra=None):
            if obj_data is None:
                return None

            # If class accepts a second argument (units_by_id), pass it from extra
            try:
                sig = inspect.signature(cls_type.from_dict)
                params = list(sig.parameters.values())
                if len(params) >= 2:
                    # expects (cls, data, units_by_id) or similar
                    return cls_type.from_dict(obj_data, extra or {})
                else:
                    return cls_type.from_dict(obj_data)
            except (TypeError, ValueError, AttributeError):
                # Fallback: try calling with single arg
                try:
                    return cls_type.from_dict(obj_data)
                except Exception as e:
                    raise TypeError(
                        f"Cannot restore {label}: failed to call {cls_type.__name__}.from_dict -> {e}") from e

        # import component classes
        try:
            from backend.army import Army
        except Exception as e:
            raise TypeError(f"Cannot restore armies: failed to import backend.army -> {e}") from e

        try:
            from backend.generals import General
        except Exception as e:
            raise TypeError(f"Cannot restore generals: failed to import backend.generals -> {e}") from e

        MapClass = None
        try:
            from backend.map import Map as MapClass
        except Exception:
            try:
                from backend.map import GameMap as MapClass
            except Exception:
                MapClass = None

        # Prepare units_by_id mapping if Army.from_dict expects it.
        units_by_id = {}
        # Try to load Unit.from_dict if present
        UnitClass = None
        try:
            from backend.units import Unit as UnitClass
        except Exception:
            UnitClass = None

        if UnitClass is not None and hasattr(UnitClass, "from_dict"):
            # Collect any unit dicts found inside saved armies
            all_army_unit_dicts = []
            for key in ("army1", "army2"):
                a = data.get(key) or {}
                unit_list = a.get("units") or []
                if isinstance(unit_list, list):
                    all_army_unit_dicts.extend(unit_list)

            for ud in all_army_unit_dicts:
                try:
                    # prefer common id keys, fallback to None
                    uid = ud.get("id") if isinstance(ud, dict) else None
                    if uid is None:
                        uid = ud.get("uid") if isinstance(ud, dict) else None
                    unit_obj = UnitClass.from_dict(ud)
                    if uid is None:
                        # try to read attribute from object
                        uid = getattr(unit_obj, "id", None) or getattr(unit_obj, "uid", None)
                    if uid is None:
                        # fallback to object's id() to ensure uniqueness (not ideal but avoids crash)
                        uid = f"__gen_{id(unit_obj)}"
                    units_by_id[uid] = unit_obj
                except Exception:
                    # skip units we can't reconstruct here; Army.from_dict should tolerate missing ones or raise
                    continue

        # restore map (require Map.from_dict if a map was saved)
        if MapClass is None or not hasattr(MapClass, "from_dict"):
            if data.get("map") is not None:
                raise TypeError(
                    "Saved battle contains a map but no map class with `from_dict` was found. "
                    "Add `from_dict` to your map class or adjust the save format."
                )
            restored_map = None
        else:
            restored_map = _restore(data.get("map"), MapClass, "map")

        # Restore armies (pass units_by_id as extra when required)
        restored_army1 = _restore(data.get("army1"), Army, "army1", extra=units_by_id)
        restored_army2 = _restore(data.get("army2"), Army, "army2", extra=units_by_id)

        # Restore generals
        restored_general1 = _restore(data.get("general1"), General, "general1")
        restored_general2 = _restore(data.get("general2"), General, "general2")

        battle = cls(restored_map, restored_army1, restored_general1, restored_army2, restored_general2)
        battle.tick = int(data.get("tick", 0))
        return battle