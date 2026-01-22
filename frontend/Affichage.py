from abc import ABC, abstractmethod

from backend.Class.Army import Army
from backend.Class.Map import Map


class Affichage(ABC) :


    @abstractmethod
    def initialiser(self):
        pass

    @abstractmethod
    def afficher(self,map:Map, army1:Army, army2:Army):
        pass

