from time import sleep

import PyScreen

scr = PyScreen.PyScreen()

running = True
while running:

    scr.handle_input()
    scr.draw()

scr.quit()