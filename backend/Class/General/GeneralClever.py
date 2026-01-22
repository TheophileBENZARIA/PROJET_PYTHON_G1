from General import General, _manhattan


class GeneralClever(General):
    """
    A smarter general that uses tactical decision-making:
    - Positions archers behind the melee block until enemies are close
    - Focuses fire on damaged/weak targets to eliminate them quickly
    - Calculates target priority based on damage potential and distance
    - Uses unit type bonuses when selecting targets
    """

    def __init__(self):
        super().__init__("General Clever")
        self.is_deployed = False
        # Cache for max HP lookup (populated on first use)
        self._max_hp_cache:  Dict[str, int] = {}

    def _get_max_hp(self, unit_type: str) -> int:
        """Get the max HP for a unit type, caching the result."""
        if unit_type not in self._max_hp_cache:
            # Default max HP values based on unit types
            defaults = {
                "Knight": 100,
                "Pikeman": 55,
                "Crossbowman":  35,
            }
            self._max_hp_cache[unit_type] = defaults.get(unit_type, 100)
        return self._max_hp_cache[unit_type]

    def _calculate_target_score(self, attacker, target) -> float:
        """
        Calculate target priority score based on:
        - Effective damage (attack + bonus - armor)
        - Distance (closer = higher priority)
        - Focus fire bonus (damaged units get higher priority)
        """
        if target. position is None or attacker.position is None:
            return -float("inf")

        # Calculate effective damage
        try:
            bonus = attacker.compute_bonus(target)
        except Exception:
            bonus = 0

        raw_dmg = getattr(attacker, "attack", 1) + bonus
        effective_dmg = max(1, raw_dmg - getattr(target, "armor", 0))

        # Distance factor
        dist = _manhattan(attacker. position, target.position)

        # Base score:  damage efficiency over distance
        score = effective_dmg / (dist + 1)

        # Focus fire bonus:  prioritize damaged units
        target_type = target. unit_type() if callable(getattr(target, "unit_type", None)) else "Unknown"
        max_hp = self._get_max_hp(target_type)
        current_hp = getattr(target, "hp", max_hp)
        hp_ratio = current_hp / max_hp if max_hp > 0 else 1.0

        # Strongly prioritize units below 50% HP (easier to finish off)
        if hp_ratio < 0.5:
            score *= 1.8
        elif hp_ratio < 0.75:
            score *= 1.3

        # Slight bonus for closer targets (encourages engagement)
        score *= (1.0 + max(0.0, (5 - dist) * 0.05))

        return float(score)

    def _step_towards(self, unit, tx:  int, ty: int, game_map) -> bool:
        """
        Move unit one step towards target position (tx, ty).
        Returns True if movement occurred, False otherwise.
        """
        pos = getattr(unit, "position", None)
        if pos is None:
            return False

        ux, uy = pos
        dx = tx - ux
        dy = ty - uy

        # Already at destination
        if dx == 0 and dy == 0:
            return False

        # Determine primary and alternate movement directions
        if abs(dx) >= abs(dy):
            # Prefer horizontal movement
            primary = (ux + (1 if dx > 0 else -1), uy)
            alternate = (ux, uy + (1 if dy > 0 else -1 if dy < 0 else 0))
        else:
            # Prefer vertical movement
            primary = (ux, uy + (1 if dy > 0 else -1))
            alternate = (ux + (1 if dx > 0 else -1 if dx < 0 else 0), uy)

        width = game_map.width
        height = game_map.height

        # Try primary direction first, then alternate
        for nx, ny in (primary, alternate):
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            tile = game_map.grid[nx][ny]
            if tile.is_empty():
                try:
                    game_map.move_unit(unit, nx, ny)
                    return True
                except Exception:
                    continue

        return False

    def _move_with_pathfinding(self, unit, tx: int, ty: int, game_map) -> bool:
        """
        Move unit towards (tx, ty) using A* pathfinding.
        Returns True if movement occurred.
        """
        if unit.position is None:
            return False

        ux, uy = unit.position

        # Already at or near destination
        if abs(ux - tx) + abs(uy - ty) <= 1:
            return False

        try:
            path = find_path(game_map, (ux, uy), (tx, ty))
        except Exception:
            path = []

        if path and len(path) >= 2:
            # Move up to unit's speed along the path
            steps = min(max(1, getattr(unit, "speed", 1)), len(path) - 1)

            # Try each step from furthest to nearest
            for step_idx in range(steps, 0, -1):
                if step_idx < len(path):
                    nx, ny = path[step_idx]
                    if 0 <= nx < game_map.width and 0 <= ny < game_map.height:
                        if game_map.grid[nx][ny]. is_empty():
                            try:
                                game_map.move_unit(unit, nx, ny)
                                return True
                            except Exception:
                                continue

        # Fallback to simple step
        return self._step_towards(unit, tx, ty, game_map)

    def _maneuver_formation(self, army, enemy_army, game_map) -> None:
        """
        Position archers behind the melee block for protection.
        Calculates the center of melee units and positions archers
        on the opposite side from the nearest enemy.
        """
        my_units = army.living_units()
        enemies = enemy_army. living_units()

        if not my_units or not enemies:
            return

        # Separate melee and ranged units
        melee_units = [u for u in my_units if u.unit_type() in ("Knight", "Pikeman")]
        archer_units = [u for u in my_units if u.unit_type() == "Crossbowman"]

        if not melee_units or not archer_units:
            return

        # Calculate center of melee formation
        valid_melee = [u for u in melee_units if u.position is not None]
        if not valid_melee:
            return

        avg_x = sum(u.position[0] for u in valid_melee) / len(valid_melee)
        avg_y = sum(u.position[1] for u in valid_melee) / len(valid_melee)

        # Find closest enemy to the melee center
        def dist_to_center(e):
            if e.position is None:
                return float("inf")
            return (e.position[0] - avg_x) ** 2 + (e.position[1] - avg_y) ** 2

        closest_enemy = min(enemies, key=dist_to_center)
        if closest_enemy.position is None:
            return

        # Calculate direction away from enemy
        dx = closest_enemy.position[0] - avg_x
        dy = closest_enemy.position[1] - avg_y
        mag = (dx * dx + dy * dy) ** 0.5

        if mag == 0:
            return

        # Rally point is 5 tiles behind the melee line (opposite to enemy)
        rally_x = int(avg_x - (dx / mag) * 5)
        rally_y = int(avg_y - (dy / mag) * 5)

        # Clamp to map bounds
        rally_x = max(0, min(game_map.width - 1, rally_x))
        rally_y = max(0, min(game_map.height - 1, rally_y))

        # Move archers towards rally point
        for archer in archer_units:
            if archer.position is None:
                continue

            # If already near rally point, don't move
            if _manhattan(archer.position, (rally_x, rally_y)) <= 2:
                continue

            # Move archer towards rally point
            self._move_with_pathfinding(archer, rally_x, rally_y, game_map)

    def _get_best_target(self, unit, enemies:  List) -> Optional[object]:
        """
        Find the best target for a unit based on tactical scoring.
        """
        best_target = None
        best_score = -float("inf")

        for enemy in enemies:
            if enemy.position is None or not enemy.is_alive():
                continue

            score = self._calculate_target_score(unit, enemy)
            if score > best_score:
                best_score = score
                best_target = enemy

        return best_target

    def issue_orders(self, army, enemy_army, game_map):
        """
        Main order-issuing method called each tick.

        Strategy:
        1. MANEUVER PHASE:  If enemies are far, position archers safely behind melee
        2. ENGAGEMENT PHASE: Select optimal targets using tactical scoring
        3. MOVEMENT:  Move towards best target if not in range
        """
        my_units = army. living_units()
        alive_enemies = enemy_army.living_units()

        if not my_units or not alive_enemies:
            return

        # Calculate minimum distance to any enemy
        min_dist = float("inf")
        for u in my_units:
            if u. position is None:
                continue
            for e in alive_enemies:
                if e.position is None:
                    continue
                d = _manhattan(u.position, e. position)
                if d < min_dist:
                    min_dist = d

        # --- PHASE 1: MANEUVER ---
        # If enemies are still far (distance > 8), position archers behind melee
        if not self.is_deployed and min_dist > 8:
            self._maneuver_formation(army, enemy_army, game_map)
            # Only order melee units to advance; archers stay in formation
            units_to_order = [u for u in my_units if u.unit_type() != "Crossbowman"]
        else:
            # Once deployed or enemies are close, all units engage
            self.is_deployed = True
            units_to_order = my_units

        # --- PHASE 2: TACTICAL TARGETING AND MOVEMENT ---
        for unit in units_to_order:
            if unit.position is None:
                continue

            # Find the best target based on tactical scoring
            best_target = self._get_best_target(unit, alive_enemies)

            if best_target is None:
                continue

            # Calculate distance to target
            dist = _manhattan(unit.position, best_target.position)
            unit_range = getattr(unit, "range", 1)

            # If in attack range, set target (combat handled by battle.update_units)
            if dist <= unit_range:
                try:
                    unit.current_target = best_target
                except Exception:
                    pass
            else:
                # Move towards best target
                tx, ty = best_target.position

                # For ranged units, try to maintain optimal distance
                if unit_range > 1:
                    # Move to get within range but not too close
                    if dist > unit_range:
                        self._move_with_pathfinding(unit, tx, ty, game_map)
                else:
                    # Melee units: close the distance
                    self._move_with_pathfinding(unit, tx, ty, game_map)
