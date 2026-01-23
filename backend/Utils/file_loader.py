# backend/map_loader.py
"""
Simple ASCII map loader.
"""
from backend.Class.Map import Map
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman

"""
Army file format (example):
18;3
K..............P..
..C..P....K
..................


Legend (example):
  . = empty plain tile
  K = Knight
  P = Pikeman
  C = Crossbowman

This loader returns a tuple of Army instance and optionally lists of spawned units.

def load_mirrored_army_from_file(path: str) -> tuple[Army, Army] :
    #Cette fonction recupère un ficher, structurer correctement et génère une armée et une armée mirroir
    pass
"""
from backend.Class.Army import Army
from backend.Class.Units import Unit

def load_mirrored_army_from_file(path: str) -> tuple[Army, Army]:
    army1 = Army()
    army2 = Army()
    with open(path, "r", encoding="utf-8") as f:
        
        # 1. RÉCUPÉRATION DES DIMENSIONS
        
        line_header = f.readline().strip()
        if not line_header:
            return army1, army2
        
        # On extrait x_max (la largeur) pour savoir où placer le miroir
        x_max = int(line_header.split(';')[0])
        
        # 2. PARCOURS DE LA GRILLE (Ligne par ligne)
        
        for y, line in enumerate(f):
            line = line.replace("\n","").replace(" ", "") # On nettoie la ligne des retours à la ligne (\n) et des espaces
            
            
            for x, char in enumerate(line):
                
                # On vérifie si le caractère correspond à une unité connue
                unit_class = None
                if char == 'K' : unit_class = Knight
                elif char == 'C': unit_class = Crossbowman
                elif char == 'P' : unit_class = Pikeman
                if unit_class :
                    u1 = unit_class((x,y))
                    # Mirror horizontally: army2 units go to the opposite side
                    mirrored_x = x_max - 1 - x
                    u2 = unit_class((mirrored_x, y))

                    army1.add_unit(u1)
                    army2.add_unit(u2)

   
    return army1, army2

"""
Map file format (example):
20;5
####################
#..................#
#..h..H....b.......#
#..................#
####################

Legend (example):
  . = empty plain tile
  # = impassable (treated as building/wall)
  h = hill (elevation +1)
  H = high hill (elevation +2)
  b = building (provides cover)

This loader returns a Map instance and optionally lists of spawned units.
"""
def load_map_from_file(path: str) -> Map:
    """
    with open(path, "r", encoding="utf-8") as f:
        x_max, y_max = f.readline().replace("\n", "").split(";")
        x_max, y_max = int(x_max), int(y_max)
        lines = [line.rstrip("\n") for line in f.readlines() if line.strip() != ""]

    for y in range(y_max):
        for x in range(x_max):
            ch = None
            try:
                ch = lines[y][x]
            except:
                break
    """
    return Map()


"""
    CHAR_LEGEND = {
    "K": {"elevation": 0, "building": None},
    "C": {"elevation": 0, "building": "wall"},
    "P": {"elevation": 1, "building": None},
    }

    height = len(lines)
    width = max(len(line) for line in lines)
    game_map = Map(width, height)

    army1 = Army("Player1")
    army2 = Army("Player2")

    for y, line in enumerate(lines):
        for x, ch in enumerate(line.ljust(width, ".")):
            info = CHAR_LEGEND.get(ch, CHAR_LEGEND["."])
            tile = game_map.grid[x][y]
            tile.elevation = info.get("elevation", 0)
            tile.building = info.get("building", None)
            spawn = info.get("spawn")
            if spawn:
                owner, unit_type = spawn
                # spawn a Knight by default; extend for more unit types later
                unit = Knight(owner)
                game_map.place_unit(unit, x, y)
                if owner == "Player1":
                    army1.add_unit(unit)
                else:
                    army2.add_unit(unit)

    return game_map, army1, army2
    """
