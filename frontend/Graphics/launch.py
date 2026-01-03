from time import sleep

import PyScreen

scr = PyScreen.PyScreen()

while True :
    scr.draw()
    scr.handle_input()