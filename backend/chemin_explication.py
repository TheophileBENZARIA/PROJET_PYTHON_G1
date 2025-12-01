# File: `pathfinding_standalone.py`
# python
import math
from typing import List, Optional, Tuple

# --- CLASSES DE BASE (Vector et Unit) ---

class Vector: 
    """Représente un vecteur 2D (position ou déplacement)."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Soustraction de vecteurs."""
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        """Addition de vecteurs."""
        return Vector(self.x + other.x, self.y + other.y)

    def magnitude(self) -> float:
        """Magnitude (longueur) du vecteur."""
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> 'Vector':
        """Normalise le vecteur (le rend unitaire)."""
        mag = self.magnitude()
        if mag == 0:
            return Vector(0.0, 0.0)
        return Vector(self.x / mag, self.y / mag)

    def scale(self, scalar: float) -> 'Vector':
        """Multiplie le vecteur par un scalaire."""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self) -> str:
        return f"V({self.x:.2f}, {self.y:.2f})"


class Unit: 
    """Représente une unité dans la simulation de mouvement continu."""
    
    # Pour simuler les unités de votre jeu, j'utilise un tuple de (x, y) pour la position
    # mais le Vector sera utilisé en interne pour le mouvement flottant.
    
    def __init__(self, name: str, x: float, y: float, radius: float, speed: float, is_static: bool = False):
        self.name = name
        # Stocke la position en Vector (flottant) pour le pathfinding
        self._position_vector = Vector(x, y)
        self.target: Optional[Vector] = None
        self.target_name: Optional[str] = None
        self.radius = radius        # Rayon d'influence (pour l'évitement)
        self.speed = speed          # Vitesse de déplacement (distance max par tick)
        self.is_evading = False
        self.is_static = is_static
        self.last_move = Vector(0.0, 0.0)

    @property
    def position(self) -> Tuple[float, float]:
        """Retourne la position comme un tuple (x, y) de flottants."""
        return (self._position_vector.x, self._position_vector.y)

    @position.setter
    def position(self, new_pos: Tuple[float, float]):
        """Définit la position à partir d'un tuple (x, y) de flottants."""
        self._position_vector.x = new_pos[0]
        self._position_vector.y = new_pos[1]

    def set_target(self, x: float, y: float, name: Optional[str] = None):
        """Définit la cible de l'unité."""
        if not self.is_static:
            self.target = Vector(x, y)
            self.target_name = name if name else 'T'
            self.is_evading = False

    def _check_for_obstacles(self, obstacles: List['Unit']) -> Vector:
        """Calcule la force d'évitement à partir des autres unités."""
        evasion_force = Vector(0.0, 0.0)
        # 6 fois le rayon pour définir la zone de réaction à l'évitement
        proximity_threshold = self.radius * 6 

        for obstacle in obstacles:
            if obstacle is self:
                continue

            distance = (obstacle._position_vector - self._position_vector).magnitude()
            
            if distance < proximity_threshold and distance > 0:
                away_from_obstacle = (self._position_vector - obstacle._position_vector).normalize()
                # Facteur qui augmente plus l'obstacle est proche (1 à 0)
                strength = 1.0 - distance / proximity_threshold 
                evasion_force = evasion_force + away_from_obstacle.scale(strength)

        return evasion_force

    def update(self, obstacles: List['Unit']):
        """
        Calcule et applique le mouvement pour un 'tick' de simulation.
        Nécessite la liste de toutes les unités (y compris elle-même) comme obstacles.
        """
        if self.is_static:
            self.last_move = Vector(0.0, 0.0)
            return

        old_position = self._position_vector
        
        if not self.target:
            self.last_move = Vector(0.0, 0.0)
            return

        # 1. Calcul de la direction vers la cible
        direction_to_target = (self.target - self._position_vector).normalize()
        movement_vector = direction_to_target.scale(self.speed)

        # 2. Calcul de la force d'évitement
        evasion_vector = self._check_for_obstacles(obstacles)

        # 3. Combinaison des forces
        if evasion_vector.magnitude() > 0:
            # Combinaison : 0.5 vers la cible, 1.5 pour l'évitement (favorise l'évitement)
            combined_vector = movement_vector.scale(0.5) + evasion_vector.scale(1.5)
            self.is_evading = True
        else:
            combined_vector = movement_vector
            # Si nous revenons à la trajectoire, on désactive l'évitement
            if self.is_evading and (self.target - self._position_vector).magnitude() > self.speed * 2:
                 self.is_evading = False

        # 4. Mouvement final
        target_distance = (self.target - self._position_vector).magnitude()
        
        if target_distance > self.speed:
            # Se déplace d'une longueur 'speed' dans la direction combinée
            final_move = combined_vector.normalize().scale(self.speed)
            new_position = self._position_vector + final_move
        else:
            # Arrivé à la cible, se déplace exactement à la position cible
            final_move = self.target - self._position_vector
            new_position = self.target
            self.target = None
            self.target_name = None
            
        self._position_vector = new_position
        self.last_move = self._position_vector - old_position
            
    def __str__(self):
        """Affichage du statut de l'unité."""
        pos = f"({self.position[0]:.2f}, {self.position[1]:.2f})"
        status = "**ÉVITE**" if self.is_evading else ("Mouvement" if self.target else "Au repos")
        move = f"-> dx:{self.last_move.x:.2f}, dy:{self.last_move.y:.2f}"
        return f"[{self.name}] {pos} - {status} {move}"


