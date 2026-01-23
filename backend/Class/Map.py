from backend.Class.Obstacles.Obstacle import Obstacle


class Map:
    def __init__(self):

        self.obstacles = set()
        self.gameMode=None

    def add_obstacle(self, obstacle : Obstacle):
        self.map = self
        self.obstacles.add(obstacle)