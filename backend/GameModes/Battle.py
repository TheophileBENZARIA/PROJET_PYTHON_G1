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
        """
        while not self.army1.isEmpty() and not self.army2.isEmpty() and (not self.max_tick or self.tick < self.max_tick) :
            self.army1.fight(self.map, otherArmy=self.army2)
            print("army1 fight ok")
            self.army2.fight(self.map, otherArmy=self.army1)
            print("army2 fight ok")
            self.save()
            print("save ok")
            self.affichage.afficher(self.map, army1=self.army1, army2=self.army2)
            print("affichage")
            self.tick+=1
        """
        import pygame
        clock = pygame.time.Clock()
        self.affichage.afficher(self.map, army1=self.army1, army2=self.army2)
        running = True
        while running:
            # Update display (this will handle input and events internally)
            result = self.affichage.afficher(self.map, army1=self.army1, army2=self.army2)
            # If afficher returns False, it means user wants to quit
            if result is False:
                running = False
            clock.tick(60)  # Limit to 60 FPS



    def save(self):
        pass
