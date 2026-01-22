from General import General, _manhattan

class CaptainBraindead(General):
    """
    A reactive general that doesn't proactively seek enemies, but units will
    retaliate against attackers they remember (threat memory system).
    Units pursue enemies that have attacked them, even ranged attackers.
    """

    def __init__(self):
        super().__init__("Captain Braindead")

    def issue_orders(self, army, enemy_army, game_map):
        """
        For each unit, check if they have a threat in memory (someone who attacked them).
        If so, move toward that threat to retaliate.
        """
        for unit in army.living_units():
            if unit.position is None:
                continue

            # Check for priority threat (most recent attacker)
            threat = unit.get_priority_threat()

            if threat is not None and threat. is_alive() and threat.position is not None:
                # Unit has been attacked, pursue the attacker
                self._move_toward_threat(unit, threat, game_map)

    def _move_toward_threat(self, unit, threat, game_map):
        """
        Move unit toward the attacker using pathfinding.
        """
        if unit.position is None or threat.position is None:
            return

        ux, uy = unit.position
        tx, ty = threat. position

        # Calculate distance
        dist = abs(ux - tx) + abs(uy - ty)

        # If already in attack range, don't need to move
        if dist <= unit.range:
            return

        # Use A* to find a path
        try:
            path = find_path(game_map, (ux, uy), (tx, ty))
        except Exception:
            path = []

        if path and len(path) >= 2:
            steps = min(max(1, getattr(unit, "speed", 1)), len(path) - 1)
            next_pos = path[steps]
            nx, ny = next_pos

            if 0 <= nx < game_map. width and 0 <= ny < game_map.height:
                tile = game_map. grid[nx][ny]
                if tile. is_empty():
                    game_map.move_unit(unit, nx, ny)
                    return
                else:
                    for alt in path[1:steps]:
                        ax, ay = alt
                        if 0 <= ax < game_map.width and 0 <= ay < game_map. height:
                            if game_map.grid[ax][ay]. is_empty():
                                game_map.move_unit(unit, ax, ay)
                                return

        # Fallback:  greedy neighbor movement toward threat
        self._greedy_move_toward(unit, tx, ty, game_map)

    def _greedy_move_toward(self, unit, tx:  int, ty: int, game_map):
        """Fallback greedy movement when pathfinding fails."""
        ux, uy = unit.position

        dx = 1 if tx > ux else (-1 if tx < ux else 0)
        dy = 1 if ty > uy else (-1 if ty < uy else 0)

        candidates = []
        if dx != 0 or dy != 0:
            candidates.append((ux + dx, uy + dy))
        if dx != 0:
            candidates.append((ux + dx, uy))
        if dy != 0:
            candidates.append((ux, uy + dy))
        if dx != 0 and dy != 0:
            candidates.append((ux + dx, uy - dy))
            candidates.append((ux - dx, uy + dy))
        candidates.extend([(ux + 1, uy), (ux - 1, uy), (ux, uy + 1), (ux, uy - 1)])

        for new_x, new_y in candidates:
            if not (0 <= new_x < game_map.width and 0 <= new_y < game_map. height):
                continue
            tile = game_map. grid[new_x][new_y]
            if tile. building is not None:
                continue
            if tile. is_empty():
                game_map. move_unit(unit, new_x, new_y)
                return
