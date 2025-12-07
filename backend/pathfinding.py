# backend/pathfinding.py
"""
A small A* pathfinder adapted to the project's Map/Tile layout.

API:
    find_path(game_map, start, goal, max_nodes=20000) -> List[(x,y)] or [] if no path

Notes:
- Treats tiles with tile.building != None as impassable.
- Treats tiles with tile.unit != None as impassable except for the goal tile.
- Uses Manhattan distance heuristic (grid-based movement).
- Returns a list of coordinates from start to goal inclusive. If start == goal returns [start].
"""
from heapq import heappush, heappop
from typing import List, Tuple, Optional, Set, Dict

def manhattan(a: Tuple[int,int], b: Tuple[int,int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors4(x: int, y: int):
    yield (x+1, y)
    yield (x-1, y)
    yield (x, y+1)
    yield (x, y-1)

def find_path(game_map, start: Tuple[int,int], goal: Tuple[int,int], max_nodes: int = 20000) -> List[Tuple[int,int]]:
    """
    A* pathfinding on the provided Map.
    start and goal are (x,y) tuples. Returns a list of (x,y) from start to goal inclusive
    or an empty list if no path found within max_nodes expansions.
    """
    if start == goal:
        return [start]

    width = game_map.width
    height = game_map.height

    def in_bounds(p):
        x, y = p
        return 0 <= x < width and 0 <= y < height

    # quick check: goal must be in bounds
    if not in_bounds(goal):
        return []

    # A* structures
    open_heap: List[Tuple[int, Tuple[int,int]]] = []
    gscore: Dict[Tuple[int,int], int] = {start: 0}
    fscore: Dict[Tuple[int,int], int] = {start: manhattan(start, goal)}
    came_from: Dict[Tuple[int,int], Tuple[int,int]] = {}

    heappush(open_heap, (fscore[start], start))
    visited_count = 0
    closed: Set[Tuple[int,int]] = set()

    while open_heap and visited_count < max_nodes:
        _, current = heappop(open_heap)
        visited_count += 1

        if current == goal:
            # reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        closed.add(current)

        cx, cy = current
        for nx, ny in neighbors4(cx, cy):
            neighbor = (nx, ny)
            if not in_bounds(neighbor):
                continue

            if neighbor in closed:
                continue

            # impassable if building present
            tile = game_map.grid[nx][ny]
            if getattr(tile, "building", None) is not None:
                continue

            # tile occupied by some unit: allow it only if it's the goal tile
            if neighbor != goal and getattr(tile, "unit", None) is not None:
                continue

            tentative_g = gscore[current] + 1
            if tentative_g < gscore.get(neighbor, 1_000_000):
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g
                f = tentative_g + manhattan(neighbor, goal)
                f_prev = fscore.get(neighbor)
                fscore[neighbor] = f
                # push to heap (we don't attempt to remove duplicates; check gscore when popped)
                heappush(open_heap, (f, neighbor))

    # no path found
    return []