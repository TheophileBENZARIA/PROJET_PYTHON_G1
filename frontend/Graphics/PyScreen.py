import pygame

from backend.Class.Army import Army
from backend.Class.Map import Map
from frontend.Affichage import Affichage

class PyScreen(Affichage) :


    def initialiser(self):
        pass

    def afficher(self, map: Map, army1: Army, army2: Army):
        pass

    def __init__(self, path):
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.offset_x, self.offset_y = 0, 0
        self.zoom_factor = 3

        # Paramètres de la vue isométrique
        self.tile_size = 128  # Taille d'une tuile carrée

        # Charger l'image de la tuile PNG (image carrée)
        self.TILE_IMAGE = pygame.image.load(path+"/tile.png")

        self.KNIGHT_IMAGE = pygame.image.load(path+"/knight.png")

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

    def draw(self, entitylist: list[dict]):
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

        for entity in entitylist :
            iso_coor = self.convert_to_iso(entity["coor"])

            if entity["type"] is "Knight":
                tile_image = pygame.transform.scale(self.KNIGHT_IMAGE, (self.tile_size * self.zoom_factor,
                                                                      self.tile_size * self.zoom_factor))
            rect = tile_image.get_rect(center=iso_coor)
            self.screen.blit(tile_image, rect.topleft)

            bar_width = 40 / self.zoom_factor
            bar_height = 6 / self.zoom_factor
            bar_x = iso_coor[0]
            bar_y = iso_coor[1] - 100/self.zoom_factor  # au-dessus de l'ennemi

            # Fond (rouge)
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (bar_x, bar_y, bar_width, bar_height)
            )

            # Vie actuelle (verte)
            health_ratio = entity["health"] / entity["max_health"]
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (bar_x, bar_y, bar_width * health_ratio, bar_height)
            )



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

