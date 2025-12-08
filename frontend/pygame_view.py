"""
Pygame frontend (top-down 2.5D with elevation offset and z-sorting)

Usage:
  - place assets in frontend/pygame_assets/ (see ASSET_FILENAMES below)
  - from Python:
        from frontend.pygame_view import launch_pygame_battle
        launch_pygame_battle(battle, delay=0.2, assets_dir="frontend/pygame_assets")
"""
import os
import time
import math
import threading
import queue
from turtle import delay
from typing import Dict, Any, List, Tuple, Optional

from backend import battle

try:
    import pygame
except Exception:
    pygame = None

TILE_SIZE = 38    # pixels per tile (adjustable)
FPS = 60

# Expected asset filenames (put PNGs into frontend/pygame_assets/)
ASSET_FILENAMES = {
    "grass": "grass.png",
    "hill": "hill.png",
    "building": "building.png",
    "Knight": "knight.png",
    "Pikeman": "pikeman.png",
    "Crossbowman": "crossbowman.png",
    "shadow": "shadow.png",  # optional shadow image
}

# how many pixels vertical offset per elevation level (tunable for "2.5D" look)
ELEVATION_PIXEL = int(TILE_SIZE * 0.45)


def _load_image(path, size=None):
    # load image; convert_alpha requires display initialized (we ensure that earlier)
    img = pygame.image.load(path)
    # convert_alpha sometimes fails if display not initialized; we expect display init done
    try:
        img = img.convert_alpha()
    except Exception:
        try:
            img = img.convert()
        except Exception:
            pass
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img


