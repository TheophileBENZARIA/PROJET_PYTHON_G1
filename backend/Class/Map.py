from backend.Class.Obstacles.Obstacle import Obstacle
from typing import List, Dict, Any


class Map:
    """
    Obstacles are treated as buildings on tiles.
    Units are placed directly on tiles.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.gameMode = None

        # grid[x][y]
        self.grid: List[List[Tile]] = [
            [Tile(x, y) for y in range(height)]
            for x in range(width)
        ]

        self.obstacles = set()

    # =========================
    # Obstacles 
    # =========================

    def add_obstacle(self, obstacle: Obstacle):
        """
        An obstacle is stored as a building on a tile.
        """
        self.obstacles.add(obstacle)
        x, y = obstacle.position

        if self.in_bounds(x, y):
            self.grid[x][y].building = obstacle

    # =========================
    # Units handling
    # =========================

    def place_unit(self, unit, x: int, y: int):
        """
        Place a unit on an empty tile.
        """
        if not self.in_bounds(x, y):
            raise ValueError("Position out of bounds")

        tile = self.grid[x][y]
        if tile.is_empty():
            tile.unit = unit
            unit.position = (x, y)
        else:
            raise ValueError("Tile occupied")

    def move_unit(self, unit, new_x: int, new_y: int):
        """
        Move a unit from its current tile to another one.
        """
        if not self.in_bounds(new_x, new_y):
            return  # ignore invalid move

        old_x, old_y = unit.position
        self.grid[old_x][old_y].unit = None

        self.grid[new_x][new_y].unit = unit
        unit.position = (new_x, new_y)

    # =========================
    # Utilities
    # =========================

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    # =========================
    # Serialization (optional but useful)
    # =========================

    def to_dict(self) -> Dict[str, Any]:
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
                tile = game_map.grid[x][y]
                tile.elevation = tile_data.get("elevation", 0)
                tile.building = tile_data.get("building")
                # unit placement handled elsewhere

        return game_map


class Tile:
    """
    One cell of the grid.
    """

    def __init__(self, x: int, y: int, elevation: int = 0):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.unit = None      # Unit currently on this tile
        self.building = None  # Obstacle / building on this tile

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