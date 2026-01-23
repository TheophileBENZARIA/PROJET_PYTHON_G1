from backend.Class.Generals.General import General


class GeneralClever(General):
    """
    A smarter general that uses tactical decision-making:
    - Positions archers behind the melee block until enemies are close
    - Focuses fire on damaged/weak targets to eliminate them quickly
    - Calculates target priority based on damage potential and distance
    - Uses unit type bonuses when selecting targets
    """

    def __init__(self):
        super().__init__()
        self._max_hp_cache: dict[str, int] = {}
        self._is_deployed = False
        self._deployment_threshold = 8

    def getTargets(self, map, otherArmy):
        enemies = otherArmy.living_units()
        my_units = self.army.living_units()

        if not enemies or not my_units:
            return []

        min_distance = self._min_distance(my_units, enemies)
        if not self._is_deployed and min_distance <= self._deployment_threshold:
            self._is_deployed = True

        targets = []
        for unit in my_units:
            if unit.position is None:
                continue

            if not self._is_deployed and self._is_ranged(unit):
                # Hold archers behind melee screen until battle is close.
                continue

            target = self._choose_target(unit, enemies)
            if target is not None:
                targets.append((unit, target))

        return targets

    def _choose_target(self, unit, enemies):
        best = None
        best_score = float("-inf")
        for enemy in enemies:
            if enemy.position is None:
                continue
            score = self._calculate_target_score(unit, enemy)
            if score > best_score:
                best_score = score
                best = enemy
        return best

    def _calculate_target_score(self, attacker, target):
        if attacker.position is None or target.position is None:
            return float("-inf")

        try:
            bonus = attacker.compute_bonus(target)
        except Exception:
            bonus = 0

        raw_damage = getattr(attacker, "attack", 1) + bonus
        effective_damage = max(1, raw_damage - getattr(target, "armor", 0))

        dist = _manhattan(attacker.position, target.position)
        score = effective_damage / (dist + 1)

        target_type = target.unit_type() if callable(getattr(target, "unit_type", None)) else None
        max_hp = self._get_max_hp(target_type)
        hp = getattr(target, "hp", max_hp)
        hp_ratio = hp / max_hp if max_hp else 1

        if hp_ratio < 0.5:
            score *= 1.8
        elif hp_ratio < 0.75:
            score *= 1.3

        score *= (1.0 + max(0, (5 - dist)) * 0.05)
        return score

    def _min_distance(self, units, enemies):
        best = float("inf")
        for unit in units:
            if unit.position is None:
                continue
            for enemy in enemies:
                if enemy.position is None:
                    continue
                dist = _manhattan(unit.position, enemy.position)
                if dist < best:
                    best = dist
        return best

    @staticmethod
    def _is_ranged(unit):
        return getattr(unit, "range", 1) > 1

    def _get_max_hp(self, unit_type):
        defaults = {
            "Knight": 100,
            "Pikeman": 55,
            "Crossbowman": 35,
        }
        if unit_type not in self._max_hp_cache:
            self._max_hp_cache[unit_type] = defaults.get(unit_type, 100)
        return self._max_hp_cache[unit_type]
