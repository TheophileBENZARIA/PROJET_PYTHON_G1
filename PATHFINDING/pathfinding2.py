import random

# Taille de la map
TAILLE_MAP = 120

# Initialisation de la map avec des "."
map_grid = [["." for _ in range(TAILLE_MAP)] for _ in range(TAILLE_MAP)]

# Stockage des adversaires
adversaires = {}

# Initialiser les 3 adversaires automatiquement
for i in range(1, 4):
    while True:
        x = random.randint(0, TAILLE_MAP-1)
        y = random.randint(0, TAILLE_MAP-1)
        if map_grid[y][x] == ".":  # s'assurer que la case est libre
            map_grid[y][x] = f"A{i}"
            adversaires[f"A{i}"] = (x, y)
            break

# Initialiser le personnage (Jour J) en haut à gauche
jour_j_pos = [0, 0]

# Choisir la cible automatiquement
cible_id = random.choice(list(adversaires.keys()))
print(f"La cible choisie est {cible_id} en position {adversaires[cible_id]}")

# Fonction pour afficher un zoom autour de Jour J
def afficher_map(jour_j_pos, zoom=10):
    x0 = max(jour_j_pos[0]-zoom, 0)
    x1 = min(jour_j_pos[0]+zoom, TAILLE_MAP-1)
    y0 = max(jour_j_pos[1]-zoom, 0)
    y1 = min(jour_j_pos[1]+zoom, TAILLE_MAP-1)

    for y in range(y0, y1+1):
        ligne = ""
        for x in range(x0, x1+1):
            if [x, y] == jour_j_pos:
                ligne += "J "
            elif map_grid[y][x] != ".":
                ligne += map_grid[y][x] + " "
            else:
                ligne += ". "
        print(ligne)
    print("\n")

# Boucle pour que le personnage se déplace vers la cible
while True:
    afficher_map(jour_j_pos)

    # Vérifier si on a trouvé la cible
    if tuple(jour_j_pos) == adversaires[cible_id]:
        print("Crève enflures !")
        break

    # Déplacement simple : aller vers la cible pas à pas
    cible_x, cible_y = adversaires[cible_id]

    if jour_j_pos[0] < cible_x:
        jour_j_pos[0] += 1
    elif jour_j_pos[0] > cible_x:
        jour_j_pos[0] -= 1
    elif jour_j_pos[1] < cible_y:
        jour_j_pos[1] += 1
    elif jour_j_pos[1] > cible_y:
        jour_j_pos[1] -= 1
