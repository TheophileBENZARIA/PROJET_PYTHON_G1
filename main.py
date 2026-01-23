import argparse

from backend.GameModes.Battle import Battle
from backend.Utils.class_by_name import general_from_name, get_available_generals
from backend.Utils.file_loader import load_mirrored_army_from_file, load_map_from_file
from frontend.Graphics.PyScreen import PyScreen
from frontend.Terminal import Screen


def main():


    def get_available_scenarios() :
        return ""

    parser = argparse.ArgumentParser(description="MedievAIl Battle Simulator")
    subparsers = parser.add_subparsers(dest="mode")

    # ==================== RUN ====================
    run_parser = subparsers.add_parser("run", help="Run a new battle")

    run_parser.add_argument(
        "--ticks", "-t", type=int, default=None,
        help="Maximum ticks to run the battle (omit to run until end)"
    )
    """
    run_parser.add_argument(
        "--delay", "-d", type=float, default=0.5,
        help="Delay (seconds) between ticks; set 0 for headless"
    )
    """

    run_parser.add_argument(
        "--general1", "-g1", type=str, default=None,
        help=f"Comma-separated list of generals.  Available: {', '.join(get_available_generals())}"
    )
    run_parser.add_argument(
        "--general2", "-g2", type=str, default=None,
        help=f"Comma-separated list of generals.  Available: {', '.join(get_available_generals())}"
    )
    run_parser.add_argument(
        "--army_file", type=str,
        help="path of the army repartition file"
    )
    run_parser.add_argument(
        "--map_file", type=str,
        help="path of the map file"
    )
    run_parser.add_argument(
        "--curses", action="store_true", dest="use_curses",
        help="Use curses-based terminal display if available"
    )
    run_parser.add_argument(
        "--pygame", action="store_true", dest="use_pygame",
        help="Use pygame graphical display if available"
    )
    run_parser.add_argument(
        "--assets_dir", type=str, default="frontend/Graphics/pygame_assets",
        help="Directory containing pygame assets (tiles/sprites)"
    )

    # ==================== LANCHESTER ====================
    lan_parser = subparsers.add_parser("lanchester", help="Run a Lanchester scenario (N vs 2N)")
    lan_parser.add_argument(
        "--type", "-u", choices=["melee", "archer"], default="melee",
        help="Unit type:  'melee' (Knight) or 'archer' (Crossbowman)"
    )
    lan_parser.add_argument(
        "--N", "-n", type=int, required=True,
        help="Base number of units on weaker side (will fight 2*N)"
    )
    lan_parser.add_argument(
        "--delay", "-d", type=float, default=0.0,
        help="Delay between ticks (0 for headless fast runs)"
    )
    lan_parser. add_argument(
        "--curses", action="store_true", dest="use_curses",
        help="Use curses terminal display"
    )
    lan_parser.add_argument(
        "--pygame", action="store_true", dest="use_pygame",
        help="Use pygame display if available"
    )
    lan_parser.add_argument(
        "--assets-dir", type=str, default="frontend/pygame_assets",
        help="Directory containing pygame assets (tiles/sprites)"
    )
    lan_parser. add_argument(
        "--save", type=str, default=None,
        help="Optional filename (. json) to save final battle state"
    )

    # ==================== LOAD ====================
    load_parser = subparsers.add_parser("load", help="Load a battle state")
    load_parser.add_argument("filename", help="Name of save file to load")
    load_parser. add_argument(
        "--continue", "-c", action="store_true", dest="do_continue",
        help="Continue running the loaded battle"
    )
    load_parser. add_argument(
        "--ticks", "-t", type=int, default=None,
        help="Maximum ticks to run if continuing (omit to run until end)"
    )
    load_parser.add_argument(
        "--delay", "-d", type=float, default=0.5,
        help="Delay (seconds) between ticks; set 0 for headless"
    )
    load_parser.add_argument(
        "--curses", action="store_true", dest="use_curses",
        help="Use curses-based terminal display if available"
    )
    load_parser. add_argument(
        "--pygame", action="store_true", dest="use_pygame",
        help="Use pygame graphical display if available"
    )
    load_parser.add_argument(
        "--assets-dir", type=str, default="frontend/pygame_assets",
        help="Directory containing pygame assets (tiles/sprites)"
    )

    # ==================== PLACE ====================
    place_parser = subparsers.add_parser("place", help="Place units manually using curses or pygame")
    place_parser.add_argument(
        "--curses", action="store_true", dest="use_curses",
        help="Use curses interface for placement"
    )
    place_parser. add_argument(
        "--pygame", action="store_true", dest="use_pygame",
        help="Use pygame interface for placement"
    )

    # ==================== TOURNAMENT ====================
    tournament_parser = subparsers.add_parser("tournament", help="Run a tournament between generals")
    tournament_parser.add_argument(
        "--generals", "-g", type=str, default=None,
        help=f"Comma-separated list of generals.  Available: {', '.join(get_available_generals())}"
    )
    tournament_parser.add_argument(
        "--scenarios", "-s", type=str, default=None,
        help=f"Comma-separated list of scenarios. Available: {', '.join(get_available_scenarios())}"
    )
    tournament_parser.add_argument(
        "--repeats", "-r", type=int, default=3,
        help="Number of times to repeat each matchup (default: 3)"
    )
    tournament_parser.add_argument(
        "--no-swap", action="store_true",
        help="Don't swap sides between repeats"
    )
    tournament_parser.add_argument(
        "--delay", "-d", type=float, default=0.5,
        help="Delay between ticks during battles (default: 0.5s)"
    )
    tournament_parser. add_argument(
        "--curses", action="store_true", dest="use_curses",
        help="Use curses display for battles"
    )
    tournament_parser. add_argument(
        "--pygame", action="store_true", dest="use_pygame",
        help="Use pygame display for battles"
    )
    tournament_parser. add_argument(
        "--assets-dir", type=str, default="frontend/pygame_assets",
        help="Directory containing pygame assets"
    )
    tournament_parser. add_argument(
        "--headless", action="store_true",
        help="Run battles without display (fast mode, no visuals)"
    )
    tournament_parser. add_argument(
        "--output-dir", "-o", type=str, default="tournament_reports",
        help="Directory to save tournament reports"
    )
    tournament_parser. add_argument(
        "--html", action="store_true",
        help="Generate HTML report"
    )
    tournament_parser. add_argument(
        "--pdf", action="store_true",
        help="Generate PDF report (requires reportlab)"
    )
    tournament_parser. add_argument(
        "--all-reports", "-a", action="store_true",
        help="Generate all report formats (HTML + PDF)"
    )
    tournament_parser. add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress verbose output (don't show standings after each match)"
    )
    tournament_parser. add_argument(
        "--list", action="store_true", dest="list_options",
        help="List available generals and scenarios, then exit"
    )

    args = parser.parse_args()

    gameMode = None
    # ==================== MODE:  RUN ====================

    if args.mode == "run":
        battle = Battle()
        battle.max_tick=args.ticks
        gameMode = battle

        army1,army2 = load_mirrored_army_from_file(args.army_file)
        map = load_map_from_file(args.map_file)

        gameMode.army1 = army1
        gameMode.army2 = army2

        general1_cls = general_from_name(args.general1)
        general2_cls = general_from_name(args.general2)

        army1.general = general1_cls()
        army1.general.army = army1
        army2.general = general2_cls()
        army2.general.army = army2

        gameMode.map = map

        affichage=None
        if args.use_pygame :
            affichage = PyScreen(args.assets_dir)
        elif args.use_curses :
            affichage = Screen()

        gameMode.affichage = affichage


        choice = input("Do you want to save this battle? (y/n): ")
        if choice. lower().startswith("y"):
            gameMode.isSave = True
        
        gameMode.launch()
        gameMode.gameLoop()
        gameMode.end()

        """
    # ==================== MODE: LANCHESTER ====================
    elif args.mode == "lanchester":
        unit_type = args.type
        N = args. N
        width = 40
        height = 20
        game_map, army1, army2 = lanchester(unit_type, N, width=width, height=height)

        general1 = MajorDaft()
        general2 = MajorDaft()
        battle = Battle(game_map, army1, general1, army2, general2)

        print(f"Running Lanchester scenario:  type={unit_type} | N={N} vs 2*N={2*N}")
        print_map(battle.map)
        battle.debug_print_tick()

        battle = run_battle(
            battle=battle,
            delay=args.delay,
            use_curses=args.use_curses,
            use_pygame=args.use_pygame,
            assets_dir=args.assets_dir
        )

        army1_surv = len(battle.army1.living_units())
        army2_surv = len(battle.army2.living_units())
        print(f"Lanchester result: Player1 (N={N}) survivors: {army1_surv}  |  Player2 (2N={2*N}) survivors: {army2_surv}")

        if args.save:
            if args.save.lower().endswith(".json"):
                save_battle_json(battle, args.save)
            else:
                save_battle_pickle(battle, args.save)

    # ==================== MODE: LOAD ====================
    elif args. mode == "load":
        try:
            battle = load_any_battle(args.filename)
        except Exception as e:
            print(f"Failed to load battle '{args.filename}':  {e}")
            return

        print("Map from loaded battle:")
        print_map(battle. map)
        battle.debug_print_tick()
        print(f"Tick: {battle.tick}")

        if args. do_continue:
            battle = run_battle(
                battle=battle,
                max_ticks=args.ticks,
                delay=args. delay,
                use_curses=args.use_curses,
                use_pygame=args.use_pygame,
                assets_dir=args.assets_dir
            )
            choice = input("Do you want to save the continued battle? (y/n): ")
            if choice.lower().startswith("y"):
                choose_save_method_and_save(battle)
        else:
            choice = input("Do you want to continue running this loaded battle now? (y/n): ")
            if choice.lower().startswith("y"):
                battle = run_battle(
                    battle=battle,
                    max_ticks=args.ticks,
                    delay=args.delay,
                    use_curses=args.use_curses,
                    use_pygame=args. use_pygame,
                    assets_dir=args.assets_dir
                )
                choice2 = input("Do you want to save the continued battle? (y/n): ")
                if choice2.lower().startswith("y"):
                    choose_save_method_and_save(battle)

    # ==================== MODE:  PLACE ====================
    elif args.mode == "place":
        base_map = Map(20, 20)
        _place_default_terrain(base_map)

        if args.use_pygame:
            from frontend.pygame_placement import pygame_placement_editor
            from frontend.pygame_view import PygameView

            viewer = PygameView(base_map)
            assets = viewer.assets

            positions = pygame_placement_editor(base_map, assets)
            positions = {k. lower(): v for k, v in positions.items()}
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

    # ==================== MODE: TOURNAMENT ====================
    elif args. mode == "tournament":
        # Handle --list option
        if args.list_options:
            print("\n" + "=" * 50)
            print("AVAILABLE OPTIONS")
            print("=" * 50)
            print("\nGenerals:")
            for g in get_available_generals():
                print(f"  - {g}")
            print("\nScenarios:")
            for s in get_available_scenarios():
                print(f"  - {s}")
            print("\n" + "=" * 50)
            print("EXAMPLE COMMANDS")
            print("=" * 50)
            print("\n# Run full tournament with all generals (visual):")
            print("  python main.py tournament --delay 0.3")
            print("\n# Run Clever vs Daft on triplet scenario:")
            print("  python main.py tournament -g daft,clever -s triplet -r 5")
            print("\n# Fast headless tournament with HTML report:")
            print("  python main.py tournament --headless --html")
            print("\n# Tournament with pygame display:")
            print("  python main.py tournament -g braindead,daft,clever --pygame --delay 0.5")
            print("\n# Full tournament with all reports:")
            print("  python main.py tournament -r 5 --headless --all-reports -o my_reports")
            return

        # Run tournament
        run_tournament_cli(args)
        """
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    
