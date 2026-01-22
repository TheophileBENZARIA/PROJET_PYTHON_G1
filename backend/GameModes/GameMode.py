from abc import ABC, abstractmethod


class GameMode(ABC) :
    def __init__(self):
        self.army1 = None
        self.army2 = None
        self.affichage = None
        self.map = None

    @abstractmethod
    def launch(self):
        pass

    @abstractmethod
    def gameLoop(self):
        pass

    @abstractmethod
    def save(self):
        pass


