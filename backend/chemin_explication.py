import math
from typing import List, Optional, Tuple
import time
import os

# --- CLASSES DE BASE ---

class Vector: 
    """Représente un vecteur 2D (position ou déplacement)."""
    __slots__ = ('x', 'y')  # Optimisation mémoire
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> 'Vector':
        mag = self.magnitude()
        if mag == 0:
            return Vector(0.0, 0.0)
        return Vector(self.x / mag, self.y / mag)

    def scale(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self) -> str:
        return f"V({self.x:.1f},{self.y:.1f})"


class Unit: 
    """Représente une unité dans la simulation."""
    
    def __init__(self, name: str, x: float, y: float, radius: float, speed: float, is_static: bool = False):
        self.name = name
        self._position_vector = Vector(x, y)
        self.target: Optional[Vector] = None
        self.target_name: Optional[str] = None
        self.radius = radius
        self.speed = speed
        self.is_evading = False
        self.is_static = is_static
        self.last_move = Vector(0.0, 0.0)

    @property
    def position(self) -> Tuple[float, float]:
        return (self._position_vector.x, self._position_vector.y)

    @position.setter
    def position(self, new_pos: Tuple[float, float]):
        self._position_vector.x = new_pos[0]
        self._position_vector.y = new_pos[1]

    def set_target(self, x: float, y: float, name: Optional[str] = None):
        if not self.is_static:
            self.target = Vector(x, y)
            self.target_name = name if name else 'T'
            self.is_evading = False

    def _check_for_obstacles(self, obstacles: List['Unit']) -> Vector:
        """Calcule la force d'évitement (optimisée)."""
        evasion_force = Vector(0.0, 0.0)
        proximity_threshold = self.radius * 6 

        for obstacle in obstacles:
            if obstacle is self:
                continue

            # Calcul optimisé de la distance au carré (évite sqrt inutile)
            dx = obstacle._position_vector.x - self._position_vector.x
            dy = obstacle._position_vector.y - self._position_vector.y
            dist_squared = dx * dx + dy * dy
            
            # Vérification rapide avant calcul de la vraie distance
            if dist_squared < proximity_threshold**2 and dist_squared > 0:
                distance = math.sqrt(dist_squared)
                
                # Direction d'éloignement
                away_x = -dx / distance
                away_y = -dy / distance
                
                strength = 1.0 - distance / proximity_threshold 
                evasion_force.x += away_x * strength
                evasion_force.y += away_y * strength

        return evasion_force

    def update(self, obstacles: List['Unit']):
        """Calcule et applique le mouvement."""
        if self.is_static or not self.target:
            self.last_move = Vector(0.0, 0.0)
            return

        old_position = self._position_vector
        
        # Direction vers la cible
        direction_to_target = (self.target - self._position_vector).normalize()
        movement_vector = direction_to_target.scale(self.speed)

        # Force d'évitement
        evasion_vector = self._check_for_obstacles(obstacles)

        # Combinaison des forces
        if evasion_vector.magnitude() > 0:
            combined_vector = movement_vector.scale(0.5) + evasion_vector.scale(1.5)
            self.is_evading = True
        else:
            combined_vector = movement_vector
            self.is_evading = False

        # Mouvement final
        target_distance = (self.target - self._position_vector).magnitude()
        
        if target_distance > self.speed:
            final_move = combined_vector.normalize().scale(self.speed)
            new_position = self._position_vector + final_move
        else:
            final_move = self.target - self._position_vector
            new_position = self.target
            self.target = None
            self.target_name = None
            
        self._position_vector = new_position
        self.last_move = self._position_vector - old_position
            
    def __str__(self):
        """Affichage compact."""
        pos = f"({self.position[0]:.1f},{self.position[1]:.1f})"
        status = "⚠️" if self.is_evading else ("→" if self.target else "✓")
        return f"{self.name}:{pos} {status}"


class StandaloneSimulation:
    """Gère la simulation avec affichage optimisé."""
    
    def __init__(self, width: int = 50, height: int = 15):
        self.units: List[Unit] = []
        self.steps = 0
        self.width = width
        self.height = height
        self._map_cache = None  # Cache pour la map

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def draw_map(self):
        """Affichage optimisé et compact."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Initialisation rapide de la map
        map_data = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # Placement des éléments
        for unit in self.units:
            x, y = int(round(unit.position[0])), int(round(unit.position[1]))
            
            # Cible
            if unit.target and unit.target_name:
                xt, yt = int(round(unit.target.x)), int(round(unit.target.y))
                if 0 <= yt < self.height and 0 <= xt < self.width:
                    map_data[yt][xt] = unit.target_name[0].lower()
            
            # Unité (écrase la cible)
            if 0 <= y < self.height and 0 <= x < self.width:
                map_data[y][x] = unit.name[0]

        # Affichage compact
        print("┌" + "─" * self.width + "┐")
        for row in map_data:
            print("│" + "".join(row) + "│")
        print("└" + "─" * self.width + "┘")
        
        # Statut condensé
        print(f"\n⏱️  Étape {self.steps}")
        for unit in self.units:
            print(f"  {unit}")

    def run_step(self) -> bool:
        """Fait avancer la simulation d'une étape."""
        self.steps += 1
        
        for unit in self.units:
            unit.update(self.units)

        self.draw_map()
        
        # Arrêt si toutes les unités sont arrivées
        return any(unit.target is not None for unit in self.units if not unit.is_static)


# --- SIMULATION ---

def run_simulation():
    """Lance la simulation optimisée."""
    sim = StandaloneSimulation(width=60, height=18)

    # Création des unités
    player_a = Unit(name="A", x=5.0, y=5.0, radius=1.5, speed=1.0) 
    player_b = Unit(name="B", x=50.0, y=10.0, radius=1.5, speed=0.7)
    wall_static = Unit(name="M", x=30.0, y=9.0, radius=2.0, speed=0.0, is_static=True)

    sim.add_unit(player_a)
    sim.add_unit(player_b)
    sim.add_unit(wall_static)

    # Cibles
    player_a.set_target(x=55.0, y=15.0, name="T1")
    player_b.set_target(x=5.0, y=2.0, name="T2")

    print("\n🎮 SIMULATION DE MOUVEMENT AVEC ÉVITEMENT\n")
    time.sleep(1)

    MAX_STEPS = 100
    animation_delay = 0.15  # Ajustable selon votre préférence

    try:
        while sim.run_step() and sim.steps < MAX_STEPS:
            time.sleep(animation_delay)
    except KeyboardInterrupt:
        print("\n\n⏸️  Simulation interrompue.")

    print(f"\n✅ Simulation terminée après {sim.steps} étapes\n")


if __name__ == "__main__":
    run_simulation()