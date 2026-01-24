from backend.GameModes.GameMode import GameMode


class Battle(GameMode):

    def __init__(self):
        super().__init__()
        self.max_tick = None
        self.tick = 0


    def end(self):
        if hasattr(self.affichage, "shutdown"):
            self.affichage.shutdown()

    def launch(self):
        self.affichage.initialiser()

    def gameLoop(self):
        import time
        use_pygame = getattr(self.affichage, "uses_pygame", False)
        clock = None
        if use_pygame:
            import pygame
            clock = pygame.time.Clock()
        else:
            pygame = None  # placeholder for cleanup branch

        # Initial display (helps fill buffers for curses/pygame alike)
        self.affichage.afficher(self.map, army1=self.army1, army2=self.army2)
        running = True
        last_tick_time = time.time()
        tick_delay = 0.5  # Delay between battle ticks (in seconds) - adjust for faster/slower simulation

        while running:
            # Check if battle should continue
            battle_continues = (
                not self.army1.isEmpty() and 
                not self.army2.isEmpty() and 
                (self.max_tick is None or self.tick < self.max_tick)
            )
            paused = False
            if hasattr(self.affichage, "is_paused") and callable(getattr(self.affichage, "is_paused")):
                try:
                    paused = self.affichage.is_paused()
                except Exception:
                    paused = False

            if battle_continues and not paused:
                # Check if enough time has passed for next tick
                current_time = time.time()
                if current_time - last_tick_time >= tick_delay:
                    # Store previous positions for smooth animation (before battle tick)
                    if hasattr(self.affichage, 'unit_previous_positions'):
                        for unit in self.army1.living_units() + self.army2.living_units():
                            if unit.position is not None:
                                self.affichage.unit_previous_positions[unit.id] = unit.position

                    # Execute one battle tick
                    self.army1.fight(self.map, otherArmy=self.army2)
                    self.army2.fight(self.map, otherArmy=self.army1)
                    self.save()
                    self.tick += 1
                    last_tick_time = current_time
                    
                    # Print battle status
                    army1_count = len(self.army1.living_units())
                    army2_count = len(self.army2.living_units())
                    #print(f"Tick {self.tick}: Army1={army1_count} units, Army2={army2_count} units")
            
            # Update display (this will handle input and events internally)
            result = self.affichage.afficher(self.map, army1=self.army1, army2=self.army2)
            
            # If afficher returns "QUIT", user wants to quit
            if result == "QUIT":
                running = False
                break

            # If battle is over, show final state but keep window open
            if not battle_continues:
                # Battle ended - show final results
                if self.army1.isEmpty():
                    print("Battle Over: Army 2 wins!")
                elif self.army2.isEmpty():
                    print("Battle Over: Army 1 wins!")
                elif self.max_tick and self.tick >= self.max_tick:
                    print(f"Battle Over: Reached max tick ({self.max_tick})")
                    army1_count = len(self.army1.living_units())
                    army2_count = len(self.army2.living_units())
                    print(f"Final: Army1={army1_count} units, Army2={army2_count} units")
            
            if clock:
                clock.tick(60)
            else:
                time.sleep(0.05)

        # Clean up pygame when exiting
        if pygame:
            pygame.quit()
        print("Battle ended. Exiting...")

    def save(self):
        pass
