import math
# On importe 'math' pour pouvoir utiliser la racine carrée (sqrt) et la puissance (x**2)
from typing import List, Optional, Tuple
# 'typing' nous aide à dire quel type de données on attend (liste, nombre, etc.)

# --- CLASSES DE BASE (Vector et Unit) ---

class Vector: 
    """Représente un vecteur 2D (position ou déplacement)."""
    # C'est notre objet pour gérer les coordonnées (x, y) !
    def __init__(self, x: float, y: float):
        # Quand on crée un vecteur, on lui donne une coordonnée X et une Y.
        self.x = x
        self.y = y

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Soustraction de vecteurs (ex: Position Cible - Position Actuelle = Vecteur de Déplacement)."""
        # On soustrait les X ensemble et les Y ensemble pour obtenir un nouveau Vector.
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        """Addition de vecteurs (ex: Position Actuelle + Vecteur de Mouvement = Nouvelle Position)."""
        # On additionne les X ensemble et les Y ensemble.
        return Vector(self.x + other.x, self.y + other.y)

    def magnitude(self) -> float:
        """Magnitude (longueur) du vecteur. C'est la distance réelle (Pythagore)."""
        # Formule de la distance : racine carrée de (x au carré + y au carré)
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> 'Vector':
        """Normalise le vecteur (le rend unitaire). Longueur = 1. Donne la direction pure."""
        mag = self.magnitude()
        if mag == 0:
            # Si le vecteur est (0, 0), on ne peut pas le diviser, on retourne (0, 0).
            return Vector(0.0, 0.0)
        # On divise chaque composante (x et y) par la longueur totale (magnitude).
        return Vector(self.x / mag, self.y / mag)

    def scale(self, scalar: float) -> 'Vector':
        """Multiplie le vecteur par un scalaire (un nombre). Utilisé pour la vitesse."""
        # On multiplie X et Y par le nombre 'scalar'.
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self) -> str:
        # Comment afficher le vecteur quand on l'imprime.
        return f"V({self.x:.2f}, {self.y:.2f})"


