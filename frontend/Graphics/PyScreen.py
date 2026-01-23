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
        # Initialisation de Pygame
        pygame.init()
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Affichage d'une tile")
        # Chargement de l'image

        self.WIDTH, self.HEIGHT = 1920, 1080
        self.offset_x, self.offset_y = 0, 0
        self.zoom_factor = 3

        # Paramètres de la vue isométrique
        self.tile_size = 10  # Taille d'une tuile carrée

        # Charger l'image de la tuile PNG (image carrée)
        self.TILE_IMAGE = pygame.image.load(self.path + "tile.bmp").convert()

        self.KNIGHT_IMAGE = pygame.image.load(self.path + "knight.bmp").convert()
        self.PIKEMAN_IMAGE = pygame.image.load(self.path + "pikeman.bmp").convert()
        self.CROSSBOWMAN_IMAGE = pygame.image.load(self.path + "crossbowman.bmp").convert()

    def afficher(self, map: Map, army1: Army, army2: Army):


        self.screen.fill((0, 0, 0))
        x_max, x_min, y_max, y_min = Affichage.get_sizeMap(map, army1, army2)
        print(x_max, x_min, y_max, y_min)
        tile_image = pygame.transform.scale(self.TILE_IMAGE,
                                            (self.tile_size * self.zoom_factor, self.tile_size * self.zoom_factor))

        for x in range(int(x_min) - 1, int(x_max) + 1,10):
            for y in range(int(y_min) - 1, int(y_max) + 1,10):
                iso_x, iso_y = self.convert_to_iso((x,y))
                self.screen.blit(self.TILE_IMAGE, (iso_x, iso_y))
        # Mise à jour de l'écran
        pygame.display.flip()

        sleep(0.1)



    def __init__(self, *args):
        super().__init__(*args)
        self.path = args[0]


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