class PygameView:
    def __init__(self, game_map, tile_size=TILE_SIZE, assets_dir="frontend/pygame_assets"):
        if pygame is None:
            raise RuntimeError("pygame not installed. Install with `pip install pygame`.")
        self.map = game_map
        self.tile_size = tile_size
        self.assets_dir = assets_dir
        self.screen = None
        self.clock = pygame.time.Clock()
        self.width_px = self.map.width * tile_size
        # reserve UI area under map for logs
        self.height_px = self.map.height * tile_size + 140
        self.running = False

        # Ensure pygame and the display module are initialized before loading images.
        # convert_alpha() requires pygame.display to be initialized.
        try:
            if not pygame.get_init():
                pygame.init()
            if not pygame.display.get_init():
                # initialize display module only (no window yet). This is enough for convert_alpha.
                pygame.display.init()
        except Exception:
            # If initialization fails (headless env), continue — loader will handle missing images.
            pass

        # load assets (missing assets -> graceful fallback)
        self.assets: Dict[str, Any] = {}
        self._load_assets()

    def _asset_path(self, name: str) -> str:
        return os.path.join(self.assets_dir, name)

    def _load_assets(self):
        """
        Load assets from self.assets_dir. Be verbose about missing files or load errors.
        Also try fallback directories if the provided directory doesn't look right.
        """
        # Candidate directories to try in order
        candidates = []
        if self.assets_dir:
            candidates.append(self.assets_dir)
        # common fallbacks
        candidates.append(os.path.join("frontend", "pygame_assets"))
        candidates.append("frontend/pygame_assets")
        candidates.append("pygame_assets")
        candidates.append(os.path.join(os.getcwd(), "frontend", "pygame_assets"))

        chosen = None
        for cand in candidates:
            try:
                if os.path.isdir(cand) and os.listdir(cand):
                    chosen = cand
                    break
            except Exception:
                continue

        if chosen is None:
            # use user-provided dir even if empty so we attempt loads and show errors
            chosen = self.assets_dir or "frontend/pygame_assets"

        print(f"[PygameView] loading assets from: {chosen!r}")
        print(f"[PygameView] expected asset filenames: {list(ASSET_FILENAMES.values())}")

        for key, fname in ASSET_FILENAMES.items():
            path = os.path.join(chosen, fname)
            if not os.path.exists(path):
                print(f"[PygameView] asset missing: {path!r} (key='{key}')")
                self.assets[key] = None
                continue
            # attempt to load via pygame and report any exception
            try:
                img = _load_image(path, (self.tile_size, self.tile_size))
                self.assets[key] = img
                print(f"[PygameView] loaded asset: {path!r} (key='{key}')")
            except Exception as e:
                self.assets[key] = None
                print(f"[PygameView] failed to load asset: {path!r} (key='{key}') -> {e}")

    def world_to_screen(self, x: float, y: float, elevation: float = 0.0) -> Tuple[float, float]:
        """
        Convert world tile coordinates (x,y) and elevation level -> screen pixel coords.
        We offset the y (vertical) by elevation*ELEVATION_PIXEL to create a 2.5D effect.
        The returned coords are top-left of the tile area in pixels.
        """
        sx = x * self.tile_size
        sy = y * self.tile_size - elevation * ELEVATION_PIXEL
        return sx, sy

    def _draw_tile(self, surf, x: int, y: int, tile):
        px = x * self.tile_size
        py = y * self.tile_size
        # base ground (grass)
        img = self.assets.get("grass")
        if img:
            surf.blit(img, (px, py))
        else:
            pygame.draw.rect(surf, (100, 180, 80), (px, py, self.tile_size, self.tile_size))

        # building drawn above ground (when present)
        if getattr(tile, "building", None) is not None:
            img_b = self.assets.get("building")
            if img_b:
                surf.blit(img_b, (px, py))
            else:
                pygame.draw.rect(surf, (120, 70, 40), (px + 4, py + 4, self.tile_size - 8, self.tile_size - 8))
            return  # building occupies tile visually; we don't draw hill under it

        # hill overlay (only visible when no building and optionally no unit)
        if getattr(tile, "elevation", 0):
            img_h = self.assets.get("hill")
            if img_h:
                surf.blit(img_h, (px, py))
            else:
                # simple hill marker
                font = pygame.font.Font(None, 20)
                text = font.render("H", True, (80, 40, 0))
                surf.blit(text, (px + 4, py + 4))

    def _draw_unit_on_canvas(self, surf, unit_snapshot: Dict[str, Any], screen_pos: Tuple[float, float], elevation: float):
        """
        Draw single unit sprite at screen_pos (pixels). screen_pos is top-left of tile area.
        We center unit sprite on the tile and apply elevation offset (sprite drawn higher).
        Also draw a shadow underneath at ground position for depth.
        """
        utype = unit_snapshot["unit_type"]
        owner = unit_snapshot["owner"]
        hp = unit_snapshot.get("hp", None)

        # compute center pixel for tile
        center_x = screen_pos[0] + self.tile_size / 2
        center_y = screen_pos[1] + self.tile_size / 2

        # shadow (prefer asset shadow.png)
        shadow_img = self.assets.get("shadow")
        if shadow_img:
            shadow_rect = shadow_img.get_rect(center=(center_x, center_y + self.tile_size * 0.18 + elevation * (-ELEVATION_PIXEL)))
            surf.blit(shadow_img, shadow_rect.topleft)
        else:
            # fallback: soft ellipse
            shadow_surf = pygame.Surface((self.tile_size // 1, self.tile_size // 3), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), shadow_surf.get_rect())
            shadow_rect = shadow_surf.get_rect(center=(center_x, center_y + self.tile_size * 0.18))
            surf.blit(shadow_surf, shadow_rect.topleft)

        # draw sprite (centered); use unit asset if present
        img = self.assets.get(utype)
        if img:
            # allow sprite to overlap tile vertically (we center on bottom)
            sprite = img
            sprite_rect = sprite.get_rect()
            # place sprite so its bottom-center sits at (center_x, center_y - elevation_pixels)
            bottom_y = center_y - elevation * ELEVATION_PIXEL + (self.tile_size * 0.0)
            sprite_rect.centerx = int(center_x)
            sprite_rect.bottom = int(bottom_y + self.tile_size / 2)
            surf.blit(sprite, sprite_rect.topleft)
        else:
            # fallback circle
            color = (40, 120, 220) if owner == "Player1" else (190, 70, 200)
            r = int(self.tile_size * 0.28)
            pygame.draw.circle(surf, color, (int(center_x), int(center_y - elevation * ELEVATION_PIXEL)), r)

        # HP bar above sprite
        if hp is not None:
            bar_w = int(self.tile_size * 0.6)
            bar_h = 6
            bx = center_x - bar_w / 2
            by = center_y - self.tile_size / 2 - 12 - elevation * ELEVATION_PIXEL
            pct = max(0.0, min(1.0, hp / 100.0))
            pygame.draw.rect(surf, (30, 30, 30), (bx, by, bar_w, bar_h))
            pygame.draw.rect(surf, (50, 200, 50), (bx, by, bar_w * pct, bar_h))

    def run(self, snapshot_queue: "queue.Queue[Dict]", tick_delay: float = 0.5):
        # Ensure display is set up for the renderer (set_mode will create window)
        pygame.display.set_caption("MedievAIl - Pygame 2.5D View")
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))
        font = pygame.font.Font(None, 18)

        self.running = True

        prev_snapshot: Optional[Dict] = None
        curr_snapshot: Optional[Dict] = None
        curr_time = None
        interpolation_duration = max(0.0001, tick_delay)

        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_q:
                        self.running = False

            try:
                snap = snapshot_queue.get_nowait()
                prev_snapshot = curr_snapshot
                curr_snapshot = snap
                curr_time = time.time()
            except queue.Empty:
                pass

            # draw tiles from map (ground layer)
            # background: fill for quick clear
            self.screen.fill((40, 100, 40))
            for y in range(self.map.height):
                for x in range(self.map.width):
                    tile = self.map.grid[x][y]
                    self._draw_tile(self.screen, x, y, tile)

            # determine interpolation factor
            t = 1.0
            if prev_snapshot and curr_snapshot and curr_time is not None:
                elapsed = time.time() - curr_time
                t = min(1.0, max(0.0, elapsed / interpolation_duration))

            # build maps by id
            prev_map = {}
            if prev_snapshot:
                for u in prev_snapshot["units"]:
                    prev_map[u["id"]] = u
            curr_map = {}
            if curr_snapshot:
                for u in curr_snapshot["units"]:
                    curr_map[u["id"]] = u

            all_ids = set(prev_map.keys()).union(curr_map.keys())

            # build draw list with z-key = screen_y so we can sort by depth
            draw_items = []
            for uid in all_ids:
                pu = prev_map.get(uid)
                cu = curr_map.get(uid)
                # if appeared or disappeared, handle accordingly
                if pu and cu:
                    x0, y0 = pu["pos"]
                    x1, y1 = cu["pos"]
                    ix = x0 + (x1 - x0) * t
                    iy = y0 + (y1 - y0) * t
                    # sample elevation from nearest tile
                    ex = int(round(ix))
                    ey = int(round(iy))
                    elev = 0
                    if 0 <= ex < self.map.width and 0 <= ey < self.map.height:
                        elev = int(getattr(self.map.grid[ex][ey], "elevation", 0) or 0)
                    sx, sy = self.world_to_screen(ix, iy, elev)
                    # z-key: sy + small offset so units further down draw later
                    zkey = sy + elev * (-ELEVATION_PIXEL * 0.001)
                    draw_items.append((zkey, cu, (sx, sy), elev))
                elif cu and not pu:
                    # new unit: draw at its pos
                    ix, iy = cu["pos"]
                    ex = int(round(ix))
                    ey = int(round(iy))
                    elev = 0
                    if 0 <= ex < self.map.width and 0 <= ey < self.map.height:
                        elev = int(getattr(self.map.grid[ex][ey], "elevation", 0) or 0)
                    sx, sy = self.world_to_screen(ix, iy, elev)
                    zkey = sy
                    draw_items.append((zkey, cu, (sx, sy), elev))
                elif pu and not cu:
                    # unit disappeared (died) - skip drawing
                    pass

            # sort and draw units by zkey
            draw_items.sort(key=lambda it: it[0])
            for _z, unit_snapshot, screen_pos, elev in draw_items:
                self._draw_unit_on_canvas(self.screen, unit_snapshot, screen_pos, elev)

            # draw UI/log area
            ui_base_y = self.map.height * self.tile_size + 8
            events = (curr_snapshot or prev_snapshot or {}).get("events", [])[-6:]
            for i, line in enumerate(events):
                txt = str(line)[:self.width_px - 8]
                surf_text = font.render(txt, True, (230, 230, 230))
                self.screen.blit(surf_text, (8, ui_base_y + i * 18))
            tick = (curr_snapshot or prev_snapshot or {}).get("tick", 0)
            status = font.render(f"Tick: {tick}   Press Q to quit", True, (220, 220, 220))
            self.screen.blit(status, (8, ui_base_y + 6 * 18))

                        # === ARMY COUNTERS WITH BACKGROUND PANEL ===
            army1 = (curr_snapshot or prev_snapshot or {}).get("army1_types", {})
            army2 = (curr_snapshot or prev_snapshot or {}).get("army2_types", {})

            panel_x = self.width_px - 220      # slightly wider 
            panel_y = 25                       # LOWERED 
            panel_w = 210
            panel_h = 200                      # you can increase if needed

            # draw semi-transparent background
            panel_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surface.fill((20, 20, 20, 180))  # RGBA → 180/255 = semi transparent
            self.screen.blit(panel_surface, (panel_x, panel_y))

            # draw text on top
            title1 = font.render("Army 1:", True, (255, 255, 100))
            self.screen.blit(title1, (panel_x + 10, panel_y + 10))

            y = panel_y + 30
            for unit_type, count in army1.items():
                txt = font.render(f"{unit_type}: {count}", True, (255, 255, 255))
                self.screen.blit(txt, (panel_x + 10, y))
                y += 18

            y += 10
            title2 = font.render("Army 2:", True, (255, 180, 100))
            self.screen.blit(title2, (panel_x + 10, y))
            y += 20

            for unit_type, count in army2.items():
                txt = font.render(f"{unit_type}: {count}", True, (230, 230, 230))
                self.screen.blit(txt, (panel_x + 10, y))
                y += 18

            # === DYNAMIC MINIMAP WITH TRANSPARENCY ===
            minimap_w, minimap_h = 120, 120
            minimap_x, minimap_y = 10, 10

            # create a surface with per-pixel alpha once
            if not hasattr(self, "_minimap_surface"):
                self._minimap_surface = pygame.Surface((minimap_w, minimap_h), pygame.SRCALPHA)
            minimap_surface = self._minimap_surface

            # fill with transparent green (R, G, B, Alpha)
            minimap_surface.fill((50, 180, 50, 120))  # 120/255 = semi-transparent

            units = (curr_snapshot or prev_snapshot or {}).get("units", [])

            map_width = max(1, self.map.width)
            map_height = max(1, self.map.height)

            for u in units:
                pos = u.get("pos")
                if not pos:
                    continue
                x, y = pos
                mini_x = int(x / map_width * minimap_w)
                mini_y = int(y / map_height * minimap_h)
                
                owner = u.get("owner", "")
                color = (255, 255, 0) if owner == "Player1" else (255, 0, 0)
                
                mini_x = min(max(mini_x, 0), minimap_w-1)
                mini_y = min(max(mini_y, 0), minimap_h-1)
                
                pygame.draw.rect(minimap_surface, color, (mini_x, mini_y, 2, 2))

            # optional semi-transparent border
            pygame.draw.rect(minimap_surface, (200, 200, 200, 180), (0, 0, minimap_w, minimap_h), 1)

            # blit minimap with alpha onto the screen
            self.screen.blit(minimap_surface, (minimap_x, minimap_y))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    
