"""
Script de visualisation simple des batailles entre Daft et Braindead
Version sans emojis pour Windows
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft
from Army import Army
from Unit import Unit, UnitType

def create_visual_battle():
    """Crée une bataille avec affichage visuel détaillé"""
    
    print("=" * 60)
    print("VISUALISATION BATAILLE : DAFT vs BRAINDEAD")
    print("=" * 60)
    
    # Création des généraux
    print("\nCreation des generaux...")
    braindead = CaptainBraindead()
    daft = MajorDaft()
    print(f"[OK] {braindead.get_name()} (Defensif) cree")
    print(f"[OK] {daft.get_name()} (Agressif) cree")
    
    # Création des armées
    print("\nCreation des armees...")
    army1 = Army("Armee Rouge")
    army2 = Army("Armee Bleue")
    
    # Armée 1 (Braindead) - Position défensive
    positions_army1 = [
        (2, 3), (3, 3), (4, 3),  # Knights
        (2, 4), (3, 4), (4, 4),  # Archers  
        (2, 5), (3, 5), (4, 5),  # Spearmen
        (2, 6), (3, 6), (4, 6)   # Swordsmen
    ]
    
    # Armée 2 (Daft) - Position offensive
    positions_army2 = [
        (15, 3), (16, 3), (17, 3),  # Knights
        (15, 4), (16, 4), (17, 4),  # Archers
        (15, 5), (16, 5), (17, 5),  # Spearmen  
        (15, 6), (16, 6), (17, 6)   # Swordsmen
    ]
    
    # Ajout des unités
    for i, (x, y) in enumerate(positions_army1):
        unit_type = [UnitType.KNIGHT, UnitType.ARCHER, UnitType.SPEARMAN, UnitType.SWORDSMAN][i % 4]
        army1.add_unit(Unit(unit_type, x, y))
    
    for i, (x, y) in enumerate(positions_army2):
        unit_type = [UnitType.KNIGHT, UnitType.ARCHER, UnitType.SPEARMAN, UnitType.SWORDSMAN][i % 4]
        army2.add_unit(Unit(unit_type, x, y))
    
    # Assignation des armées aux généraux
    braindead.set_army(army1)
    daft.set_army(army2)
    
    print(f"[OK] {army1.name}: {army1.get_unit_count()} unites")
    print(f"[OK] {army2.name}: {army2.get_unit_count()} unites")
    
    # Création du moteur de bataille
    print("\nCreation du moteur de bataille...")
    engine = BattleEngine(width=20, height=10, max_turns=15)
    print(f"[OK] Champ de bataille: {engine.width}x{engine.height}")
    
    # Affichage de la position initiale
    print("\nPOSITION INITIALE:")
    print("=" * 40)
    print("Legende:")
    print("[R] P = Piquier (Spearman) - Armee Rouge")
    print("[R] A = Archer - Armee Rouge") 
    print("[R] K = Knight - Armee Rouge")
    print("[R] S = Swordsman - Armee Rouge")
    print("[B] P = Piquier (Spearman) - Armee Bleue")
    print("[B] A = Archer - Armee Bleue")
    print("[B] K = Knight - Armee Bleue") 
    print("[B] S = Swordsman - Armee Bleue")
    print("=" * 40)
    
    # Lancement de la bataille avec affichage détaillé
    print("\nDEBUT DE LA BATAILLE!")
    print("=" * 40)
    
    winner_name, total_turns, actions_count = engine.simulate_battle(army1, army2, braindead, daft, verbose=True)
    
    # Résultats finaux
    print("\nRESULTATS FINAUX:")
    print("=" * 40)
    print(f"Vainqueur: {winner_name if winner_name else 'Match nul'}")
    print(f"Tours ecoules: {total_turns}")
    print(f"Actions enregistrees: {actions_count}")
    
    # Analyse des stratégies
    print("\nANALYSE DES STRATEGIES:")
    print("=" * 40)
    print(f"[DEF] {braindead.get_name()}: Strategie defensive")
    print("   - Reste en position defensive")
    print("   - Attend l'attaque de l'ennemi")
    print("   - Reagit seulement si attaque")
    
    print(f"\n[ATT] {daft.get_name()}: Strategie offensive") 
    print("   - Avance vers l'ennemi")
    print("   - Attaque des que possible")
    print("   - Recherche le combat rapproche")
    
    return winner_name, total_turns

def show_multiple_battles():
    """Montre plusieurs batailles rapides pour voir les tendances"""
    
    print("\nANALYSE DE CONSISTANCE - 5 BATAILLES RAPIDES")
    print("=" * 60)
    
    braindead_wins = 0
    daft_wins = 0
    
    for i in range(5):
        print(f"\n--- BATAILLE {i+1}/5 ---")
        
        # Création rapide
        braindead = CaptainBraindead()
        daft = MajorDaft()
        
        army1 = Army("Armee Rouge")
        army2 = Army("Armee Bleue")
        
        # Positions plus proches pour des batailles plus rapides
        for j in range(3):  # Armées plus petites pour des batailles plus rapides
            army1.add_unit(Unit(UnitType.KNIGHT, 2, 3+j))
            army1.add_unit(Unit(UnitType.ARCHER, 2, 6+j))
            army2.add_unit(Unit(UnitType.KNIGHT, 8, 3+j))
            army2.add_unit(Unit(UnitType.SWORDSMAN, 8, 6+j))
        
        braindead.set_army(army1)
        daft.set_army(army2)
        
        engine = BattleEngine(width=12, height=10, max_turns=10)
        winner_name, total_turns, _ = engine.simulate_battle(army1, army2, braindead, daft, verbose=False)
        
        if winner_name == "Armee Rouge":
            braindead_wins += 1
            print(f"[WIN] Vainqueur: {braindead.get_name()} ({total_turns} tours)")
        elif winner_name == "Armee Bleue":
            daft_wins += 1
            print(f"[WIN] Vainqueur: {daft.get_name()} ({total_turns} tours)")
        else:
            print(f"[DRAW] Match nul ({total_turns} tours)")
    
    print(f"\nRESULTATS FINAUX:")
    print("=" * 30)
    print(f"[DEF] {braindead.get_name()}: {braindead_wins} victoires")
    print(f"[ATT] {daft.get_name()}: {daft_wins} victoires")
    print(f"[DRAW] Matchs nuls: {5 - braindead_wins - daft_wins}")
    
    if braindead_wins > daft_wins:
        print(f"\n[CHAMPION] {braindead.get_name()} est plus efficace!")
    elif daft_wins > braindead_wins:
        print(f"\n[CHAMPION] {daft.get_name()} est plus efficace!")
    else:
        print(f"\n[EQUILIBRE] Les deux generaux sont equilibres!")

if __name__ == "__main__":
    try:
        # Bataille principale avec visualisation
        winner, turns = create_visual_battle()
        
        # Demander si on veut voir l'analyse de consistance
        print(f"\nVoulez-vous voir l'analyse de consistance ? (o/n)")
        response = input().lower().strip()
        
        if response in ['o', 'oui', 'y', 'yes']:
            show_multiple_battles()
        
        print(f"\n[OK] Visualisation terminee!")
        
    except Exception as e:
        print(f"\n[ERREUR] Erreur lors de la visualisation : {e}")
        print("Verifiez que tous les fichiers sont presents et correctement configures")
