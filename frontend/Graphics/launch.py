from time import sleep

import PyScreen

scr = PyScreen.PyScreen()

entl = [
    {
        "coor" : (0.2,0.3),
        "type" : "Knight",
        "health" : 30,
        "max_health" : 100
    }


]


running = True
while running:

    scr.handle_input()
    scr.draw(entl)

scr.quit()