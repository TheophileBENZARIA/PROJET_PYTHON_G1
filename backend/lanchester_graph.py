# backend/lanchester_graph.py
"""
Lanchester's Laws graph generation for battle analysis.

Generates graphs comparing actual battle results with theoretical Lanchester predictions:
- Lanchester's Linear Law (for ancient/melee combat): dA/dt = -k*B, dB/dt = -k*A
- Lanchester's Square Law (for modern/ranged combat): dA/dt = -k*B, dB/dt = -k*A (but losses proportional to enemy numbers)

The Square Law predicts that combat effectiveness scales with the square of force size,
meaning a force twice as large is four times as effective.
"""

import os
import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Try to import matplotlib, gracefully handle if not installed
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None

# Try numpy for numerical integration, fallback to manual if not available
try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None


@dataclass
class BattleSnapshot:
    """Snapshot of battle state at a given tick."""
    tick: int
    army1_count: int
    army2_count: int
    army1_hp_total: int
    army2_hp_total: int


class LanchesterTracker:
    """
    Tracks battle progress for Lanchester analysis.
    Collects snapshots each tick and generates comparison graphs.
    """

    def __init__(self, initial_army1: int, initial_army2: int, unit_type: str = "melee"):
        self.initial_army1 = initial_army1
        self.initial_army2 = initial_army2
        self.unit_type = unit_type  # "melee" or "archer"
        self.snapshots: List[BattleSnapshot] = []

        # Estimated attrition coefficients (can be tuned based on unit stats)
        # These represent how effectively each side kills the other per tick
        self.k1 = 0.1  # Army1's kill rate coefficient
        self.k2 = 0.1  # Army2's kill rate coefficient

    def record_snapshot(self, tick: int, army1_units: List, army2_units: List):
        """Record the current battle state."""
        army1_count = len([u for u in army1_units if u.is_alive()])
        army2_count = len([u for u in army2_units if u.is_alive()])
        army1_hp = sum(getattr(u, 'hp', 0) for u in army1_units if u.is_alive())
        army2_hp = sum(getattr(u, 'hp', 0) for u in army2_units if u.is_alive())

        self.snapshots.append(BattleSnapshot(
            tick=tick,
            army1_count=army1_count,
            army2_count=army2_count,
            army1_hp_total=army1_hp,
            army2_hp_total=army2_hp
        ))

    def _solve_linear_law(self, max_ticks: int) -> Tuple[List[float], List[float], List[int]]:
        """
        Solve Lanchester's Linear Law (Ancient/Melee Combat).

        In melee combat, each unit can only engage one enemy at a time.
        Attrition is proportional to the minimum of the two forces.

        dA/dt = -k * min(A, B)
        dB/dt = -k * min(A, B)
        """
        A = float(self.initial_army1)
        B = float(self.initial_army2)

        army1_theory = [A]
        army2_theory = [B]
        ticks = [0]

        k = (self.k1 + self.k2) / 2  # Average attrition rate

        for t in range(1, max_ticks + 1):
            if A <= 0 or B <= 0:
                break

            # Linear law: losses proportional to minimum force size
            min_force = min(A, B)
            dA = -k * min_force
            dB = -k * min_force

            A = max(0, A + dA)
            B = max(0, B + dB)

            army1_theory.append(A)
            army2_theory.append(B)
            ticks.append(t)

        return army1_theory, army2_theory, ticks

    def _solve_square_law(self, max_ticks: int) -> Tuple[List[float], List[float], List[int]]:
        """
        Solve Lanchester's Square Law (Modern/Ranged Combat).

        In ranged combat, each unit can potentially engage all enemies.
        Combat power scales with the square of force size.

        dA/dt = -k2 * B
        dB/dt = -k1 * A

        Conservation:  k1 * A^2 - k2 * B^2 = constant
        """
        A = float(self.initial_army1)
        B = float(self.initial_army2)

        army1_theory = [A]
        army2_theory = [B]
        ticks = [0]

        # Adjust coefficients for balance
        k1 = self.k1 * 0.5
        k2 = self.k2 * 0.5

        for t in range(1, max_ticks + 1):
            if A <= 0 or B <= 0:
                break

            # Square law: losses proportional to enemy force size
            dA = -k2 * B
            dB = -k1 * A

            A = max(0, A + dA)
            B = max(0, B + dB)

            army1_theory.append(A)
            army2_theory.append(B)
            ticks.append(t)

        return army1_theory, army2_theory, ticks

    def estimate_attrition_coefficients(self):
        """
        Estimate attrition coefficients from actual battle data.
        This improves the theoretical curve fit.
        """
        if len(self.snapshots) < 3:
            return

        # Calculate average attrition rates from actual data
        total_a1_loss = 0
        total_a2_loss = 0
        total_a1_exposure = 0
        total_a2_exposure = 0

        for i in range(1, len(self.snapshots)):
            prev = self.snapshots[i - 1]
            curr = self.snapshots[i]

            a1_loss = prev.army1_count - curr.army1_count
            a2_loss = prev.army2_count - curr.army2_count

            total_a1_loss += max(0, a1_loss)
            total_a2_loss += max(0, a2_loss)
            total_a1_exposure += prev.army2_count  # Army1 losses depend on Army2 size
            total_a2_exposure += prev.army1_count  # Army2 losses depend on Army1 size

        # Estimate k values
        if total_a1_exposure > 0:
            self.k2 = total_a1_loss / total_a1_exposure if total_a1_exposure > 0 else 0.1
        if total_a2_exposure > 0:
            self.k1 = total_a2_loss / total_a2_exposure if total_a2_exposure > 0 else 0.1

        # Clamp to reasonable values
        self.k1 = max(0.01, min(0.5, self.k1))
        self.k2 = max(0.01, min(0.5, self.k2))

    def generate_graph(self, output_dir: str = "graphs", filename: Optional[str] = None) -> Optional[str]:
        """
        Generate and save the Lanchester analysis graph.

        Returns the path to the saved graph, or None if generation failed.
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Warning: matplotlib not installed. Cannot generate Lanchester graph.")
            print("Install with: pip install matplotlib")
            return None

        if not self.snapshots:
            print("Warning: No battle data recorded. Cannot generate graph.")
            return None

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Estimate coefficients from actual data for better fit
        self.estimate_attrition_coefficients()

        # Extract actual data
        actual_ticks = [s.tick for s in self.snapshots]
        actual_army1 = [s.army1_count for s in self.snapshots]
        actual_army2 = [s.army2_count for s in self.snapshots]

        max_tick = max(actual_ticks) if actual_ticks else 100

        # Generate theoretical predictions
        if self.unit_type == "melee":
            theory_army1, theory_army2, theory_ticks = self._solve_linear_law(max_tick)
            law_name = "Linear Law (Melee)"
        else:
            theory_army1, theory_army2, theory_ticks = self._solve_square_law(max_tick)
            law_name = "Square Law (Ranged)"

        # Create the figure with multiple subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f"Lanchester's Laws Analysis\n{law_name} - N={self.initial_army1} vs 2N={self.initial_army2}",
                     fontsize=14, fontweight='bold')

        # Plot 1: Army sizes over time (main comparison)
        ax1 = axes[0, 0]
        ax1.plot(actual_ticks, actual_army1, 'b-', linewidth=2,
                 label=f'Army 1 (Actual) - Started: {self.initial_army1}')
        ax1.plot(actual_ticks, actual_army2, 'r-', linewidth=2,
                 label=f'Army 2 (Actual) - Started: {self.initial_army2}')
        ax1.plot(theory_ticks, theory_army1, 'b--', linewidth=1.5, alpha = 0.7, label = 'Army 1 (Theoretical)')
        ax1.plot(theory_ticks, theory_army2, 'r--', linewidth=1.5, alpha=0.7, label='Army 2 (Theoretical)')
        ax1.set_xlabel('Tick')
        ax1.set_ylabel('Unit Count')
        ax1.set_title('Force Strength Over Time')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, max_tick)
        ax1.set_ylim(0, max(self.initial_army1, self.initial_army2) * 1.1)

        # Plot 2: HP totals over time
        ax2 = axes[0, 1]
        actual_hp1 = [s.army1_hp_total for s in self.snapshots]
        actual_hp2 = [s.army2_hp_total for s in self.snapshots]
        ax2.plot(actual_ticks, actual_hp1, 'b-', linewidth=2, label='Army 1 Total HP')
        ax2.plot(actual_ticks, actual_hp2, 'r-', linewidth=2, label='Army 2 Total HP')
        ax2.fill_between(actual_ticks, actual_hp1, alpha=0.3, color='blue')
        ax2.fill_between(actual_ticks, actual_hp2, alpha=0.3, color='red')
        ax2.set_xlabel('Tick')
        ax2.set_ylabel('Total HP')
        ax2.set_title('Total Army HP Over Time')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)

        # Plot 3: Force ratio over time
        ax3 = axes[1, 0]
        actual_ratio = []
        theory_ratio = []

        for a1, a2 in zip(actual_army1, actual_army2):
            if a2 > 0:
                actual_ratio.append(a1 / a2)
            else:
                actual_ratio.append(float('inf') if a1 > 0 else 1.0)

        for a1, a2 in zip(theory_army1, theory_army2):
            if a2 > 0:
                theory_ratio.append(a1 / a2)
            else:
                theory_ratio.append(float('inf') if a1 > 0 else 1.0)

        # Cap ratios for display
        actual_ratio_capped = [min(r, 10) for r in actual_ratio]
        theory_ratio_capped = [min(r, 10) for r in theory_ratio[: len(actual_ticks)]]

        ax3.plot(actual_ticks, actual_ratio_capped, 'g-', linewidth=2, label='Actual Ratio (A1/A2)')
        ax3.plot(actual_ticks[: len(theory_ratio_capped)], theory_ratio_capped, 'g--', linewidth=1.5, alpha=0.7,
                 label='Theoretical Ratio')
        ax3.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5, label='Equal Forces')
        ax3.axhline(y=0.5, color='orange', linestyle=':', alpha=0.5, label='Initial Ratio (1:2)')
        ax3.set_xlabel('Tick')
        ax3.set_ylabel('Force Ratio (Army1 / Army2)')
        ax3.set_title('Force Ratio Over Time')
        ax3.legend(loc='upper right')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 5)

        # Plot 4: Summary statistics
        ax4 = axes[1, 1]
        ax4.axis('off')

        # Calculate statistics
        final_a1 = actual_army1[-1] if actual_army1 else 0
        final_a2 = actual_army2[-1] if actual_army2 else 0
        battle_duration = actual_ticks[-1] if actual_ticks else 0

        a1_casualties = self.initial_army1 - final_a1
        a2_casualties = self.initial_army2 - final_a2

        winner = "Army 1 (N)" if final_a1 > final_a2 else ("Army 2 (2N)" if final_a2 > final_a1 else "Draw")

        # Lanchester prediction
        if self.unit_type == "melee":
            # Linear law: larger force loses same as smaller, but survives
            predicted_winner = "Army 2 (2N)" if self.initial_army2 > self.initial_army1 else "Army 1 (N)"
            predicted_survivors = abs(self.initial_army2 - self.initial_army1)
        else:
            # Square law: A1^2 * k1 vs A2^2 * k2
            a1_power = self.initial_army1 ** 2
            a2_power = self.initial_army2 ** 2
            predicted_winner = "Army 2 (2N)" if a2_power > a1_power else "Army 1 (N)"
            # Predicted survivors using square law
            if a2_power > a1_power:
                predicted_survivors = int(math.sqrt(a2_power - a1_power))
            else:
                predicted_survivors = int(math.sqrt(a1_power - a2_power))

        stats_text = f"""
