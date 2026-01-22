# backend/tournament.py
"""
Tournament system for running multiple battles between generals and generating reports.
"""
from typing import List, Dict, Tuple, Callable, Optional
from dataclasses import dataclass, field
import os
import itertools
from datetime import datetime

from backend.Class.battle import Battle
from backend.Class.army import Army
from backend.Class.map import Map
from backend.scenarios import (
    simple_knight_duel,
    mirrored_knight_crossbow_duel,
    mirrored_triplet_pikeman_knight_crossbow_duel,
)
from backend.generals import (
    General,
    CaptainBraindead,
    MajorDaft,
    GeneralClever,
)


@dataclass
class MatchResult:
    """Result of a single match in the tournament."""
    scenario: str
    general1_name: str
    general2_name:  str
    winner:  str
    ticks: int
    army1_survivors: int
    army2_survivors: int

    def is_draw(self) -> bool:
        return self.winner == "Draw"


@dataclass
class TournamentResult:
    """Aggregated results of a tournament."""
    matches: List[MatchResult] = field(default_factory=list)
    victories: Dict[str, int] = field(default_factory=dict)
    draws: int = 0

    def add_match(self, match:  MatchResult):
        self.matches. append(match)
        if match.is_draw():
            self.draws += 1
        else:
            self.victories[match.winner] = self.victories.get(match.winner, 0) + 1

    def get_leaderboard(self) -> List[Tuple[str, int]]:
        """Return sorted list of (general_name, wins) by wins descending."""
        return sorted(self.victories.items(), key=lambda x: x[1], reverse=True)

    def summary(self) -> str:
        """Return a text summary of the tournament."""
        lines = []
        lines.append("=" * 50)
        lines.append("TOURNAMENT SUMMARY")
        lines.append("=" * 50)
        lines.append(f"Total matches: {len(self.matches)}")
        lines.append(f"Total draws: {self.draws}")
        lines.append("")
        lines.append("Leaderboard:")
        for rank, (name, wins) in enumerate(self.get_leaderboard(), 1):
            lines.append(f"  {rank}.  {name}: {wins} win(s)")
        lines.append("=" * 50)
        return "\n".join(lines)


# --- Available scenarios registry ---
SCENARIO_REGISTRY:  Dict[str, Callable[[], Tuple[Map, Army, Army]]] = {
    "knight_duel": simple_knight_duel,
    "knight_crossbow":  mirrored_knight_crossbow_duel,
    "triplet":  mirrored_triplet_pikeman_knight_crossbow_duel,
}

# --- Available generals registry ---
GENERAL_REGISTRY:  Dict[str, Callable[[], General]] = {
    "braindead": CaptainBraindead,
    "daft": MajorDaft,
    "clever": GeneralClever,
}


def get_available_scenarios() -> List[str]:
    """Return list of available scenario names."""
    return list(SCENARIO_REGISTRY.keys())


def get_available_generals() -> List[str]:
    """Return list of available general names."""
    return list(GENERAL_REGISTRY.keys())


def run_single_match(
    scenario_name: str,
    scenario_func: Callable[[], Tuple[Map, Army, Army]],
    general1:  General,
    general2: General,
    match_number: int,
    total_matches: int,
    delay:  float = 0.5,
    use_curses: bool = False,
    use_pygame: bool = False,
    assets_dir: str = "frontend/pygame_assets",
    headless: bool = False,
) -> MatchResult:
    """
    Run a single match between two generals.
    """
    # Create fresh scenario
    game_map, army1, army2 = scenario_func()

    # Create battle
    battle = Battle(game_map, army1, general1, army2, general2)

    # Display match header
    print("\n" + "=" * 60)
    print(f"MATCH {match_number}/{total_matches}")
    print(f"Scenario:  {scenario_name}")
    print(f"{general1.name} (Player1) vs {general2.name} (Player2)")
    print("=" * 60)

    if headless:
        # Run without display
        result = battle.run(delay=0)
    elif use_pygame:
        try:
            from frontend.pygame_view import launch_pygame_battle
            if launch_pygame_battle is not None:
                launch_pygame_battle(battle, delay=delay, assets_dir=assets_dir)
            else:
                print("Pygame not available, falling back to standard display")
                result = battle.run(delay=delay)
        except Exception as e:
            print(f"Pygame display failed: {e}, falling back to standard display")
            result = battle.run(delay=delay)
    elif use_curses:
        try:
            from frontend.Terminal. terminal_view import launch_curses_battle
            launch_curses_battle(battle, delay=delay)
        except Exception as e:
            print(f"Curses display failed: {e}, falling back to standard display")
            result = battle.run(delay=delay)
    else:
        from frontend.Terminal.terminal_view import print_map

        print("\nInitial map:")
        print_map(battle.map)

        result = battle.run(delay=delay)

        print("\nFinal map:")
        print_map(battle. map)

    # Get result
    if not hasattr(result, 'winner'):
        army1_alive = bool(battle.army1.living_units())
        army2_alive = bool(battle.army2.living_units())
        if battle._victory is not None:
            winner = battle._victory
        elif army1_alive and not army2_alive:
            winner = general1.name
        elif army2_alive and not army1_alive:
            winner = general2.name
        else:
            winner = "Draw"
        ticks = battle.tick
    else:
        winner = result.winner
        ticks = result.ticks

    army1_survivors = len(battle.army1.living_units())
    army2_survivors = len(battle.army2.living_units())

    match_result = MatchResult(
        scenario=scenario_name,
        general1_name=general1.name,
        general2_name=general2.name,
        winner=winner,
        ticks=ticks,
        army1_survivors=army1_survivors,
        army2_survivors=army2_survivors,
    )

    print("\n" + "-" * 40)
    print(f"MATCH RESULT: {winner} wins!")
    print(f"Duration: {ticks} ticks")
    print(f"Survivors - {general1.name}: {army1_survivors}, {general2.name}: {army2_survivors}")
    print("-" * 40)

    if not headless:
        try:
            input("\nPress Enter to continue to next match...")
        except EOFError:
            pass

    return match_result


