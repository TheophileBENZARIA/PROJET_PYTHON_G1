# L'algo le plus efficient: A star
# Trois étapes: 1/Grid 2/Astar 3/Test
# Cmd+Shift+P puis new Terminal

# Démarrer : git pull origin main
#Coder ton travail...
#Finir : git add .
#Finir : git commit -m "Ton message décrivant le travail"
#Finir : git push origin main
 """"
from heapq import heappush, heappop
import math
import random

class Grid: #ca c'est mon constructeur et dedans j'ai des methodes
    def __init__(self, width, height, walls=None, allow_diagonal=False, cost_deplacement=None):
        self.width = width
        self.height = height
        self.walls = set(walls) if walls else set()
        self.allow_diagonal = allow_diagonal
        self.cost_deplacement = dict(cost_deplacement) if cost_deplacement else {}

    def in_bounds(self, node):
        x, y = node  #là je crée un tuple(x,y) qui corres aux coordonées de mon noeud
        return 0<x<self.width and 0<y<self.height  #x(largeur) et y(hauteur)
    
    def neighbors(self, node):
        x, y = node
        candidates = [(x+1,y+1) , (x+1,y-1) , (x-1,y+1) , (x-1,y-1)]
        if self.allow_diagonal :
            candidates = candidates + [(x+1,y+1) , (x+1,y-1) , (x-1,y+1) , (x-1,y-1)]
        results = [n for n in candidates if self.in_bounds(n) and self.clear(n)] # on parcourt la liste candidates et a chaque fois que n est dans les limites on l'ajoute à la new liste results en gros n c'est un voisin possible
        return results 
    
    def clear(self, node): #là je verifie si c'est un obstacle
        return node not in self.walls
    
    def cost(self, from_node, to_node):
        return self.cost_deplacement.get(to_node, 1) #get est une methode python pour acceder a une clee d'un dictionnaire SYNTAXE: dictionnaire.get(clé, valeur par defaut)
    

def heuristic(a,b): #Cette methode calcule le cout pour aller du point a au point b 
    (x1, y1) = a
    (x2, y2) = b


    return """

import math
import random

class Unite:
    def __init__(self, x, y, target_x, target_y, vitesse=1.0, rayon=0.5):
        self.x = float(x)
        self.y = float(y)
        self.target_x = float(target_x)
        self.target_y = float(target_y)
        self.vitesse = vitesse
        self.rayon = rayon  # taille de l'unité
        self.update_direction()

    def update_direction(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            self.dx = dx / dist
            self.dy = dy / dist
        else:
            self.dx = self.dy = 0

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def eviter_collision(self, autres, force_avoidance=0.5):
        # Calcul d’un vecteur de répulsion si un autre joueur est trop proche
        avoid_x, avoid_y = 0, 0
        for autre in autres:
            if autre is self:
                continue
            dist = self.distance_to(autre)
            if dist < self.rayon * 2:  # collision potentielle
                # Calcul d’un vecteur qui s’éloigne de l’autre
                avoid_x += (self.x - autre.x) / (dist + 1e-6)
                avoid_y += (self.y - autre.y) / (dist + 1e-6)

        # Ajuste légèrement la direction si nécessaire
        self.dx += force_avoidance * avoid_x
        self.dy += force_avoidance * avoid_y
        norm = math.sqrt(self.dx**2 + self.dy**2)
        if norm > 0:
            self.dx /= norm
            self.dy /= norm

    def deplacer(self, autres):
        self.eviter_collision(autres)
        self.x += self.dx * self.vitesse
        self.y += self.dy * self.vitesse
        self.update_direction()

    def atteint_cible(self, tolerance=0.1):
        return math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2) < tolerance
