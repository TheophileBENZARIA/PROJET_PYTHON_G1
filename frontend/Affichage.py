from abc import ABC, abstractmethod

from backend.Class.Army import Army
from backend.Class.Map import Map


class Affichage(ABC) :
    def __init__(self, *args):
        self.gameMode = None

    @abstractmethod
    def initialiser(self):
        pass

    @abstractmethod
    def afficher(self,map:Map, army1:Army, army2:Army):
        pass

    @classmethod
    def get_sizeMap(cls, map, army1, army2):
        x_max , y_max, x_min, y_min = 0,0,0,0

        for unit in army2.living_units()+ army1.living_units() :
            if unit.position[0] > x_max:
                x_max =unit.position[0]
            if unit.position[1] > y_max:
                y_max =unit.position[1]
            if unit.position[0] < x_min:
                x_min =unit.position[0]
            if unit.position[1] < y_min:
                y_min =unit.position[1]

        for obstacle in map.obstacles :
            if obstacle.position[0] > x_max:
                x_max =obstacle.position[0]
            if obstacle.position[1] > y_max:
                y_max =obstacle.position[1]
            if obstacle.position[0] < x_min:
                x_min =obstacle.position[0]
            if obstacle.position[1] < y_min:
                y_min =obstacle.position[1]

        return (x_max,x_min,y_max,y_min)