def run_tournament(
    generals: Optional[List[str]] = None,
    scenarios: Optional[List[str]] = None,
    num_repeats: int = 3,
    swap_sides: bool = True,
    delay:  float = 0.5,
    use_curses: bool = False,
    use_pygame: bool = False,
    assets_dir: str = "frontend/pygame_assets",
    headless: bool = False,
    verbose: bool = True,
) -> TournamentResult:
    """
    Run a full tournament between generals across scenarios.
    """
    if generals is None:
        generals = list(GENERAL_REGISTRY.keys())

    general_instances = []
    for name in generals:
        if name not in GENERAL_REGISTRY:
            raise ValueError(f"Unknown general: {name}. Available: {list(GENERAL_REGISTRY.keys())}")
        general_instances.append((name, GENERAL_REGISTRY[name]))

    if scenarios is None:
        scenarios = list(SCENARIO_REGISTRY.keys())

    scenario_funcs = []
    for name in scenarios:
        if name not in SCENARIO_REGISTRY:
            raise ValueError(f"Unknown scenario: {name}. Available: {list(SCENARIO_REGISTRY.keys())}")
        scenario_funcs.append((name, SCENARIO_REGISTRY[name]))

    num_matchups = len(general_instances) ** 2
    total_matches = len(scenario_funcs) * num_matchups * num_repeats

    tournament_result = TournamentResult()

    print("\n" + "=" * 60)
    print("TOURNAMENT STARTING")
    print("=" * 60)
    print(f"Generals: {[g[0] for g in general_instances]}")
    print(f"Scenarios: {[s[0] for s in scenario_funcs]}")
    print(f"Repeats per matchup: {num_repeats}")
    print(f"Swap sides: {swap_sides}")
    print(f"Total matches: {total_matches}")
    print(f"Display mode: {'Headless' if headless else ('Pygame' if use_pygame else ('Curses' if use_curses else 'Terminal'))}")
    print("=" * 60)

    if not headless:
        try:
            input("\nPress Enter to start the tournament...")
        except EOFError:
            pass

    match_count = 0

    for scenario_name, scenario_func in scenario_funcs:
        print(f"\n{'#' * 60}")
        print(f"# SCENARIO: {scenario_name. upper()}")
        print(f"{'#' * 60}")

        for (name_a, cls_a), (name_b, cls_b) in itertools.product(general_instances, repeat=2):
            for repeat in range(num_repeats):
                match_count += 1

                if swap_sides and repeat % 2 == 1:
                    gen1, gen2 = cls_b(), cls_a()
                else:
                    gen1, gen2 = cls_a(), cls_b()

                match_result = run_single_match(
                    scenario_name=scenario_name,
                    scenario_func=scenario_func,
                    general1=gen1,
                    general2=gen2,
                    match_number=match_count,
                    total_matches=total_matches,
                    delay=delay,
                    use_curses=use_curses,
                    use_pygame=use_pygame,
                    assets_dir=assets_dir,
                    headless=headless,
                )

                tournament_result. add_match(match_result)

                if verbose:
                    print("\nCurrent Standings:")
                    for name, wins in tournament_result.get_leaderboard():
                        print(f"   {name}:  {wins} win(s)")

    print("\n" + tournament_result.summary())

    return tournament_result


