# backend/pathfinding.py
"""
A* pathfinder optimisé pour Map/Tile.
API:
    find_path(game_map, start, goal, max_nodes=20000) -> List[(x,y)] or []
Notes:
- Tiles avec building != None : impassables
- Tiles avec unit != None : impassables sauf si c'est la case goal
- Heuristique Manhattan (déplacement en grille)
- Retourne une liste de coordonnées de start à goal (inclus)
"""
from heapq import heappush, heappop
from typing import List, Tuple, Dict

# Constantes pré-calculées pour les voisins (évite les yield/generator)
NEIGHBORS_OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Distance Manhattan entre deux points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(
    game_map, 
    start: Tuple[int, int], 
    goal: Tuple[int, int], 
    max_nodes: int = 20000
) -> List[Tuple[int, int]]:
    """
    A* pathfinding sur la Map fournie.
    Retourne une liste de (x,y) de start à goal (inclus) ou [] si aucun chemin.
    
    Optimisations:
    - Utilisation d'un set pour closed (O(1) lookup)
    - Pas de dictionnaire fscore séparé (non nécessaire)
    - Vérification early exit pour gscore
    - Accès direct aux attributs sans getattr
    - Neighbors précalculés
    """
    if start == goal:
        return [start]
    
    width = game_map.width
    height = game_map.height
    grid = game_map.grid
    
    # Vérification rapide des limites
    gx, gy = goal
    if not (0 <= gx < width and 0 <= gy < height):
        return []
    
    # Structures A*
    open_heap: List[Tuple[int, Tuple[int, int]]] = []
    gscore: Dict[Tuple[int, int], int] = {start: 0}
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    closed = set()
    
    # Initialisation
    h_start = manhattan(start, goal)
    heappush(open_heap, (h_start, start))
    
    visited_count = 0
    
    while open_heap and visited_count < max_nodes:
        f_current, current = heappop(open_heap)
        
        # Si ce nœud a déjà été visité avec un meilleur score, skip
        current_g = gscore.get(current, float('inf'))
        if f_current > current_g + manhattan(current, goal):
            continue
        
        if current == goal:
            # Reconstruction du chemin
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
        
        if current in closed:
            continue
            
        closed.add(current)
        visited_count += 1
        
        cx, cy = current
        
        # Exploration des voisins (version optimisée)
        for dx, dy in NEIGHBORS_OFFSETS:
            nx, ny = cx + dx, cy + dy
            
            # Vérification des limites
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            
            neighbor = (nx, ny)
            
            # Skip si déjà visité
            if neighbor in closed:
                continue
            
            # Accès direct au tile (évite getattr)
            tile = grid[nx][ny]
            
            # Vérification building
            if tile.building is not None:
                continue
            
            # Vérification unité (sauf si c'est le goal)
            if neighbor != goal and tile.unit is not None:
                continue
            
            # Calcul du nouveau g-score
            tentative_g = current_g + 1
            
            # Early exit si ce chemin n'est pas meilleur
            if tentative_g >= gscore.get(neighbor, float('inf')):
                continue
            
            # Mise à jour du meilleur chemin vers ce voisin
            came_from[neighbor] = current
            gscore[neighbor] = tentative_g
            
            # Calcul f = g + h et ajout à la heap
            f = tentative_g + manhattan(neighbor, goal)
            heappush(open_heap, (f, neighbor))
    
    # Aucun chemin trouvé
    return []