from backend.Class.Obstacles.Obstacle import Obstacle


class Map:

    def __init__(self):

        self.obstacles = set()
        self.gameMode=None

    def add_obstacle(self, obstacle : Obstacle):
        self.map = self
        self.obstacles.add(obstacle)

    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # grid[x][y]
        self.grid: List[List[Tile]] = [[Tile(x, y) for y in range(height)] for x in range(width)]

    def place_unit(self, unit, x: int, y: int):
        tile = self.grid[x][y]
        if tile.is_empty() or tile.unit is None:
            tile.unit = unit
            unit.position = (x, y)
        else:
            raise ValueError("Tile occupied!")

    def move_unit(self, unit, new_x: int, new_y: int):
        old_x, old_y = unit.position
        self.grid[old_x][old_y].unit = None
        self.grid[new_x][new_y].unit = unit
        unit.position = (new_x, new_y)

    def to_dict(self) -> Dict[str, Any]:
        # serialize as list-of-rows for readability
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.grid[x][y].to_dict())
            tiles.append(row)
        return {
            "width": self.width,
            "height": self.height,
            "tiles": tiles,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Map":
        width = data["width"]
        height = data["height"]
        game_map = cls(width, height)
        tiles_data = data.get("tiles", [])
        for y, row in enumerate(tiles_data):
            for x, tile_data in enumerate(row):
                t = game_map.grid[x][y]
                t.elevation = tile_data.get("elevation", 0)
                t.building = tile_data.get("building")
                # do not set t.unit here — unit placement is handled by Battle.from_dict
        return game_map

class Tile:

    def __init__(self, x: int, y: int, elevation: int = 0):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.unit = None   # a unit currently standing here (set by Map.place_unit)
        self.building = None

    def is_empty(self) -> bool:
        return self.unit is None and self.building is None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "elevation": self.elevation,
            "building": self.building,
            "unit_id": self.unit.id if self.unit else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tile":
        t = cls(data["x"], data["y"], elevation=data.get("elevation", 0))
        t.building = data.get("building")
        # unit will be placed later using unit_id
        return t

"""