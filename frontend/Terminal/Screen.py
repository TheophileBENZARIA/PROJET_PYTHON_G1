import curses
import sys
from socket import send_fds
from time import sleep


class Screen :
    def __init__(self, stdsrc :curses.window):
        self.std = stdsrc
        self.x = 0
        self.y = 0

        self.grille = []

    def start(self):
        curses.curs_set(0)
        self.std.nodelay(True)
        self.std.keypad(True)

    def getch(self):
        key =self.std.getch()
        if key == 259 and self.y >0:# up arrow
            self.y-=1
        if key == 258 : #down arrow
            self.y+=1
        if key == 260 and self.x >0: #right arrow
            self.x-=1
        if key == 261 : #left arrow
            self.x+=1

        if key == ord('q'):
            sys.exit()


    def actualiser_grille(self, grille):
        self.grille = grille

    def afficher_grille(self):
        x_n = 0
        y_n = 0

        maxy, maxx = self.std.getmaxyx()
        maxy-=3
        maxx-=2

        if abs(maxy - len(self.grille)) < self.y :
            self.y = abs(maxy - len(self.grille))
        min_y = self.y
        max_y = maxy + self.y
        if  maxy > len(self.grille) :
            y_n = 1
            min_y = 0
            max_y = len(self.grille)
        elif maxy == len(self.grille) - self.y:
            min_y = self.y
            max_y = maxy + self.y
            y_n =2
        elif self.y == 0:
                y_n = 4
        else :
            y_n=3


        if len(self.grille) == 0 :
            x_n = 1
            min_x = 0
            max_x = 0
        else :
            if abs(maxx - len(self.grille[0])) < self.x :
                self.x = abs(maxx - len(self.grille[0]))
            min_x = self.x
            max_x = maxx + self.x

            if maxx > len(self.grille[0]):
                x_n = 1
                min_x = 0
                max_x = len(self.grille[0])
            elif maxx == len(self.grille[0]) - self.x:
                min_x = self.x
                max_x = maxx + self.x
                x_n = 2
            elif self.x == 0 :
                x_n = 4
            else:
                x_n = 3

        for y in range(min_y, max_y):
            c= "|"
            if x_n == 2 or x_n == 3 :
                c="."
            self.std.addstr(1+y-min_y,0,c)

        for x in range(min_x,max_x) :
            c = "_"
            if y_n == 2 or y_n == 3:
                c = "."
            self.std.addstr(0,1+x-min_x,c)
            for y in range(min_y, max_y) :
                self.std.addstr(1 + y - min_y, 1+x-min_x, str(self.grille[y][x]))
            c = "‾"
            if y_n == 3 or y_n == 4:
                c = "."
            self.std.addstr(1 + max_y - min_y, 1+x-min_x,c)

        for y in range(min_y, max_y):
            c= "|"
            if x_n == 4 or x_n == 3 :
                c="."
            self.std.addstr(1+y-min_y,1 + max_x - min_x,c)


        self.std.addstr(maxy-1,0,"q pour quitter ; utiliser les flèches pour se déplacer")