BATTLE SUMMARY
{'=' * 40}

Initial Forces:
  Army 1 (N):     {self.initial_army1} units
  Army 2 (2N):    {self.initial_army2} units
  Ratio:          1:{self.initial_army2 / self.initial_army1:.1f}

Final State (Tick {battle_duration}):
  Army 1 survivors: {final_a1}
  Army 2 survivors:  {final_a2}

Casualties:
  Army 1 losses:  {a1_casualties} ({100 * a1_casualties / self.initial_army1:.1f}%)
  Army 2 losses:  {a2_casualties} ({100 * a2_casualties / self.initial_army2:.1f}%)

ACTUAL WINNER: {winner}

{'=' * 40}
LANCHESTER PREDICTION ({law_name})
{'=' * 40}

Predicted Winner: {predicted_winner}
Predicted Survivors: ~{predicted_survivors}

Estimated Attrition Coefficients: 
  k1 (Army1 lethality): {self.k1:.3f}
  k2 (Army2 lethality): {self.k2:.3f}

Note: {law_name} applies to {'melee/ancient warfare where units engage 1v1' if self.unit_type == 'melee' else 'ranged/modern warfare where all units can fire simultaneously'}.
"""

        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, fontsize=9,
                 verticalalignment='top', fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        # Generate filename
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lanchester_{self.unit_type}_N{self.initial_army1}_vs_2N{self.initial_army2}_{timestamp}.png"

        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)

        print(f"Lanchester graph saved to:  {filepath}")
        return filepath


def create_tracker(initial_army1: int, initial_army2: int, unit_type: str = "melee") -> LanchesterTracker:
    """Factory function to create a Lanchester tracker."""
    return LanchesterTracker(initial_army1, initial_army2, unit_type)