def launch_pygame_battle(battle, delay: float = 0.5, assets_dir: str = "frontend/pygame_assets"):
    """
    Launch pygame window and run the battle concurrently.
    - battle: Battle object
    - delay: seconds between ticks (Battle.run delay param)
    - assets_dir: path to image assets
    """
    if pygame is None:
        raise RuntimeError("pygame not available; install via `pip install pygame`")

    # snapshot queue shared between battle thread and graphics thread
    snap_q: "queue.Queue[Dict]" = queue.Queue(maxsize=16)

    def snapshot_callback(game_map):
        """Called every tick by the battle engine. Produces a snapshot."""
        units = []
        army1_types = {}
        army2_types = {}

        for army in (battle.army1, battle.army2):
            for u in army.living_units():
                units.append({
                    "id": getattr(u, "id", None),
                    "unit_type": u.unit_type(),
                    "owner": u.owner,
                    "hp": getattr(u, "hp", None),
                    "pos": tuple(u.position) if u.position is not None else None,
                })

                # count unit types per army
                target_dict = army1_types if army is battle.army1 else army2_types
                ut = u.unit_type()
                target_dict[ut] = target_dict.get(ut, 0) + 1

        try:
            events = list(battle.event_log)[-6:]
        except Exception:
            events = []

        snap = {
            "units": units,
            "tick": getattr(battle, "tick", 0),
            "events": events,
            "army1_types": army1_types,
            "army2_types": army2_types,
        }

        try:
            snap_q.put_nowait(snap)
        except queue.Full:
            pass

    # create view
    view = PygameView(battle.map, tile_size=TILE_SIZE, assets_dir=assets_dir)

    # run battle in separate thread
    def battle_thread_fn():
        try:
            battle.run(delay=delay, display_callback=snapshot_callback)
        except Exception as e:
            print("[Battle thread crashed]:", e)

    bt = threading.Thread(target=battle_thread_fn, daemon=True)
    bt.start()

    # graphics loop
    view.run(snap_q, tick_delay=delay)
