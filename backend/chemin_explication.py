import math 
import time #permet de ralentir l'animation
import os #nettoie la carte

# --- CLASSES DE BASE (Vector et Unit) ---

class Vector: #definit une classe pour représenter un vecteur 2D (position ou deplacement)
    def __init__(self, x, y): #initialisation des coordonées
        self.x = x
        self.y = y

    def __sub__(self, other): #soustraction entre deux vecteurs : retourne un vecteur qui avec la diff des coordonées
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other): #addition entre 2 vecteurs
        return Vector(self.x + other.x, self.y + other.y)#retourne un vecteur

    def magnitude(self): #magnitude (longueur) du veteur, utilise pythagore
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self): #normalise le vecteur (le rend unitaire)
    #divise chaque coordonee par la magnitude
        mag = self.magnitude()
        if mag == 0:  #si magnitude = 0 vecteur retourné est 0,0
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag) 

    def scale(self, scalar): #permet de multiplier le vecteur par un scalaire (étire ou condense)
        return Vector(self.x * scalar, self.y * scalar)

class Unit: #rpz une unité dans la simulation
    def __init__(self, name, x, y, radius, speed, is_static=False):
        self.name = name
        self.position = Vector(x, y)
        self.target = None
        self.target_name = None # NOUVEAU : Nom de la cible
        self.radius = radius #rayon d'influence de l'unité
        self.speed = speed #vitesse de déplacement
        self.is_evading = False #boolean si unité est entrain d'éviter un obstacle
        self.is_static = is_static #indique si l'unité ne se déplace pas
        self.last_move = Vector(0, 0) 
        
    def set_target(self, x, y, name=None): # definition de la cible de l'unité et son nom
        if not self.is_static:
            self.target = Vector(x, y)
            self.target_name = name if name else 'T' # Utilise 'T' par défaut
            self.is_evading = False

    def update(self, obstacles): #appelé à chaque étape de la simulation. Si l'uunité est static, elle ne bouge pas.
        if self.is_static:
            self.last_move = Vector(0, 0) # Les murs ne bougent pas
            return #permet de définir les unité statique

        # Stocker la position avant le mouvement
        old_position = self.position #on garde la position actuelle avant le mvt pour pouvoir calculer le déplacement
        
        if not self.target: #si l'unité n'a pas de cible, elle ne se déplace pas
            self.last_move = Vector(0, 0)
            return

        direction_to_target = (self.target - self.position).normalize() #on calcule la direction vers la cible (vecteur normalisé), 
        movement_vector = direction_to_target.scale(self.speed)#puis on multiplie ce vecteur âr la vitesse pour obtenir le vecteur de déplacement

        evasion_vector = self._check_for_obstacles(obstacles) #verification de si les obstacles proches

        # Si obstacles proches -> application de l'évitement
        if evasion_vector.magnitude() > 0: #si vecteur d'evitement existe -> magnitude >0
            # Combinaison : 0.5 vers la cible, 1.5 pour l'évitement (favorise l'évitement)
            combined_vector = movement_vector.scale(0.5) + evasion_vector.scale(1.5) 
            self.is_evading = True
        else: #si pas d'obstacle : 
            combined_vector = movement_vector #simple mvt vers la cible
            # Reprise de la trajectoire
            if self.is_evading: #si l'unité est en evitement, on véirife si la distance restante à la cible est sufisante
            # (>speed*2) pour decider de remettre is_evading à False
                if (self.target - self.position).magnitude() > self.speed * 2:
                    self.is_evading = False

        # 3. Mouvement
        target_distance = (self.target - self.position).magnitude() #calcul la distance restante à la coble
        
        if target_distance > self.speed: #Si la distance > speed : on se déplace d’une longueur speed dans la direction de combined_vector (on normalise pour préserver la longueur).
            final_move = combined_vector.normalize().scale(self.speed)
            self.position = self.position + final_move
        else: #Sinon (on est proche) : on se déplace exactement jusqu’à la cible (évite de « dépasser »), position = target, et on efface target et target_name.
            final_move = self.target - self.position # Déplacement exact jusqu'à la cible
            self.position = self.target
            self.target = None
            self.target_name = None # Réinitialiser le nom de la cible
            
        #Calcule le vecteur du déplacement réellement effectué cette étape, utile pour l’affichage/debug
        self.last_move = self.position - old_position
            
    def _check_for_obstacles(self, obstacles):
        evasion_force = Vector(0, 0) #Initialise le vecteur d’évitement à zéro.
        proximity_threshold = self.radius * 6 #définit jusqu’à quelle distance on commence à appliquer une force d’évitement (ici 6 fois le rayon).

        for obstacle in obstacles: #Parcourt chaque obstacle (en réalité on passe toutes les unités, 
            #d’où le test is self pour ignorer soi-même).
            if obstacle is self: 
                continue

            distance = (obstacle.position - self.position).magnitude() #Calcule la distance à l’obstacle.
            
            if distance < proximity_threshold: #Si cette distance est inférieure au seuil
                away_from_obstacle = (self.position - obstacle.position).normalize() #away_from_obstacle : vecteur unitaire pointant loin de l’obstacle.
                strength = 1 - distance / proximity_threshold #strength : facteur entre 0 et 1 qui augmente lorsque l’obstacle est plus proche (linéaire).
                evasion_force = evasion_force + away_from_obstacle.scale(strength) #On accumule dans evasion_force la contribution pondérée par strength. Ainsi plusieurs obstacles s’additionnent.

        return evasion_force #retourne le vecteur d'evitement total (zéro si aucun obstacle)

    def __str__(self): #Si l’unité est statique, __str__ renvoie une ligne descriptive indiquant que c’est un mur statique
        if self.is_static:
            return f"[{self.name}] ({self.position.x:.1f}, {self.position.y:.1f}) - Mur Statique"
        
        status = "**ÉVITE**" if self.is_evading else ("Mouvement" if self.target else "Au repos")
        pos = f"({self.position.x:.1f}, {self.position.y:.1f})"
        
        # Afficher le déplacement
        move = f"-> dx:{self.last_move.x:.2f}, dy:{self.last_move.y:.2f}"
        
        return f"[{self.name}] {pos} - {status} {move}"
    
    #Pour unités mobiles :

