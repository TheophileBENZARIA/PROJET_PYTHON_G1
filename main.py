# main.py
import backend
import logging
import argparse
from typing import Optional, Dict, Tuple, List, Type
from backend.generals import CaptainBraindead, MajorDaft
from backend.battle import Battle
from backend.save_manager import (
    save_battle_json,
    load_battle_json,
    save_battle_pickle,
    load_battle_pickle,
)
from frontend.Terminal.terminal_view import print_map, launch_curses_battle
# new pygame launcher import (graceful failure if pygame frontend not present)
try:
    from frontend.pygame_view import launch_pygame_battle
except Exception:
    launch_pygame_battle = None

# new imports for interactive scenario construction
from backend.map import Map
from backend.units import Knight, Pikeman, Crossbowman

# Import Lanchester scenario generator
from backend.scenarios import lanchester

# available unit types (lowercase keys used internally)
_UNIT_CLASSES = {
    "knight": Knight,
    "pikeman": Pikeman,
    "crossbowman": Crossbowman,
}

CASTLE_HP = 300

def _place_castles_on_map(game_map: Map):
    """
    Place a Player1 castle near the top center and a Player2 castle near the bottom center.
    Castles are placed 'behind the troops' so top/bottom rows are used.
    """
    cx = game_map.width // 2
    top_y = 0
    bot_y = game_map.height - 1
    # set building dicts with hp and owner
    game_map.grid[cx][top_y].building = {"type": "castle", "owner": "Player1", "hp": CASTLE_HP, "max_hp": CASTLE_HP}
    game_map.grid[cx][bot_y].building = {"type": "castle", "owner": "Player2", "hp": CASTLE_HP, "max_hp": CASTLE_HP}


def ask_for_composition_interactive() -> Dict[str, int]:
    """
    Prompt the user for the number of each available unit type, one by one.
    """
    print("Please select the number of units for one army (armies are mirrored).")
    print("Enter a non-negative integer for each unit type. Press Enter for 0.")
    composition: Dict[str, int] = {}

    # keep a deterministic order for prompting
    prompt_order = ["knight", "pikeman", "crossbowman"]

    for key in prompt_order:
        display_name = key.title()
        while True:
            try:
                raw = input(f"{display_name}: ").strip()
            except EOFError:
                raw = ""
            if raw == "":
                count = 0
                break
            try:
                count = int(raw)
                if count < 0:
                    print("Please enter a non-negative integer.")
                    continue
                break
            except ValueError:
                print("Invalid number, please enter a non-negative integer (or press Enter for 0).")
        if count > 0:
            composition[key] = count

    # If composition ended up empty, provide a small default so simulation runs
    if not composition:
        print("No units selected; using default composition: Knight:1, Crossbowman:1")
        composition = {"knight": 1, "crossbowman": 1}

    # show summary and confirm
    print("\nSelected composition for one army:")
    for name, cnt in composition.items():
        print(f"  {name.title()}: {cnt}")
    while True:
        confirm = input("Proceed with this composition? (Y/n): ").strip().lower()
        if confirm in ("", "y", "yes"):
            break
        if confirm in ("n", "no"):
            print("Let's re-enter the composition.")
            return ask_for_composition_interactive()
        print("Please answer 'y' or 'n' (or press Enter for yes).")

    return composition