# --- EXEMPLE DE SIMULATION HORS-MAP (pour tester la logique) ---
# Ce bloc simule l'environnement "sans Map"
import time
import os

class StandaloneSimulation:
    def __init__(self, width: int = 50, height: int = 15):
        self.units: List[Unit] = []
        self.steps = 0
        self.width = width # Garde les dimensions pour l'affichage uniquement
        self.height = height

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def draw_map(self):
        """Dessine une carte simple en terminal pour visualisation."""
        os.system('cls' if os.name == 'nt' else 'clear')
        map_data = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        targets_to_draw = {}
        units_to_draw = {}

        # 1. Enregistrer les positions (arrondies)
        for unit in self.units:
            x_pos, y_pos = unit.position
            x_grid, y_grid = int(round(x_pos)), int(round(y_pos))
            
            if 0 <= y_grid < self.height and 0 <= x_grid < self.width:
                units_to_draw[(x_grid, y_grid)] = unit.name[0]

            if unit.target and unit.target_name:
                xt, yt = unit.target.x, unit.target.y
                x_target, y_target = int(round(xt)), int(round(yt))
                if 0 <= y_target < self.height and 0 <= x_target < self.width:
                    targets_to_draw[(x_target, y_target)] = unit.target_name

        # 2. Placer les symboles
        for (x, y), symbol in targets_to_draw.items():
            map_data[y][x] = symbol

        for (x, y), symbol in units_to_draw.items():
            # Les unités écrasent les cibles
            map_data[y][x] = symbol 

        # 3. Afficher la carte
        print(" " + "=" * self.width)
        for row in map_data:
            print("|" + "".join(row) + "|")
        print("=" * (self.width + 2))
        
        # 4. Afficher le statut
        print(f"\n--- Étape {self.steps} (Flottant) ---")
        for unit in self.units:
            print(unit)

    def run_step(self) -> bool:
        self.steps += 1
        
        for unit in self.units:
            # Passe la liste complète des unités comme obstacles
            unit.update(self.units) 

        self.draw_map()
        
        # Arrêt si toutes les unités ont atteint leur cible
        if all(unit.target is None for unit in self.units if not unit.is_static):
            return False
        return True

# --- DÉMARRAGE DE LA SIMULATION STANDALONE ---

sim = StandaloneSimulation(width=60, height=18)

# Joueur Mobile Principal (A)
player_a = Unit(name="A", x=5.0, y=5.0, radius=1.5, speed=1.0) 

# Obstacle Mobile (B)
player_b = Unit(name="B", x=50.0, y=10.0, radius=1.5, speed=0.7)

# "Mur" Statique (représenté par une unité statique)
wall_static = Unit(name="M", x=30.0, y=9.0, radius=2.0, speed=0.0, is_static=True)

sim.add_unit(player_a)
sim.add_unit(player_b)
sim.add_unit(wall_static) 

player_a.set_target(x=55.0, y=15.0, name="T1") 
player_b.set_target(x=5.0, y=2.0, name="T2") 

print("\n*** DÉBUT DE LA SIMULATION SANS MAP (A doit éviter B et M) ***")

MAX_STEPS = 100
current_step = 0
animation_delay = 0.1

try:
    while sim.run_step() and current_step < MAX_STEPS:
        current_step = sim.steps
        time.sleep(animation_delay)
except KeyboardInterrupt:
    print("\nSimulation interrompue par l'utilisateur.")

print(f"\n*** FIN DE LA SIMULATION après {current_step} étapes ***")