class Unit: 
    """Représente une unité dans la simulation de mouvement continu (ex: un joueur)."""
    
    def __init__(self, name: str, x: float, y: float, radius: float, speed: float, is_static: bool = False):
        self.name = name # Nom pour l'affichage (ex: "A")
        # Position réelle (stockée comme un Vector pour faire les calculs)
        self._position_vector = Vector(x, y)
        self.target: Optional[Vector] = None # Où l'unité veut aller (sa cible)
        self.target_name: Optional[str] = None # Nom de la cible pour l'affichage
        self.radius = radius        # Rayon de l'unité (pour éviter de se cogner)
        self.speed = speed          # Vitesse maximale par 'tick' de simulation
        self.is_evading = False     # Est-ce que l'unité est en train d'éviter un obstacle ?
        self.is_static = is_static  # Est-ce que cette unité est un mur (ne bouge pas) ?
        self.last_move = Vector(0.0, 0.0) # Le déplacement fait au dernier tick

    @property
    def position(self) -> Tuple[float, float]:
        """Retourne la position comme un tuple (x, y). Utile pour l'affichage."""
        return (self._position_vector.x, self._position_vector.y)

    @position.setter
    def position(self, new_pos: Tuple[float, float]):
        """Définit la position à partir d'un tuple (x, y) de flottants."""
        self._position_vector.x = new_pos[0]
        self._position_vector.y = new_pos[1]

    def set_target(self, x: float, y: float, name: Optional[str] = None):
        """Définit la cible de l'unité si elle n'est pas statique."""
        if not self.is_static:
            self.target = Vector(x, y)
            self.target_name = name if name else 'T'
            self.is_evading = False # On arrête d'éviter si on a une nouvelle cible

    def _check_for_obstacles(self, obstacles: List['Unit']) -> Vector:
        """Calcule la force d'évitement à partir des autres unités (le vecteur de 'poussée')."""
        evasion_force = Vector(0.0, 0.0)
        # La zone de danger : 6 fois le rayon. Si un obstacle est dans cette zone, on réagit.
        proximity_threshold = self.radius * 6 

        for obstacle in obstacles:
            if obstacle is self:
                continue # Ne pas se considérer comme un obstacle soi-même

            # Calcul de la distance entre cette unité et l'obstacle (magnitude du vecteur différence)
            distance = (obstacle._position_vector - self._position_vector).magnitude()
            
            if distance < proximity_threshold and distance > 0:
                # Calcul du vecteur qui va de l'obstacle vers NOUS. C'est la direction pour s'enfuir !
                away_from_obstacle = (self._position_vector - obstacle._position_vector).normalize()
                
                # 'strength' : Plus l'obstacle est PRÈS, plus cette valeur est GRANDE (entre 0 et 1)
                strength = 1.0 - distance / proximity_threshold 
                
                # On ajoute une force d'évitement (direction d'éloignement * force)
                evasion_force = evasion_force + away_from_obstacle.scale(strength)

        return evasion_force

    def update(self, obstacles: List['Unit']):
        """
        Calcule et applique le mouvement pour un 'tick' de simulation.
        C'est ici que l'unité décide où aller.
        """
        if self.is_static:
            self.last_move = Vector(0.0, 0.0)
            return # Les murs ne bougent pas

        old_position = self._position_vector
        
        if not self.target:
            self.last_move = Vector(0.0, 0.0)
            return # Rien à faire si on n'a pas de cible

        # 1. Calcul de la direction vers la cible
        # On calcule le vecteur de déplacement vers la cible, puis on le normalise (direction pure).
        direction_to_target = (self.target - self._position_vector).normalize()
        # On multiplie cette direction pure par notre vitesse max (le mouvement 'idéal').
        movement_vector = direction_to_target.scale(self.speed)

        # 2. Calcul de la force d'évitement
        evasion_vector = self._check_for_obstacles(obstacles)

        # 3. Combinaison des forces
        if evasion_vector.magnitude() > 0:
            # On combine la force d'avancement (un peu) et la force d'évitement (beaucoup)
            combined_vector = movement_vector.scale(0.5) + evasion_vector.scale(1.5)
            self.is_evading = True
        else:
            # Si aucun obstacle n'est proche, on utilise juste le mouvement vers la cible
            combined_vector = movement_vector
            self.is_evading = False # On est revenu à la normale

        # 4. Mouvement final
        target_distance = (self.target - self._position_vector).magnitude()
        
        if target_distance > self.speed:
            # On se déplace d'une longueur 'speed' dans la direction combinée
            # On normalise d'abord le combined_vector pour obtenir la direction exacte
            final_move = combined_vector.normalize().scale(self.speed)
            new_position = self._position_vector + final_move
        else:
            # On est très près : on va directement à la cible et on s'arrête
            final_move = self.target - self._position_vector
            new_position = self.target
            self.target = None # Plus de cible !
            self.target_name = None
            
        self._position_vector = new_position
        # On enregistre le mouvement réel effectué pour le débogage/l'affichage
        self.last_move = self._position_vector - old_position
            
    def __str__(self):
        """Affichage du statut de l'unité."""
        # Pour imprimer le statut de l'unité à chaque étape
        pos = f"({self.position[0]:.2f}, {self.position[1]:.2f})"
        status = "**ÉVITE**" if self.is_evading else ("Mouvement" if self.target else "Au repos")
        move = f"-> dx:{self.last_move.x:.2f}, dy:{self.last_move.y:.2f}"
        return f"[{self.name}] {pos} - {status} {move}"


# --- EXEMPLE DE SIMULATION HORS-MAP (pour tester la logique) ---

import time
import os

