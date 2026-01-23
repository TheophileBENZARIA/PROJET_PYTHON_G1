"""
Programmable Lanchester scenarios (no visual editor).
Builds headless scenarios N vs 2N for melee or archer units,
runs simulations, and optionally plots survivor curves.
"""

from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from backend.Class.Army import Army
from backend.Class.Map import Map
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Generals.MajorDaft import MajorDaft
from backend.Utils.simulation import run_headless_battle


def _make_line_positions(count: int, x: float) -> List[Tuple[float, float]]:
    """
    Place units in a vertical line, spaced by 1 on Y, fixed X.
    """
    return [(x, float(i)) for i in range(count)]


def build_lanchester_scenario(unit_type: str, N: int) -> Tuple[Map, Army, Army]:
    """
    Build a Lanchester scenario: N vs 2N of the same unit type, within engagement range.
    Units start on adjacent columns so melee can engage immediately and archers are in range.
    """
    unit_cls = Knight if unit_type == "melee" else Crossbowman

    # Map sized to fit all units on two columns with some margin
    height = max(10, 2 * N + 2)
    width = max(10, 8)
    game_map = Map(width=width, height=height)

    army1 = Army()
    army2 = Army()

    col_a = 3
    col_b = 4  # adjacent column -> distance 1 (melee can hit), archers definitely in range

    for pos in _make_line_positions(N, col_a):
        army1.add_unit(unit_cls(pos))

    for pos in _make_line_positions(2 * N, col_b):
        army2.add_unit(unit_cls(pos))

    # Assign aggressive-but-simple generals so targeting works
    gen1 = MajorDaft()
    gen2 = MajorDaft()
    army1.general = gen1
    army2.general = gen2
    gen1.army = army1
    gen2.army = army2

    # Attach gameMode map-like reference if needed for clamping
    army1.gameMode = type("GM", (), {"map": game_map})()
    army2.gameMode = army1.gameMode

    return game_map, army1, army2


def run_lanchester_experiment(
    unit_type: str,
    N_values: Iterable[int],
    max_ticks: int = 10000,
    graph_path: Optional[str] = "lanchester.png",
):
    """
    Run one or more Lanchester scenarios (N vs 2N) and optionally plot survivor curves.
    Returns (results_list, graph_path_or_None).
    """
    results = []
    for N in N_values:
        game_map, army1, army2 = build_lanchester_scenario(unit_type, N)
        res = run_headless_battle(game_map, army1, army2, max_ticks=max_ticks)
        res["N"] = N
        results.append(res)

    saved_path = None
    if graph_path:
        saved_path = _plot_results(results, unit_type, graph_path)

    return results, saved_path


def _plot_results(results, unit_type: str, graph_path: str) -> Optional[str]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed; skipping graph generation.")
        return None

    results = sorted(results, key=lambda r: r["N"])
    Ns = [r["N"] for r in results]
    surv_a = [r["army1_survivors"] for r in results]
    surv_b = [r["army2_survivors"] for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(Ns, surv_a, marker="o", label="Survivors (N side)")
    plt.plot(Ns, surv_b, marker="s", label="Survivors (2N side)")
    plt.title(f"Lanchester experiment ({unit_type})")
    plt.xlabel("N (base size)")
    plt.ylabel("Survivors after battle")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    out_path = Path(graph_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()
    return str(out_path.resolve())