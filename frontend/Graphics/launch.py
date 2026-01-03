from time import sleep

import PyScreen

scr = PyScreen.PyScreen()

running = True
while running:

    scr.handle_input()
    scr.screen.fill(scr.BLUE)
    scr.draw()
    sleep(0.01)

scr.quit()