# main.py
import argparse

from backend.scenarios import simple_knight_duel
from backend.generals import CaptainBraindead, MajorDaft
from backend.battle import Battle
from frontend.terminal_view import print_map

def main():
    parser = argparse.ArgumentParser(description="MedievAIl Battle Simulator")  # Program description
    parser.add_argument("mode", choices=["battle"], help="Run a battle") # Only 'battle' mode implemented for now
    args = parser.parse_args()

    if args.mode == "battle":
        game_map, army1, army2 = simple_knight_duel()   # Simple scenario with 1 Knight vs 1 Knight
        general1 = CaptainBraindead()
        general2 = MajorDaft()

        battle = Battle(game_map, army1, general1, army2, general2)

        print("Initial map:")
        print_map(game_map)

        result = battle.run()
        print(result)


if __name__ == "__main__":
    main()
