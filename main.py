# main.py
import argparse
from backend.scenarios import simple_knight_duel
from backend.generals import CaptainBraindead, MajorDaft
from backend.battle import Battle
from backend.save_manager import save_battle, load_battle
from frontend.terminal_view import print_map


def run_battle():
    """Run a new battle (example: simple Knight duel)"""
    game_map, army1, army2 = simple_knight_duel()
    general1 = CaptainBraindead()
    general2 = MajorDaft()

    battle = Battle(game_map, army1, general1, army2, general2)
    print("Initial map:")
    print_map(game_map)

    result = battle.run()
    print(result)
    return battle


def main():
    parser = argparse.ArgumentParser(description="MedievAIl Battle Simulator")
    subparsers = parser.add_subparsers(dest="mode")

    # run new battle
    subparsers.add_parser("run", help="Run a new battle")

    # save current battle
    save_parser = subparsers.add_parser("save", help="Save a battle state")
    save_parser.add_argument("filename", help="Name of save file (e.g. mybattle.save)")

    # load saved battle
    load_parser = subparsers.add_parser("load", help="Load a battle state")
    load_parser.add_argument("filename", help="Name of save file to load")

    args = parser.parse_args()

    if args.mode == "run":
        battle = run_battle()
        choice = input("Do you want to save this battle? (y/n): ")
        if choice.lower().startswith("y"):
            filename = input("Enter save name (e.g. knight_duel.save): ")
            save_battle(battle, filename)

    elif args.mode == "save":
        print("You can only save an active battle from within 'run' mode.")

    elif args.mode == "load":
        battle = load_battle(args.filename)
        print("Map from loaded battle:")
        print_map(battle.map)
        print(f"Tick: {battle.tick}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
