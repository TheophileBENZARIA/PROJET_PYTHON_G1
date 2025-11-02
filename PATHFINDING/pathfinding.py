# L'algo le plus efficient: A star
# Trois étapes: 1/Grid 2/Astar 3/Test
# Cmd+Shift+P puis new Terminal


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

    return 