def generate_html_report(result: TournamentResult, output_path: str):
    """Generate an HTML report of the tournament results."""
    html_content = []
    html_content.append("<!DOCTYPE html>")
    html_content.append("<html><head>")
    html_content.append("<meta charset='utf-8'>")
    html_content.append("<title>Tournament Report</title>")
    html_content. append("<style>")
    html_content.append("""
        body { font-family: Arial, sans-serif; margin: 40px; background:  #f5f5f5; }
        h1 { color:  #333; border-bottom: 2px solid #666; padding-bottom:  10px; }
        h2 { color: #555; margin-top: 30px; }
        table { border-collapse:  collapse; width: 100%; margin: 20px 0; background: white; }
        th, td { border:  1px solid #ddd; padding:  12px; text-align: left; }
        th { background-color: #4a4a4a; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f1f1f1; }
        .winner { color: #2e7d32; font-weight: bold; }
        .draw { color: #f57c00; font-style: italic; }
        .leaderboard { max-width: 400px; }
        .leaderboard td: first-child { font-weight: bold; }
        .summary { background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }
    """)
    html_content.append("</style>")
    html_content.append("</head><body>")

    html_content.append("<h1>Tournament Report</h1>")
    html_content.append(f"<p>Generated:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")

    html_content.append("<div class='summary'>")
    html_content.append(f"<strong>Total Matches: </strong> {len(result.matches)}<br>")
    html_content.append(f"<strong>Total Draws:</strong> {result. draws}")
    html_content.append("</div>")

    html_content. append("<h2>Leaderboard</h2>")
    html_content.append("<table class='leaderboard'>")
    html_content.append("<tr><th>Rank</th><th>General</th><th>Wins</th></tr>")
    for rank, (name, wins) in enumerate(result.get_leaderboard(), 1):
        html_content.append(f"<tr><td>{rank}</td><td>{name}</td><td>{wins}</td></tr>")
    html_content. append("</table>")

    html_content.append("<h2>Match Results</h2>")
    html_content.append("<table>")
    html_content.append("<tr><th>#</th><th>Scenario</th><th>General 1</th><th>General 2</th><th>Winner</th><th>Ticks</th><th>Survivors (G1/G2)</th></tr>")

    for i, match in enumerate(result.matches, 1):
        winner_class = "draw" if match.is_draw() else "winner"
        html_content.append(f"<tr>")
        html_content.append(f"<td>{i}</td>")
        html_content. append(f"<td>{match.scenario}</td>")
        html_content. append(f"<td>{match.general1_name}</td>")
        html_content.append(f"<td>{match.general2_name}</td>")
        html_content.append(f"<td class='{winner_class}'>{match.winner}</td>")
        html_content. append(f"<td>{match.ticks}</td>")
        html_content.append(f"<td>{match. army1_survivors} / {match.army2_survivors}</td>")
        html_content.append(f"</tr>")

    html_content.append("</table>")
    html_content. append("</body></html>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

    print(f"HTML report generated: {output_path}")


def generate_pdf_report(result:  TournamentResult, output_path: str):
    """Generate a PDF report of the tournament results."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab. lib.styles import getSampleStyleSheet
        from reportlab. lib.units import cm
        from reportlab.lib import colors
    except ImportError:
        print("Warning: reportlab not installed.  Skipping PDF generation.")
        print("Install with: pip install reportlab")
        return

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Tournament Report</b>", styles["Title"]))
    elements.append(Paragraph(f"Generated:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Total Matches: {len(result.matches)}", styles["Normal"]))
    elements.append(Paragraph(f"Total Draws: {result. draws}", styles["Normal"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Leaderboard</b>", styles["Heading2"]))
    leaderboard_data = [["Rank", "General", "Wins"]]
    for rank, (name, wins) in enumerate(result.get_leaderboard(), 1):
        leaderboard_data.append([str(rank), name, str(wins)])

    if len(leaderboard_data) > 1:
        lb_table = Table(leaderboard_data, colWidths=[2 * cm, 6 * cm, 2 * cm])
        lb_table. setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(lb_table)

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Match Results</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    for i, match in enumerate(result.matches, 1):
        txt = f"{i}. {match.scenario}:  {match.general1_name} vs {match.general2_name} -> <b>{match.winner}</b> ({match.ticks} ticks)"
        elements.append(Paragraph(txt, styles["Normal"]))

    doc.build(elements)
    print(f"PDF report generated: {output_path}")


def run_tournament_cli(args):
    """CLI entry point for tournament mode."""
    report_dir = args.output_dir
    os.makedirs(report_dir, exist_ok=True)

    generals = None
    if args.generals:
        generals = [g.strip() for g in args.generals.split(",")]

    scenarios = None
    if args.scenarios:
        scenarios = [s. strip() for s in args.scenarios.split(",")]

    headless = args.headless

    result = run_tournament(
        generals=generals,
        scenarios=scenarios,
        num_repeats=args.repeats,
        swap_sides=not args.no_swap,
        delay=args.delay,
        use_curses=args. use_curses,
        use_pygame=args.use_pygame,
        assets_dir=args. assets_dir,
        headless=headless,
        verbose=not args.quiet,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.html or args.all_reports:
        html_path = os.path. join(report_dir, f"tournament_{timestamp}.html")
        generate_html_report(result, html_path)

    if args.pdf or args.all_reports:
        pdf_path = os. path.join(report_dir, f"tournament_{timestamp}.pdf")
        generate_pdf_report(result, pdf_path)

    return result