def _chunk_list(lst: List[Type], size: int) -> List[List[Type]]:
    """Split list into chunks of at most size (preserving order)."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def _place_default_terrain(game_map: Map):
    """
    Add a few buildings and hills to the map so they are present at simulation start.
    - buildings set tile.building to a non-None value (e.g. 'building')
    - hills set tile.elevation to an integer > 0
    This uses a small, deterministic layout suitable for testing.
    """
    w, h = game_map.width, game_map.height

    # Example building cluster in the middle of the map
    building_coords = [
        (w // 2 - 2, h // 2), (w // 2 - 1, h // 2),
        (w // 2,     h // 2), (w // 2 + 1, h // 2),
        # a small outpost slightly above center
        (w // 2,     h // 2 - 3),
    ]

    for x, y in building_coords:
        if 0 <= x < w and 0 <= y < h:
            game_map.grid[x][y].building = "building"

    # Example hills distributed so crossbowmen can use them
    hill_coords = [
        (3, 4), (w - 4, 4),       # top-left and top-right hills
        (3, h - 5), (w - 4, h - 5),  # bottom-left and bottom-right hills
        (w // 2, h // 2 - 6),     # hill in front of center (for tactical tests)
    ]
    # give some hills elevation 1 or 2
    for idx, (x, y) in enumerate(hill_coords):
        if 0 <= x < w and 0 <= y < h:
            game_map.grid[x][y].elevation = 1 + (idx % 2)  # alternate 1 and 2


def build_mirrored_battle_from_composition(comp: Dict[str, int], width: int = 20, height: int = 20
                                          ) -> Tuple[Map, 'backend.army.Army', 'backend.army.Army']:
    """
    Given a composition dict (unitname -> count) build a Map and two mirrored armies.
    Units are placed in rows per army. Crossbowmen (ranged) are placed in back rows,
    melee units (Knight, Pikeman, etc.) are placed in front rows. If the requested
    composition is larger than available capacity it will be truncated (prefer keeping
    melee/frontline units) and a warning is printed.
    """
    game_map = Map(width, height)

    # Place default terrain before units so unit placement avoids buildings
    _place_default_terrain(game_map)

    from backend.army import Army
    army1 = Army("Player1")
    army2 = Army("Player2")

    # Split requested units into melee (front) and ranged (back) lists
    melee_classes: List[Type] = []
    ranged_classes: List[Type] = []

    for name, count in comp.items():
        cls = _UNIT_CLASSES.get(name)
        if not cls:
            continue
        for _ in range(count):
            # treat Crossbowman as ranged, others as melee by default
            if cls is Crossbowman:
                ranged_classes.append(cls)
            else:
                melee_classes.append(cls)

    total_units = len(melee_classes) + len(ranged_classes)
    if total_units == 0:
        # fallback simple composition
        melee_classes = [Knight]
        ranged_classes = [Crossbowman]
        total_units = 2

    # Placement planning
    max_cols = width  # maximum units per row

    # How many rows are available per side?
    # Reserve at least 1 row in the very top/bottom and leave a center gap of at least 1 row.
    # available_half_rows roughly (height-1)/2 - 1
    available_half_rows = max(1, (height - 1) // 2 - 1)

    capacity = available_half_rows * max_cols
    if total_units > capacity:
        # Truncate: prefer to keep melee units (front) first, then keep as many ranged as fit.
        print(f"Warning: composition too large for map {width}x{height}. Requested {total_units} units per army but only {capacity} fit.")
        # compute how many melee we can keep (prefer all melee up to capacity)
        keep_melee = min(len(melee_classes), capacity)
        remaining_capacity = capacity - keep_melee
        keep_ranged = min(len(ranged_classes), remaining_capacity)
        melee_classes = melee_classes[:keep_melee]
        ranged_classes = ranged_classes[:keep_ranged]
        total_units = keep_melee + keep_ranged

    # Now create rows: ranged rows go to back (top of top-half), melee rows to front (bottom of top-half)
    ranged_rows = _chunk_list(ranged_classes, max_cols)
    melee_rows = _chunk_list(melee_classes, max_cols)

    # Combined rows order for Player1 (top -> down): ranged_rows first (back), then melee_rows (front)
    rows: List[List[Type]] = []
    rows.extend(ranged_rows)
    rows.extend(melee_rows)

    required_rows = len(rows)
    if required_rows == 0:
        # nothing to place
        # still place castles
        _place_castles_on_map(game_map)
        return game_map, army1, army2

    # center the rows block inside the available top-half vertically
    top_half_start = 1  # leave 1 row margin at top
    top_half_height = available_half_rows
    top_start_row = top_half_start + max(0, (top_half_height - required_rows) // 2)

    # Helper: place a given rows-of-types block for an army starting at a y (increasing rows downward)
    def place_rows_for_army(row_types: List[List[Type]], owner: str, start_row: int, army):
        for r_idx, row_types_list in enumerate(row_types):
            y = start_row + r_idx
            n = len(row_types_list)
            # center horizontally
            start_x = max(0, (width - n) // 2)
            for i, cls in enumerate(row_types_list):
                inst = cls(owner)
                tx = start_x + i
                # try placement at tx,y, else scan left/right then whole map
                placed = False
                if 0 <= tx < width and 0 <= y < height and game_map.grid[tx][y].is_empty():
                    try:
                        game_map.place_unit(inst, tx, y)
                        army.add_unit(inst)
                        placed = True
                    except Exception:
                        placed = False
                if not placed:
                    # scan same row for nearest empty tile
                    for d in range(1, width):
                        for candidate in (tx + d, tx - d):
                            if 0 <= candidate < width and game_map.grid[candidate][y].is_empty():
                                game_map.place_unit(inst, candidate, y)
                                army.add_unit(inst)
                                placed = True
                                break
                        if placed:
                            break
                if not placed:
                    # fallback: scan whole map
                    found = False
                    for yy in range(height):
                        for xx in range(width):
                            if game_map.grid[xx][yy].is_empty():
                                game_map.place_unit(inst, xx, yy)
                                army.add_unit(inst)
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        raise RuntimeError("Map full — cannot place unit")

    # Place Player1 rows as computed (ranged rows first at top of the block, melee below)
    place_rows_for_army(rows, "Player1", top_start_row, army1)

    # For Player2 (mirrored in bottom half): we want mirrored layout but with back rows (ranged) further from enemy (i.e., at bottom of block).
    # Compute bottom_start_row so the block is vertically centered in bottom half
    bottom_start_row = height - 1 - (top_start_row + required_rows - 1)

    # For Player2, place rows in reverse order so melee rows are closest to the center (top of bottom block)
    mirrored_rows_for_p2 = list(reversed(rows))
    place_rows_for_army(mirrored_rows_for_p2, "Player2", bottom_start_row, army2)

    # Place castles behind the troops
    _place_castles_on_map(game_map)

    return game_map, army1, army2

def build_mirrored_battle_from_custom_positions(positions, width=20, height=20):
    from backend.map import Map
    from backend.army import Army
    from backend.units import Knight, Pikeman, Crossbowman

    _UNIT_CLASSES = {
        "knight": Knight,
        "pikeman": Pikeman,
        "crossbowman": Crossbowman
    }

    game_map = Map(width, height)

    # terrain par défaut
    _place_default_terrain(game_map)

    army1 = Army("Player1")
    army2 = Army("Player2")

    for unit_type, coords in positions.items():
        cls = _UNIT_CLASSES[unit_type]
        for (x, y) in coords:

            # --- Player1 ---
            u1 = cls("Player1")
            tile1 = game_map.grid[x][y]
            if tile1.is_empty():
                game_map.place_unit(u1, x, y)
                army1.add_unit(u1)
            else:
                raise ValueError(f"Tile P1 {x,y} non vide")

            # --- Player2 (miroir vertical) ---
            my = height - 1 - y
            u2 = cls("Player2")
            tile2 = game_map.grid[x][my]
            if tile2.is_empty():
                game_map.place_unit(u2, x, my)
                army2.add_unit(u2)
            else:
                raise ValueError(f"Tile P2 {x,my} non vide")

    # place castles behind troops so they always appear in normal battles
    _place_castles_on_map(game_map)

    return game_map, army1, army2


def run_battle(battle: Optional[Battle] = None, max_ticks: Optional[int] = None, delay: float = 0.5,
               use_curses: bool = False, use_pygame: bool = False, assets_dir: Optional[str] = None):
    """
    Run a new battle if `battle` is None, otherwise continue running the provided Battle.
    If use_pygame=True and the pygame frontend is available, the pygame UI will run the simulation.
    """
    if battle is None:
        # ask user for composition for one army (interactive per-unit prompts)
        comp = ask_for_composition_interactive()
        game_map, army1, army2 = build_mirrored_battle_from_composition(comp, width=20, height=20)
        general1 = CaptainBraindead()
        general2 = MajorDaft()
        battle = Battle(game_map, army1, general1, army2, general2)

    print("Initial map:")
    print_map(battle.map)

    battle.debug_print_tick()

    # If pygame requested, prefer it over curses
    if use_pygame:
        if launch_pygame_battle is None:
            print("Pygame frontend is not available (pygame not installed or frontend missing). Falling back to terminal.")
            use_pygame = False
        else:
            try:
                launch_pygame_battle(battle, delay=delay, assets_dir=assets_dir or "frontend/pygame_assets")
            except Exception as e:
                print("Failed to launch pygame display, falling back to standard loop:", e)
                result = battle.run(delay=delay)
                return battle
            # pygame run already executed the battle via the background thread; return mutated battle
            return battle

    if use_curses:
        # Launch curses-based UI which will run the battle inside it.
        try:
            launch_curses_battle(battle, delay=delay)
        except Exception as e:
            print("Failed to launch curses display, falling back to standard loop:", e)
            result = battle.run(delay=delay)
            return battle
    else:
        result = battle.run(delay=delay)

    # Build a human-readable summary from resulting battle state
    try:
        result = result or battle.run(delay=0)
    except Exception:
        army1_alive = bool(battle.army1.living_units())
        army2_alive = bool(battle.army2.living_units())
        if army1_alive and not army2_alive:
            winner = battle.general1.name
        elif army2_alive and not army1_alive:
            winner = battle.general2.name
        else:
            winner = "Draw"
        surviving_units = {battle.army1.owner: [u.to_dict() for u in battle.army1.living_units()],
                           battle.army2.owner: [u.to_dict() for u in battle.army2.living_units()]}
        class _R: pass
        result = _R()
        result.winner = winner
        result.ticks = battle.tick
        result.surviving_units = surviving_units

    print("\n--- Battle summary ---")
    print(f"Winner: {result.winner}")
    print(f"Ticks simulated: {result.ticks}")
    for owner, units in result.surviving_units.items():
        print(f"{owner} surviving units: {len(units)}")
    print("----------------------\n")

    return battle


def choose_save_method_and_save(battle: Battle):
    filename = input("Enter save name (e.g. knight_duel.json): ").strip()
    if not filename:
        print("No filename provided, skipping save.")
        return

    if filename.lower().endswith(".json"):
        save_battle_json(battle, filename)
    else:
        save_battle_pickle(battle, filename)


def load_any_battle(filename: str) -> Battle:
    if filename.lower().endswith(".json"):
        return load_battle_json(filename)
    else:
        return load_battle_pickle(filename)


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    parser = argparse.ArgumentParser(description="MedievAIl Battle Simulator")
    subparsers = parser.add_subparsers(dest="mode")

    # run new battle
    run_parser = subparsers.add_parser("run", help="Run a new battle")
    run_parser.add_argument(
        "--ticks", "-t", type=int, default=None, help="Maximum ticks to run the battle (omit to run until end)"
    )
    run_parser.add_argument(
        "--delay", "-d", type=float, default=0.5, help="Delay (seconds) between ticks; set 0 for headless"
    )
    run_parser.add_argument(
        "--curses", action="store_true", dest="use_curses", help="Use curses-based terminal display if available"
    )
    run_parser.add_argument(
        "--pygame", action="store_true", dest="use_pygame", help="Use pygame graphical display if available"
    )
    run_parser.add_argument(
        "--assets-dir", type=str, default="frontend/pygame_assets", help="Directory containing pygame assets (tiles/sprites)"
    )

    # lanchester scenario
    lan_parser = subparsers.add_parser("lanchester", help="Run a Lanchester scenario (N vs 2N)")
    lan_parser.add_argument("--type", "-u", choices=["melee", "archer"], default="melee",
                            help="Unit type: 'melee' (Knight) or 'archer' (Crossbowman)")
    lan_parser.add_argument("--N", "-n", type=int, required=True, help="Base number of units on weaker side (will fight 2*N)")
    lan_parser.add_argument("--delay", "-d", type=float, default=0.0, help="Delay between ticks (0 for headless fast runs)")
    lan_parser.add_argument("--curses", action="store_true", dest="use_curses", help="Use curses terminal display")
    lan_parser.add_argument("--pygame", action="store_true", dest="use_pygame", help="Use pygame display if available")
    lan_parser.add_argument("--assets-dir", type=str, default="frontend/pygame_assets", help="Directory containing pygame assets (tiles/sprites)")
    lan_parser.add_argument("--save", type=str, default=None, help="Optional filename (.json) to save final battle state")

    # load saved battle and optionally continue running it
    load_parser = subparsers.add_parser("load", help="Load a battle state")
    load_parser.add_argument("filename", help="Name of save file to load")
    load_parser.add_argument(
        "--continue",
        "-c",
        action="store_true",
        dest="do_continue",
        help="Continue running the loaded battle",
    )
    load_parser.add_argument(
        "--ticks", "-t", type=int, default=None, help="Maximum ticks to run if continuing (omit to run until end)"
    )
    load_parser.add_argument(
        "--delay", "-d", type=float, default=0.5, help="Delay (seconds) between ticks; set 0 for headless"
    )
    load_parser.add_argument(
        "--curses", action="store_true", dest="use_curses", help="Use curses-based terminal display if available"
    )
    load_parser.add_argument(
        "--pygame", action="store_true", dest="use_pygame", help="Use pygame graphical display if available"
    )
    load_parser.add_argument(
        "--assets-dir", type=str, default="frontend/pygame_assets", help="Directory containing pygame assets (tiles/sprites)"
    )


    place_parser = subparsers.add_parser("place", help="Place units manually using curses")
    place_parser.add_argument(
    "--curses",
    action="store_true",
    dest="use_curses",
    help="Use curses interface for placement"
    )
    
    place_parser.add_argument(
    "--pygame",
    action="store_true",
    dest="use_pygame",
    help="Use pygame interface for placement"
    )

    args = parser.parse_args()

    if args.mode == "run":
        battle = run_battle(max_ticks=args.ticks, delay=args.delay,
                            use_curses=args.use_curses, use_pygame=args.use_pygame, assets_dir=args.assets_dir)
        battle.debug_print_tick()
        choice = input("Do you want to save this battle? (y/n): ")
        if choice.lower().startswith("y"):
            choose_save_method_and_save(battle)

    elif args.mode == "lanchester":
        # Build scenario and run it
        unit_type = args.type
        N = args.N
        width = 40
        height = 20
        game_map, army1, army2 = lanchester(unit_type, N, width=width, height=height)

        # Use active generals that will honor aggro/targets
        # For Lanchester experiments keep both generals the same for symmetry
        general1 = MajorDaft()
        general2 = MajorDaft()
        battle = Battle(game_map, army1, general1, army2, general2)

        print(f"Running Lanchester scenario: type={unit_type} | N={N} vs 2*N={2*N}")
        print_map(battle.map)
        battle.debug_print_tick()

        # Prefer headless fast runs by default (delay from args)
        battle = run_battle(battle=battle, delay=args.delay, use_curses=args.use_curses, use_pygame=args.use_pygame, assets_dir=args.assets_dir)

        # After run, print final counts and optionally save
        army1_surv = len(battle.army1.living_units())
        army2_surv = len(battle.army2.living_units())
        print(f"Lanchester result: Player1 (N={N}) survivors: {army1_surv}  |  Player2 (2N={2*N}) survivors: {army2_surv}")

        if args.save:
            if args.save.lower().endswith(".json"):
                save_battle_json(battle, args.save)
            else:
                save_battle_pickle(battle, args.save)

    elif args.mode == "load":
        try:
            battle = load_any_battle(args.filename)
        except Exception as e:
            print(f"Failed to load battle '{args.filename}': {e}")
            return

        print("Map from loaded battle:")
        print_map(battle.map)
        battle.debug_print_tick()
        print(f"Tick: {battle.tick}")

        if args.do_continue:
            battle = run_battle(battle=battle, max_ticks=args.ticks, delay=args.delay,
                                use_curses=args.use_curses, use_pygame=args.use_pygame, assets_dir=args.assets_dir)
            choice = input("Do you want to save the continued battle? (y/n): ")
            if choice.lower().startswith("y"):
                choose_save_method_and_save(battle)
        else:
            choice = input("Do you want to continue running this loaded battle now? (y/n): ")
            if choice.lower().startswith("y"):
                battle = run_battle(battle=battle, max_ticks=args.ticks, delay=args.delay,
                                    use_curses=args.use_curses, use_pygame=args.use_pygame, assets_dir=args.assets_dir)
                choice2 = input("Do you want to save the continued battle? (y/n): ")
                if choice2.lower().startswith("y"):
                    choose_save_method_and_save(battle)

    
    elif args.mode == "place":

        base_map = Map(20, 20)
        _place_default_terrain(base_map)

        # decide which placement interface to use
        if args.use_pygame:
            from frontend.pygame_placement import pygame_placement_editor
            from frontend.pygame_view import PygameView
        
            # load assets
            viewer = PygameView(base_map)
            assets = viewer.assets

            positions = pygame_placement_editor(base_map, assets)
            positions = {k.lower(): v for k, v in positions.items()}
        else:
            from frontend.Terminal.placement import curses_placement_editor
            positions = curses_placement_editor(base_map)

        if positions is None:
            print("Placement cancelled.")
            return

        print("Building armies...")
        game_map, army1, army2 = build_mirrored_battle_from_custom_positions(positions)

        battle = Battle(
            game_map,
            army1, CaptainBraindead(),
            army2, MajorDaft()
        )

        print("Launching battle...")

        if args.use_pygame:
            launch_pygame_battle(battle)
        else:
            launch_curses_battle(battle)
    
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()