# backend/battle.py
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass
from backend.Class.Army import Army
from backend.generals import General
import time
import logging
from collections import deque

logger = logging.getLogger(__name__)

CASTLE_HP_DEFAULT = 300

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

        # append-only ring buffer of recent human-readable events (strings).
        # Terminal UI will read this and display a compact battle log.
        self.event_log = deque(maxlen=200)

        # when True, Battle. update_units avoids printing to stdout (used when a curses display is active)
        self._suppress_stdout = False

        # When a castle is destroyed we set this to the winning owner's name (string) to short-circuit the simulation
        self._victory: Optional[str] = None

    # small helper to record an event (keeps messages concise)
    def add_event(self, msg: str):
        entry = f"[T{self.tick}] {msg}"
        self.event_log.append(entry)
        # also send to logger at info level for diagnostics
        logger.info(entry)
        # If not running with an external display, still print to stdout for convenience
        if not self._suppress_stdout:
            print(entry)

    # --- NEW helper:  Bresenham + LOS check ---
    def _bresenham_line(self, a: Tuple[int, int], b: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return the integer grid cells on a line from a to b (including endpoints).
        Standard Bresenham integer algorithm.
        """
        x0, y0 = a
        x1, y1 = b
        points = []

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy  # err = dx + dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return points

    def _has_line_of_sight(self, attacker_pos: Tuple[int, int], target_pos: Tuple[int, int],
                           attacker_elev: int) -> bool:
        """
        Return True if attacker at attacker_pos (with elevation attacker_elev) can see target_pos.
        LOS is blocked if any intermediate tile (exclusive of endpoints) has:
          - a building (tile.building is not None), or
          - elevation strictly greater than attacker_elev.

        This is a conservative rule that prevents melee attackers from striking targets hidden behind hills.
        """
        # sanity bounds
        ax, ay = attacker_pos
        tx, ty = target_pos
        width = self.map.width
        height = self.map.height

        # obtain integer line points
        line = self._bresenham_line((ax, ay), (tx, ty))

        # check intermediate points only (exclude endpoints)
        for (x, y) in line[1:-1]:
            if not (0 <= x < width and 0 <= y < height):
                # out-of-bounds tile — treat as blocking
                return False
            tile = self.map.grid[x][y]
            # building blocks sight
            if getattr(tile, "building", None) is not None:
                # If the building in the middle is a castle, still blocks LOS
                return False
            # hill higher than the attacker's elevation blocks sight
            try:
                elev = int(getattr(tile, "elevation", 0) or 0)
            except Exception:
                elev = 0
            if elev > attacker_elev:
                return False
        return True

    def _damage_castle(self, castle_tile, attacker) -> Tuple[int, str]:
        """
        Apply damage to castle on castle_tile by attacker Unit.
        Returns (applied_damage, message).
        castle_tile. building is expected to be a dict with keys:  'type'=='castle', 'hp', 'max_hp', 'owner'.
        """
        b = castle_tile.building
        if not isinstance(b, dict) or b.get("type") != "castle":
            return 0, ""
        # compute damage
        try:
            bonus = attacker.compute_bonus(b) if hasattr(attacker, "compute_bonus") else 0
        except Exception:
            bonus = 0
        raw = max(1, (attacker.attack + bonus) - 0)
        # hill bonus if attacker on hill
        hill_bonus = 0
        try:
            ux, uy = attacker.position
            if 0 <= ux < self.map.width and 0 <= uy < self.map.height:
                tile = self.map.grid[ux][uy]
                hill_bonus = int(getattr(tile, "elevation", 0) or 0)
        except Exception:
            hill_bonus = 0
        total = raw + hill_bonus
        # apply to castle
        b["hp"] = max(0, int(b.get("hp", 0) - total))
        attacker.cooldown = attacker.reload_time
        owner = b.get("owner", "Unknown")
        msg = f"{attacker.owner}'s {attacker.unit_type()} damages {owner}'s castle for {total} dmg (castle HP={b['hp']}/{b.get('max_hp', b.get('hp', 0))})"
        self.add_event(msg)
        # if castle destroyed
        if b["hp"] <= 0:
            self.add_event(f"{owner}'s castle has been destroyed!")
            # record victory:  attacker.owner wins
            self._victory = attacker.owner
        return total, msg

    def run(self, delay: float = 0.5, display_callback: Optional[Callable[[Any], None]] = None) -> BattleResult:
        """
        Run the battle until one/both armies are destroyed (no artificial tick cap).
        - delay: seconds to sleep after each tick (set to 0 for headless).
        - display_callback: optional function(game_map) called after update_units each tick to
            update any external display (e.g.  curses). If the callback raises KeyboardInterrupt,
            the battle will stop gracefully.
        Returns:
            BattleResult(winner, surviving_units, ticks)
        """
        # when a display callback is provided we suppress normal stdout prints to avoid breaking curses
        self._suppress_stdout = bool(display_callback)

        # Loop until at least one army is empty or a castle is destroyed
        while (self.army1.living_units() and self.army2.living_units()) and (self._victory is None):
            self.tick += 1
            # logger.debug("=== Tick %d starting ===", self. tick)
            if not self._suppress_stdout:
                print(f"\n--- Tick {self.tick} ---")

            # Issue orders (set targets / high-level orders)
            self.general1.issue_orders(self.army1, self.army2, self.map)
            self.general2.issue_orders(self.army2, self.army1, self.map)


            # update game state (movement, attacks, cooldowns, death cleanup)
            self.update_units()


            # If provided, call the display callback so an external UI can update.
            if display_callback:
                try:
                    display_callback(self.map)
                except KeyboardInterrupt:
                    # allow the callback to request an early exit
                    logger.info("Display requested exit; ending battle early")
                    break
                except Exception:
                    logger.exception("Display callback raised an exception; continuing without it")

            # If no external display, show debug textual info to stdout
            if not self._suppress_stdout:
                self.debug_print_tick()

            if delay and delay > 0:
                time.sleep(delay)  # slow down so you can see updates

        # restore printing behavior
        self._suppress_stdout = False

        # determine winner
        if self._victory is not None:
            winner = self._victory
            print(f"\n {winner} wins by destroying the enemy castle after {self.tick} ticks! \n")
        else:
            army1_alive = bool(self.army1.living_units())
            army2_alive = bool(self.army2.living_units())

            if army1_alive and not army2_alive:
                winner = self.general1.name
                print(f"\n{winner} wins after {self.tick} ticks!\n")
            elif army2_alive and not army1_alive:
                winner = self.general2.name
                print(f"\n{winner} wins after {self.tick} ticks!\n")
            else:
                winner = "Draw"
                print(f"\nThe battle ends in a draw after {self.tick} ticks!\n")

        # collect surviving units as serializable dicts
        surviving_units: Dict[str, List[Dict[str, Any]]] = {}
        for army in (self.army1, self.army2):
            surviving_units[army.owner] = [u.to_dict() for u in army.living_units()]

        return BattleResult(winner=winner, surviving_units=surviving_units, ticks=self.tick)

    def debug_print_tick(self):
        """Print per-tick unit HP/position to debug death/damage logic."""
        print(f"--- Tick {self.tick} ---")
        for side_name, army in (("Player1", getattr(self, "army1", None)), ("Player2", getattr(self, "army2", None))):
            if army is None:
                print(f"{side_name}:  <no army>")
                continue
            units = getattr(army, "units", None) or getattr(army, "soldiers", None) or []
            print(f"{side_name} units: {len(units)}")
            for u in units:
                uid = getattr(u, "id", getattr(u, "uid", None)) or getattr(u, "__class__", type(u)).__name__
                pos = getattr(u, "position", None)
                hp = getattr(u, "hp", getattr(u, "health", getattr(u, "hitpoints", None)))
                alive = getattr(u, "is_alive", None)
                alive_str = alive() if callable(alive) else (hp is None or hp > 0)
                # Show threat count for debugging
                threat_count = len(getattr(u, "threat_memory", {}))
                print(f"  {uid} pos={pos} hp={hp} alive={alive_str} threats={threat_count}")
        # show castle HP status for debugging
        for y in range(self.map.height):
            for x in range(self.map.width):
                tile = self.map.grid[x][y]
                b = getattr(tile, "building", None)
                if isinstance(b, dict) and b.get("type") == "castle":
                    print(f"  Castle {b.get('owner')} at ({x},{y}) HP:  {b.get('hp')}/{b.get('max_hp')}")
        print("---------------------")

    def update_units(self):
        """Handle per-tick updates:  cooldowns, movement (per-unit AI), then combat including castles."""
        # Cooldown management
        for unit in self.army1.living_units() + self.army2.living_units():
            if unit.cooldown > 0:
                unit.cooldown -= 1

        # Per-unit movement (handled by generals or per-unit AI)
        all_units = self.army1.living_units() + self.army2.living_units()
        for unit in list(all_units):  # list() to avoid mutation issues
            try:
                # some units may implement perform_movement(game_map)
                if unit.is_alive() and unit.position is not None and hasattr(unit, "perform_movement"):
                    unit.perform_movement(self.map)
            except Exception:
                logger.exception("Error during movement for unit %s", getattr(unit, "id", "<unknown>"))
                continue

        # Handle melee/ranged combat (including castle targets)
        all_units = self.army1.living_units() + self.army2.living_units()

        for unit in all_units:
            if not unit.is_alive() or unit.position is None:
                continue

            # Determine the opposing army
            enemy_army = self.army2 if unit.owner == self.army1.owner else self.army1
            enemies = enemy_army.living_units()
            # find enemy castles (tiles)
            enemy_castles = []
            for x in range(self.map.width):
                for y in range(self.map.height):
                    tile = self.map.grid[x][y]
                    b = getattr(tile, "building", None)
                    if isinstance(b, dict) and b.get("type") == "castle" and b.get("owner") == enemy_army.owner:
                        enemy_castles.append((x, y, tile))

            if not enemies and not enemy_castles:
                continue

            # Find all enemies within attack range (units and castles)
            enemies_in_range = []
            try:
                ux, uy = unit.position
                unit_elev = int(getattr(self.map.grid[ux][uy], "elevation", 0) or 0) if (
                            0 <= ux < self.map.width and 0 <= uy < self.map.height) else 0
            except Exception:
                ux = uy = None
                unit_elev = 0

            # units first
            for e in enemies:
                if not e.position:
                    continue
                # distance check (Manhattan)
                if self.distance(unit, e) > unit.range:
                    continue

                # determine target elevation
                try:
                    tx, ty = e.position
                    target_elev = int(getattr(self.map.grid[tx][ty], "elevation", 0) or 0) if (
                                0 <= tx < self.map.width and 0 <= ty < self.map.height) else 0
                except Exception:
                    target_elev = 0

                # If attacker is melee (range <= 1), they cannot attack targets that are strictly higher (uphill).
                if (unit.range <= 1) and (target_elev > unit_elev):
                    continue

                # For melee, also require line-of-sight (no taller hill/building between)
                if unit.range <= 1:
                    try:
                        if not self._has_line_of_sight((ux, uy), (tx, ty), unit_elev):
                            # melee attacker cannot see the target because of intervening hill/building
                            # (don't include as in-range)
                            continue
                    except Exception:
                        # on error be conservative and skip target
                        continue

                enemies_in_range.append(e)

            # castles
            for (cx, cy, c_tile) in enemy_castles:
                # Manhattan distance
                dist = abs(ux - cx) + abs(uy - cy)
                if dist > unit.range:
                    continue
                # hill/LOS restrictions for melee same as unit
                if unit.range <= 1:
                    try:
                        if not self._has_line_of_sight((ux, uy), (cx, cy), unit_elev):
                            continue
                    except Exception:
                        continue
                # represent castle by tuple ('castle', cx, cy, tile)
                enemies_in_range.append(("castle", cx, cy, c_tile))

            if not enemies_in_range:
                continue

            # helper for choosing nearest (works for unit or castle tuple)
            def _dist_to_obj(obj):
                if isinstance(obj, tuple) and obj and obj[0] == "castle":
                    _, cx, cy, _ = obj
                    return abs(ux - cx) + abs(uy - cy)
                else:
                    return self.distance(unit, obj)

            # Choose the nearest enemy to attack
            target = min(enemies_in_range, key=_dist_to_obj)

            # Attack if cooldown allows
            if unit.can_attack():
                # Store attacker position BEFORE attack for threat tracking
                attacker_pos = tuple(unit.position) if unit.position else None

                if isinstance(target, tuple) and target and target[0] == "castle":
                    # castle attack
                    _, cx, cy, c_tile = target
                    applied, msg = self._damage_castle(c_tile, unit)
                    # if castle destroyed, the _damage_castle already set self._victory
                else:
                    # pass game_map to attack_unit so units (e.g.  Crossbowman) can use tile info (hills)
                    res = unit.attack_unit(target, game_map=self.map)
                    if isinstance(res, tuple):
                        applied, msg = res
                    else:
                        applied, msg = res, None

                    # THREAT TRACKING:  Register the attacker in the target's threat memory
                    # This happens regardless of damage (even on miss, target knows where shot came from)
                    if attacker_pos is not None and hasattr(target, 'register_threat'):
                        target.register_threat(unit, attacker_pos, self.tick)
                        logger.debug("Threat registered:  %s's %s attacked %s's %s from %s",
                                     unit.owner, unit.unit_type(), target.owner, target.unit_type(), attacker_pos)

                    # Build an event message:  prefer explicit msg from unit, otherwise synthesize
                    if msg:
                        self.add_event(msg)
                    else:
                        self.add_event(
                            f"{unit.owner}'s {unit.unit_type()} attacks {target.owner}'s {target.unit_type()} for {applied} dmg (HP={target.hp})")

            # If the target dies, remove it immediately and log
            if not (isinstance(target, tuple) and target and target[0] == "castle"):
                # normal unit death handling
                if not target.is_alive():
                    self.remove_unit(target)
                    self.add_event(f"{target.owner}'s {target.unit_type()} has died!")

                    # Clear the dead unit from all threat memories
                    for u in self.army1.living_units() + self.army2.living_units():
                        if hasattr(u, 'clear_threat'):
                            u.clear_threat(target.id)

            # If castle destroyed, we can stop further processing this tick (victory flag set)
            if self._victory is not None:
                return

        # Defensive cleanup (in case of simultaneous deaths)
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

    def to_dict(self) -> dict:
        """
        Return a JSON-serializable representation of this Battle.
        Delegates to . to_dict() on sub-objects (map, armies, generals) if available.
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

    @classmethod
    def from_dict(cls, data: dict):
        """
        Recreate a Battle from a dict produced by Battle.to_dict().
        Handles Army. from_dict signatures that require a `units_by_id` dict by
        attempting to reconstruct units first using backend.units. Unit.from_dict.
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
                # Fallback:  try calling with single arg
                try:
                    return cls_type.from_dict(obj_data)
                except Exception as e:
                    raise TypeError(
                        f"Cannot restore {label}:  failed to call {cls_type.__name__}. from_dict -> {e}") from e

        # import component classes
        try:
            from backend.Class.army import Army
        except Exception as e:
            raise TypeError(f"Cannot restore armies: failed to import backend.army -> {e}") from e

        try:
            from backend.generals import General
        except Exception as e:
            raise TypeError(f"Cannot restore generals: failed to import backend.generals -> {e}") from e

        MapClass = None
        try:
            from backend.Class.map import Map as MapClass
        except Exception:
            try:
                from backend.Class.map import GameMap as MapClass
            except Exception:
                MapClass = None

        # Prepare units_by_id mapping if Army.from_dict expects it.
        units_by_id = {}
        # Try to load Unit. from_dict if present
        UnitClass = None
        try:
            from backend.Class.Units import Unit as UnitClass
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

        # restore map (require Map. from_dict if a map was saved
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