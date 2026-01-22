import pygame
from backend.Class.Units import Knight, Pikeman, Crossbowman

TILE = 38  # same as pygame_view
UNIT_TYPES = ["Knight", "Pikeman", "Crossbowman"]
UNIT_CLASS = {
    "Knight": Knight,
    "Pikeman": Pikeman,
    "Crossbowman": Crossbowman,
}

COLOR = {
    "Knight": (0, 150, 255),
    "Pikeman": (0, 255, 100),
    "Crossbowman": (255, 200, 0),
}

def pygame_placement_editor(game_map, assets):
    pygame.init()
    width = game_map.width
    height = game_map.height

    screen = pygame.display.set_mode((width * TILE, height * TILE))
    pygame.display.set_caption("Unit Placement Editor")

    clock = pygame.time.Clock()
    selected = "Knight"

    # positions chosen by player
    positions = {t: [] for t in UNIT_TYPES}

    running = True
    while running:
        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = "Knight"
                elif event.key == pygame.K_2:
                    selected = "Pikeman"
                elif event.key == pygame.K_3:
                    selected = "Crossbowman"
                elif event.key == pygame.K_RETURN:
                    
                    return positions

            # Mouse Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x = mx // TILE
                y = my // TILE
                tile = game_map.grid[x][y]

                # left click = place
                if event.button == 1:
                    if tile.building is None and (x, y) not in positions[selected]:
                        positions[selected].append((x, y))

                # right click = remove
                if event.button == 3:
                    for t in UNIT_TYPES:
                        if (x, y) in positions[t]:
                            positions[t].remove((x, y))

        # ====================
        # DRAW MAP
        # ====================

        screen.fill((80, 180, 80))  # background

        for y in range(height):
            for x in range(width):
                tile = game_map.grid[x][y]
                px = x * TILE
                py = y * TILE

                # draw ground
                grass = assets.get("grass")
                if grass:
                    screen.blit(grass, (px, py))
                else:
                    pygame.draw.rect(screen, (100, 200, 100), (px, py, TILE, TILE))

                # draw hill
                if tile.elevation > 0:
                    hill = assets.get("hill")
                    if hill:
                        screen.blit(hill, (px, py))
                    else:
                        pygame.draw.rect(screen, (160, 160, 80), (px, py, TILE, TILE))

                # draw building
                if tile.building:
                    img = assets.get("building")
                    if img:
                        screen.blit(img, (px, py))
                    else:
                        pygame.draw.rect(screen, (140, 80, 40), (px, py, TILE, TILE))

                pygame.draw.rect(screen, (40, 40, 40), (px, py, TILE, TILE), 1)

        # ====================
        # DRAW PLACED UNITS
        # ====================
        for t in UNIT_TYPES:
            color = COLOR[t]
            img = assets.get(t)
            for (x, y) in positions[t]:
                px = x * TILE
                py = y * TILE
                if img:
                    screen.blit(img, (px, py))
                else:
                    pygame.draw.circle(screen, color, (px + TILE//2, py + TILE//2), TILE//2 - 3)

        # UI text
        font = pygame.font.Font(None, 26)
        txt = font.render(f"Selected: {selected}   (1/2/3)", True, (255, 255, 255))
        screen.blit(txt, (8, 8))

        pygame.display.flip()
        clock.tick(60)