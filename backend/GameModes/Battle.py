from backend.GameModes.GameMode import GameMode


class Battle(GameMode):

    def __init__(self):
        super().__init__()
        self.max_tick = None
        self.tick = 0


    def end(self):
        pass

    def launch(self):
        self.affichage.initialiser()

    def gameLoop(self):
        while not self.army1.isEmpty() and not self.army2.isEmpty() and (not self.max_tick or self.tick < self.max_tick) :
            self.army1.fight(self.map, otherArmy=self.army2)
            self.army2.fight(self.map, otherArmy=self.army1)
            self.save()
            self.affichage.afficher(map,army1=self.army1, army2=self.army2)
            self.tick+=1



    def save(self):
        pass