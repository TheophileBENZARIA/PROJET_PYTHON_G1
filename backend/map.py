

class Tile:
    def __init__(self, x, y, elevation=0):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.unit = None   # a unit currently standing here
        self.building = None

    def is_empty(self):
        return self.unit is None and self.building is None



class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Tile(x, y) for y in range(height)] for x in range(width)]

    def place_unit(self, unit, x, y):
        tile = self.grid[x][y]
        if tile.is_empty():
            tile.unit = unit
            unit.position = (x, y)
        else:
            raise ValueError("Tile occupied!")

    def move_unit(self, unit, new_x, new_y):
        old_x, old_y = unit.position
        self.grid[old_x][old_y].unit = None
        self.grid[new_x][new_y].unit = unit
        unit.position = (new_x, new_y)