# frontend/terminal_view.py
from backend.map import Map

def print_map(game_map: Map):
    for y in range(game_map.height):
        row = ""
        for x in range(game_map.width):
            tile = game_map.grid[x][y]
            if tile.unit:
                if tile.unit.owner == "Player1":
                    row += "A"
                else:
                    row += "B"
            else:
                row += "."
        print(row)
    print()
