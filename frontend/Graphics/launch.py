from time import sleep

import PyScreen

if __name__ == '__main__':
    scr = PyScreen.PyScreen("pygame_assets")

    entl = [
        {
            "coor": (0.2, 0.3),
            "type": "Knight",
            "health": 30,
            "max_health": 100
        }

    ]

    running = True
    while running:
        scr.handle_input()
        scr.draw(entl)

    scr.quit()


def launch_pygame_battle(battle, assets_dir: str):
    screen = PyScreen.PyScreen(assets_dir)

