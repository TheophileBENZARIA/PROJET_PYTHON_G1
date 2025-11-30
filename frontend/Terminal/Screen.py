import curses

class Screen :
    def __init__(self, stdsrc :curses.window):
        self.std = stdsrc
        self.x = 0
        self.y = 0

    def start(self):
        curses.curs_set(0)
        self.std.nodelay(True)
        self.std.keypad(True)

    def getch(self):
        self.std.getch()


    def afficher_grille(self, grille):
        ly = len(grille)
        if (ly > 0) :
            lx = len(grille[0])
            max_y, max_x = self.std.getmaxyx()
            max_y-=2

            #right border
            c = "|"
            if (self.x > 0) :
                c="."
            for i in range(1,min(max_y-2, ly)+1) :
                self.std.addstr(i,0,c)

            for i in range(1,min(lx-self.x, max_x-2)+1) :

                c="_"
                if self.y >0:
                    c="."
                self.std.addstr(0,i,c)

                for j in range(1,min(ly-self.y,max_y-2)+1) :
                    self.std.addstr(j,i,str(grille[j-1][i-1]))

                c = "."
                if min(ly-self.y,max_y-2) == ly-self.y:
                    c = "‾"
                self.std.addstr(min(ly-self.y,max_y-2)+1, i, c)

            #left border
            c = "."
            if  min(lx-self.x,max_x-2) == lx-self.x:
                c = "|"
            for i in range(1, min(max_y - 2, ly) + 1):
                self.std.addstr(i, min(lx-self.x,max_x-2)+1, c)