from backend.Class.Army import Army
from backend.Class.Map import Map
from frontend.Affichage import Affichage


class NoAffiche(Affichage):
    def initialiser(self):
        pass

    def afficher(self, map: Map, army1: Army, army2: Army):
        pass