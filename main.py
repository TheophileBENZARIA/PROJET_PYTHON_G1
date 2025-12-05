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
from frontend.Terminal.terminal_view import print_map, launch_curses_battle


def run_battle(battle: Optional[Battle] = None, max_ticks: Optional[int] = None, delay: float = 0.5, use_curses: bool = False):
    """
    Run a new battle if `battle` is None, otherwise continue running the provided Battle.
    If max_ticks is None the battle runs until one or both armies are eliminated.
    If use_curses=True and a curses frontend exists, the battle will show a curses display.
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

    # If curses mode used, battle.run has already been executed inside the curses wrapper,
    # otherwise `result` was returned above. If curses path was used, we still want to print summary.
    if not use_curses:
        result = result
    else:
        # compute result from the battle object after run
        result = battle.run(delay=0) if False else None  # placeholder to satisfy variable use below
        # The curses run already ran the battle and returned; nothing to do.

    # Print a human-readable summary from the structured result if available
    # If the curses path was used the Battle.run already printed; we attempt to compute final state:
    try:
        result = result or battle.run(delay=0)  # if result None, run a zero-delay run (no-op) to get final summary
    except Exception:
        # best-effort: if running again causes problems, build summary manually
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

    args = parser.parse_args()

    if args.mode == "run":
        battle = run_battle(max_ticks=args.ticks, delay=args.delay, use_curses=args.use_curses)
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
            battle = run_battle(battle=battle, max_ticks=args.ticks, delay=args.delay, use_curses=args.use_curses)
            choice = input("Do you want to save the continued battle? (y/n): ")
            if choice.lower().startswith("y"):
                choose_save_method_and_save(battle)
        else:
            choice = input("Do you want to continue running this loaded battle now? (y/n): ")
            if choice.lower().startswith("y"):
                battle = run_battle(battle=battle, max_ticks=args.ticks, delay=args.delay, use_curses=args.use_curses)
                choice2 = input("Do you want to save the continued battle? (y/n): ")
                if choice2.lower().startswith("y"):
                    choose_save_method_and_save(battle)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()