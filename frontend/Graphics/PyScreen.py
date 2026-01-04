import pygame

class PyScreen :
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.offset_x, self.offset_y = 0, 0
        # Couleurs
        self.zoom_factor = 3

        # Paramètres de la vue isométrique
        self.tile_size = 128  # Taille d'une tuile carrée

        # Charger l'image de la tuile PNG (image carrée)
        self.TILE_IMAGE = pygame.image.load("../pygame_assets/tile.png")  # Remplace "ton_image.png" par ton fichier PNG
        # Position initiale pour le déplacement

        pygame.init()
        pygame.display.set_caption("Vue Isométrique avec PNG Carré")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def handle_input(self):
        pygame.event.get()
        keys = pygame.key.get_pressed()
        # Déplacement avec les flèches
        if keys[pygame.K_LEFT]:
            self.offset_x += 30
        if keys[pygame.K_RIGHT]:
            self.offset_x -= 30
        if keys[pygame.K_UP]:
            self.offset_y += 30
        if keys[pygame.K_DOWN]:
            self.offset_y -= 30

        if keys[pygame.K_c]:
            self.offset_x, self.offset_y = 0, 0
            self.zoom_factor = 3

        if keys[pygame.K_1]:
            self.zoom_factor *= 1.05
        if keys[pygame.K_2]:
            self.zoom_factor /= 1.05

        if keys[pygame.K_ESCAPE]: quit()

    def draw(self):
        self.screen.fill((0,0,0))
        tile_image = pygame.transform.scale(self.TILE_IMAGE, (self.tile_size * self.zoom_factor, self.tile_size * self.zoom_factor))
        for x in range(-5, 5):  # De -5 à 5 pour une taille de carte de 10x10
            for y in range(-5, 5):
                # Calcul des coordonnées isométriques
                iso_x, iso_y = self.convert_to_iso((x,y))
                # Calculer la position pour afficher l'image correctement
                rect = tile_image.get_rect(center=(iso_x, iso_y))

                # Afficher l'image (tuile carrée transformée)
                self.screen.blit(tile_image, rect.topleft)
        pygame.display.flip()

    def init(self):
        pass

    def quit(self):
        pygame.quit()

    def convert_to_iso(self,coor : tuple):
        x, y = coor
        iso_x = ((x - y) * self.tile_size // 2 + self.WIDTH // 2 + self.offset_x) * self.zoom_factor
        iso_y = ((x + y) * self.tile_size // 4 + self.HEIGHT // 4 + self.offset_y) * self.zoom_factor
        return (iso_x, iso_y)