#status : affiche **ÉVITE** si en évitement, sinon Mouvement si une cible existe, sinon Au repos.
#pos : position formatée.
#move : changement de position (dx, dy) formaté à 2 décimales.
# Retourne une chaîne combinant tout ça, utilisée lors de l’affichage console.

# --- CLASSE DE SIMULATION ET SCÉNARIO (Taille 50x15) ---

class Simulation:
    def __init__(self, width=50, height=15):
        self.units = []
        self.steps = 0
        self.width = width
        self.height = height
        self.map_data = [['.' for _ in range(self.width)] for _ in range(self.height)] #matrice (height x width) initialisée avec '.' pour les cellules vides.

    def add_unit(self, unit): #Ajoute une unité à la simulation.
        self.units.append(unit)

    def draw_map(self):
        # Effacer l'écran
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Réinitialiser la carte
        self.map_data = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # 1. Placer les cibles, les murs et les unités
        targets_to_draw = {} # Pour éviter d'écraser les symboles de cible si elles sont au même endroit
        
        for unit in self.units:
            # Enregistrer la cible pour l'affichage (étape 2)
            #Pour chaque unité, si elle a une target et target_name, on arrondit (round) ses coordonnées et on stocke le nom de cible dans targets_to_draw (seulement si dans les limites de la grille).
            if unit.target and unit.target_name:
                x_target = int(round(unit.target.x))
                y_target = int(round(unit.target.y))
                if 0 <= y_target < self.height and 0 <= x_target < self.width:
                    targets_to_draw[(x_target, y_target)] = unit.target_name
            
            x_pos = int(round(unit.position.x))
            y_pos = int(round(unit.position.y))
            
            # Afficher le mur statique 'M'
            if unit.is_static and 0 <= y_pos < self.height and 0 <= x_pos < self.width:
                 self.map_data[y_pos][x_pos] = 'M'
            
            # Afficher l'unité mobile (A ou B)
            elif 0 <= y_pos < self.height and 0 <= x_pos < self.width:
                # L'unité affiche toujours son initiale, même en évitant
                symbol = unit.name[0]
                self.map_data[y_pos][x_pos] = symbol

        # 2. Afficher les cibles (T1, T2) après avoir placé les unités
        for (x, y), name in targets_to_draw.items():
             # Placer la cible seulement si la case est vide (pour ne pas écraser les unités ou murs)
            if self.map_data[y][x] == '.':
                 self.map_data[y][x] = name

        # 3. Afficher la carte dans le terminal
        print(" " + "=" * self.width)
        for row in self.map_data:
            print("|" + "".join(row) + "|")
        print("=" * (self.width + 2))
        
        # 4. Afficher le statut des unités (avec les mouvements)
        print(f"\n---  Étape {self.steps} ---")
        for unit in self.units:
            print(unit)

    def run_step(self):
        self.steps += 1
        
        for unit in self.units:
            unit.update(self.units)

        self.draw_map()
        
        if all(unit.target is None for unit in self.units if not unit.is_static):
            return False
        return True

# -----------------------------------------------------------------

# --- DÉMARRAGE DE LA SIMULATION ---

sim = Simulation() 

# Joueur Mobile Principal (A)
player_a = Unit(name="A", x=5, y=5, radius=1.0, speed=0.8) 

# Obstacle Mobile (B)
player_b = Unit(name="B", x=45, y=10, radius=1.0, speed=0.5)

# Mur Statique (M)
wall = Unit(name="M", x=25, y=7, radius=1.0, speed=0.0, is_static=True)


sim.add_unit(player_a)
sim.add_unit(player_b)
sim.add_unit(wall) 

# Cibles : trajectoires diagonales qui se croisent
# ATTENTION : J'ajoute le nom de la cible dans set_target()
player_a.set_target(x=40, y=12, name="T1") 
player_b.set_target(x=10, y=3, name="T2") 

print("\n*** DÉBUT DE LA SIMULATION (A doit éviter B et M) ***")

MAX_STEPS = 100
current_step = 0
animation_delay = 0.2

try:
    while sim.run_step() and current_step < MAX_STEPS:
        current_step = sim.steps
        time.sleep(animation_delay)
except KeyboardInterrupt:
    print("\nSimulation interrompue par l'utilisateur.")

print("\n*** FIN DE LA SIMULATION ***")