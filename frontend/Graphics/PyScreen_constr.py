from time import sleep

import pygame

from backend.Class.Army import Army
from backend.Class.Map import Map
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman
from frontend.Affichage import Affichage

class PyScreen(Affichage) :


    def initialiser(self):
        print("init")
        pygame.init()
        pygame.display.set_caption("Vue pygame")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def afficher(self, map: Map, army1: Army, army2: Army):

        self.screen.fill((0, 0, 0))
        x_max,x_min,y_max,y_min = Affichage.get_sizeMap(map, army1, army2)

        tile_image = pygame.transform.scale(self.TILE_IMAGE,
                                            (self.tile_size * self.zoom_factor, self.tile_size * self.zoom_factor))

        for x in range(int(x_min)-1,int(x_max)+1):
            for y in range(int(y_min)-1, int(y_max)+1):
                # Calcul des coordonnées isométriques
                iso_x, iso_y = self.convert_to_iso((x, y))

                rect = tile_image.get_rect(center=(iso_x, iso_y))

                # Afficher l'image (tuile carrée transformée)
                self.screen.blit(tile_image, rect.topleft)

        for unit in army1.living_units()+army2.living_units():
            iso_coor = self.convert_to_iso(unit.position)
            IMAGE = None
            if isinstance(unit, Knight):
                IMAGE = self.KNIGHT_IMAGE
            if isinstance(unit, Pikeman):
                IMAGE = self.PIKEMAN_IMAGE
            if isinstance(unit, Crossbowman):
                IMAGE = self.CROSSBOWMAN_IMAGE


            unit_image = pygame.transform.scale(IMAGE, (self.tile_size * self.zoom_factor,self.tile_size * self.zoom_factor))
            rect = unit_image.get_rect(center=iso_coor)
            self.screen.blit(tile_image, rect.topleft)
            """
            bar_width = 40 / self.zoom_factor
            bar_height = 6 / self.zoom_factor
            bar_x = iso_coor[0]
            bar_y = iso_coor[1] - 100 / self.zoom_factor  # au-dessus de l'ennemi

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
            """

        pygame.display.flip()
        sleep(1)

    def __init__(self, *args):
        super().__init__(*args)
        path = args[0]
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.offset_x, self.offset_y = 0, 0
        self.zoom_factor = 3

        # Paramètres de la vue isométrique
        self.tile_size = 128  # Taille d'une tuile carrée

        # Charger l'image de la tuile PNG (image carrée)
        print(path+"/tile.png")
        self.TILE_IMAGE = pygame.image.load(path+"/tile.bmp")

        self.KNIGHT_IMAGE = pygame.image.load(path+"/knight.bmp")
        self.PIKEMAN_IMAGE = pygame.image.load(path + "/pikeman.bmp")
        self.CROSSBOWMAN_IMAGE = pygame.image.load(path + "/crossbowman.bmp")

        self.screen =None


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


    def convert_to_iso(self,coor : tuple):
        x, y = coor
        iso_x = ((x - y) * self.tile_size // 2 + self.WIDTH // 2 + self.offset_x) * self.zoom_factor
        iso_y = ((x + y) * self.tile_size // 4 + self.HEIGHT // 4 + self.offset_y) * self.zoom_factor
        return (iso_x, iso_y)

