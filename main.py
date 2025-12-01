# main.py
import logging
import argparse
from typing import Optional
from backend.scenarios import simple_knight_duel
from backend.scenarios import mirrored_knight_crossbow_duel
from backend.generals import CaptainBraindead, MajorDaft
from backend.battle import Battle
from backend.save_manager import (
    save_battle_json,
    load_battle_json,
    save_battle_pickle,
    load_battle_pickle,
)
from frontend.terminal_view import print_map


def run_battle(battle: Optional[Battle] = None, max_ticks: Optional[int] = None, delay: float = 0.5):
    """
    Run a new battle if `battle` is None, otherwise continue running the provided Battle.
    If max_ticks is None the battle runs until one or both armies are eliminated.
    Returns the Battle object (mutated) so callers can save/inspect it.
    """
    if battle is None:
        game_map, army1, army2 = mirrored_knight_crossbow_duel()
        general1 = CaptainBraindead()
        general2 = MajorDaft()
        battle = Battle(game_map, army1, general1, army2, general2)

    print("Initial map:")
    print_map(battle.map)

    battle.debug_print_tick()

    result = battle.run(delay=delay)

    # Print a human-readable summary from the structured result
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

    args = parser.parse_args()

    if args.mode == "run":
        battle = run_battle(max_ticks=args.ticks, delay=args.delay)
        battle.debug_print_tick()
        choice = input("Do you want to save this battle? (y/n): ")
        if choice.lower().startswith("y"):
            choose_save_method_and_save(battle)

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
            battle = run_battle(battle=battle, max_ticks=args.ticks, delay=args.delay)
            choice = input("Do you want to save the continued battle? (y/n): ")
            if choice.lower().startswith("y"):
                choose_save_method_and_save(battle)
        else:
            choice = input("Do you want to continue running this loaded battle now? (y/n): ")
            if choice.lower().startswith("y"):
                battle = run_battle(battle=battle, max_ticks=args.ticks, delay=args.delay)
                choice2 = input("Do you want to save the continued battle? (y/n): ")
                if choice2.lower().startswith("y"):
                    choose_save_method_and_save(battle)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()