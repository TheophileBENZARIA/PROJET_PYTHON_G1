Python Project 2025–2026: MedievAIl
BAIttle GenerAIl


1. Run a Single Battle
Basic run (interactive unit selection, MajorDaft vs GeneralClever)
python main.py run

With pygame display
python main. py run --pygame --delay 0.3

With curses display
python main. py run --curses --delay 0.5

Fast headless run
python main.py run --delay 0

2. Tournament Mode
List available generals and scenarios
python main. py tournament --list

Run full tournament with all 3 generals (visual, terminal)
python main.py tournament --delay 0.3

Run tournament with pygame display
python main. py tournament --pygame --delay 0.5

Run tournament with curses display
python main.py tournament --curses --delay 0.2

Fast headless tournament (no visuals)
python main.py tournament --headless

Specific generals only
python main.py tournament -g daft,clever --delay 0.3

Specific scenario only
python main. py tournament -s triplet -r 5

Clever vs Daft on knight_crossbow scenario, 5 repeats
python main. py tournament -g daft,clever -s knight_crossbow -r 5 --delay 0.3

All three generals on all scenarios
python main.py tournament -g braindead,daft,clever -s knight_duel,knight_crossbow,triplet

Generate HTML report
python main.py tournament --headless --html

Generate PDF report (requires reportlab)
python main.py tournament --headless --pdf

Generate all reports
python main. py tournament --headless --all-reports -o my_tournament

Quiet mode (no standings after each match)
python main.py tournament --headless -q --html

Custom output directory
python main. py tournament --headless --html -o tournament_results

3. Lanchester Scenario
Melee (Knight) N=5 vs 2N=10
python main.py lanchester -u melee -n 5

Archer (Crossbowman) N=3 vs 2N=6 with pygame
python main.py lanchester -u archer -n 3 --pygame --delay 0.3

4. Place Units Manually
Curses placement editor
python main.py place --curses

Pygame placement editor
python main.py place --pygame

5. Load Saved Battle
Load and view
python main.py load battle.json

Load and continue
python main.py load battle. json --continue --delay 0.3

Quick Test Commands for GeneralClever
Test Clever vs Daft (recommended)
python main.py tournament -g daft,clever -s triplet -r 3 --delay 0.3

Test all three generals
python main. py tournament -g braindead,daft,clever -r 2 --delay 0.3

Fast benchmark (10 matches each matchup)
python main.py tournament -g daft,clever -r 10 --headless --html

Visual with pygame
python main.py tournament -g daft,clever -s triplet --pygame --delay 0.5