class StandaloneSimulation:
    """Gère l'ensemble des unités et l'affichage (la "carte" en mode texte)."""
    def __init__(self, width: int = 50, height: int = 15):
        self.units: List[Unit] = []
        self.steps = 0
        self.width = width # Largeur de l'écran texte
        self.height = height # Hauteur de l'écran texte

    def add_unit(self, unit: Unit):
        """Ajoute une unité à la simulation."""
        self.units.append(unit)

    def draw_map(self):
        """Dessine une carte simple en terminal pour visualisation."""
        # Commande pour effacer l'écran (pour l'animation)
        os.system('cls' if os.name == 'nt' else 'clear') 
        map_data = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        targets_to_draw = {}
        units_to_draw = {}

        # 1. Enregistrer les positions des unités et des cibles (en les arrondissant pour la grille)
        for unit in self.units:
            x_pos, y_pos = unit.position
            x_grid, y_grid = int(round(x_pos)), int(round(y_pos))
            
            # Si l'unité est dans les limites de l'écran, on l'enregistre
            if 0 <= y_grid < self.height and 0 <= x_grid < self.width:
                units_to_draw[(x_grid, y_grid)] = unit.name[0]

            if unit.target and unit.target_name:
                # Idem pour la cible de l'unité
                xt, yt = unit.target.x, unit.target.y
                x_target, y_target = int(round(xt)), int(round(yt))
                if 0 <= y_target < self.height and 0 <= x_target < self.width:
                    targets_to_draw[(x_target, y_target)] = unit.target_name

        # 2. Placer les symboles sur la carte texte
        for (x, y), symbol in targets_to_draw.items():
            map_data[y][x] = symbol

        for (x, y), symbol in units_to_draw.items():
            # Les unités écrasent les symboles de cibles s'ils sont au même endroit
            map_data[y][x] = symbol 

        # 3. Afficher la carte, ligne par ligne
        print(" " + "=" * self.width)
        for row in map_data:
            print("|" + "".join(row) + "|")
        print("=" * (self.width + 2))
        
        # 4. Afficher le statut des unités sous la carte
        print(f"\n--- Étape {self.steps} (Flottant) ---")
        for unit in self.units:
            print(unit)

    def run_step(self) -> bool:
        """Fait avancer la simulation d'une étape."""
        self.steps += 1
        
        for unit in self.units:
            # Très important : chaque unité se met à jour en connaissant TOUTES les autres unités
            unit.update(self.units) 

        self.draw_map()
        
        # Condition d'arrêt : Si toutes les unités mobiles n'ont plus de cible, on arrête.
        if all(unit.target is None for unit in self.units if not unit.is_static):
            return False # On s'arrête
        return True # On continue

# --- DÉMARRAGE DE LA SIMULATION STANDALONE ---

sim = StandaloneSimulation(width=60, height=18)

# On crée les unités :
# Joueur Mobile Principal (A) : position (5, 5), rayon 1.5, vitesse 1.0
player_a = Unit(name="A", x=5.0, y=5.0, radius=1.5, speed=1.0) 

# Obstacle Mobile (B) : position (50, 10), rayon 1.5, vitesse 0.7
player_b = Unit(name="B", x=50.0, y=10.0, radius=1.5, speed=0.7)

# "Mur" Statique (M) : position (30, 9), rayon 2.0, vitesse 0.0 (immobile)
wall_static = Unit(name="M", x=30.0, y=9.0, radius=2.0, speed=0.0, is_static=True)

# On les ajoute à la simulation
sim.add_unit(player_a)
sim.add_unit(player_b)
sim.add_unit(wall_static) 

# On donne leurs cibles initiales :
player_a.set_target(x=55.0, y=15.0, name="T1") # A va vers T1
player_b.set_target(x=5.0, y=2.0, name="T2") # B va vers T2

print("\n*** DÉBUT DE LA SIMULATION SANS MAP (A doit éviter B et M) ***")

MAX_STEPS = 100 # Maximum d'étapes avant de s'arrêter par sécurité
current_step = 0
animation_delay = 0.1 # Pause de 0.1 seconde entre chaque étape

try:
    # On lance la boucle de simulation : continue tant que run_step() est True ET qu'on n'a pas dépassé MAX_STEPS
    while sim.run_step() and current_step < MAX_STEPS:
        current_step = sim.steps
        time.sleep(animation_delay)
except KeyboardInterrupt:
    # Permet d'arrêter la simulation en appuyant sur Ctrl+C
    print("\nSimulation interrompue par l'utilisateur.")

print(f"\n*** FIN DE LA SIMULATION après {current_step} étapes ***")