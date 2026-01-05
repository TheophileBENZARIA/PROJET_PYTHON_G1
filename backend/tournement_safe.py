
# tournement_safe.py
# tournement_safe.py
from .battle import Battle
from .scenarios import simple_knight_duel
from .generals import CaptainBraindead, MajorDaft
import os
import itertools
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm



# --- Configuration du tournoi ---
generals = [CaptainBraindead(), MajorDaft()]
scenarios = [("Duel simple", simple_knight_duel)]
num_repeats = 3  # nombre de répétitions par paire de généraux
report_dir = "tournament_report"
os.makedirs(report_dir, exist_ok=True)

# --- Stockage des résultats ---
results = []

print("Début du tournoi...\n")
for scenario_name, scenario_func in scenarios:
    for gen_a, gen_b in itertools.product(generals, repeat=2):
        for repeat in range(num_repeats):
            # Alterner les positions pour éviter le biais
            if repeat % 2 == 0:
                general1, general2 = gen_a, gen_b
            else:
                general1, general2 = gen_b, gen_a

            game_map, army1, army2 = scenario_func()
            battle = Battle(game_map, army1, general1, army2, general2)
            result = battle.run(delay=0)  # headless, pas de pause

            results.append({
                "scenario": scenario_name,
                "general1": general1.name,
                "general2": general2.name,
                "winner": result.winner,
            })
            print(f"{scenario_name} : {general1.name} vs {general2.name} -> {result.winner}")

# --- Calcul du nombre de victoires par général ---
victories = {}
for r in results:
    winner = r["winner"]
    if winner != "Draw":
        victories[winner] = victories.get(winner, 0) + 1

# --- Génération du rapport HTML ---
html_path = os.path.join(report_dir, "report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write("<h1>Tournoi de Généraux</h1>\n")
    f.write("<h2>Résultats par match :</h2>\n")
    f.write("<ul>\n")
    for r in results:
        f.write(f"<li>{r['scenario']} : {r['general1']} vs {r['general2']} -> {r['winner']}</li>\n")
    f.write("</ul>\n")

    f.write("<h2>Nombre de victoires par général :</h2>\n")
    f.write("<ul>\n")
    for general, wins in victories.items():
        f.write(f"<li>{general} : {wins} victoires</li>\n")
    f.write("</ul>\n")

print(f"\nTournoi terminé. Rapport HTML généré : {html_path}")
def generate_pdf_report(results, victories, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # Titre
    elements.append(Paragraph("<b>Tournoi de Généraux</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Résultats des matchs
    elements.append(Paragraph("<b>Résultats des matchs :</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    for r in results:
        txt = f"{r['scenario']} : {r['general1']} vs {r['general2']} → <b>{r['winner']}</b>"
        elements.append(Paragraph(txt, styles["Normal"]))

    elements.append(Spacer(1, 12))

    # Victoires
    elements.append(Paragraph("<b>Nombre de victoires :</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    for general, wins in victories.items():
        elements.append(Paragraph(f"{general} : {wins} victoire(s)", styles["Normal"]))

    # Génération du PDF
    doc.build(elements)
result = battle.run(delay=0, max_ticks=500)
pdf_path = os.path.join(report_dir, "report.pdf")
generate_pdf_report(results, victories, pdf_path)

print(f"Rapport PDF généré : {pdf_path}")

