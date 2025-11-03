"""
Test visuel simple pour voir clairement les différences entre Daft et Braindead
Version sans emojis pour Windows
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft
from Army import Army
from Unit import Unit, UnitType

def test_visuel_simple():
    """Test visuel simple avec peu d'unités pour voir clairement les mouvements"""
    
    print("=" * 70)
    print("TEST VISUEL : DAFT vs BRAINDEAD")
    print("=" * 70)
    
    # Création des généraux
    print("\n[ETAPE 1] Creation des generaux...")
    braindead = CaptainBraindead()
    daft = MajorDaft()
    print(f"[OK] {braindead.get_name()} (DEFENSIF) - Ne bouge jamais")
    print(f"[OK] {daft.get_name()} (AGRESSIF) - Avance vers l'ennemi")
    
    # Création des armées avec peu d'unités pour plus de clarté
    print("\n[ETAPE 2] Creation des armees...")
    army1 = Army("Armee Rouge (Braindead)")
    army2 = Army("Armee Bleue (Daft)")
    
    # Armée 1 (Braindead) - Position défensive à gauche
    army1.add_unit(Unit(UnitType.KNIGHT, 2, 3))    # Chevalier
    army1.add_unit(Unit(UnitType.ARCHER, 2, 4))    # Archer
    army1.add_unit(Unit(UnitType.SPEARMAN, 2, 5))  # Piquier
    
    # Armée 2 (Daft) - Position offensive à droite
    army2.add_unit(Unit(UnitType.KNIGHT, 8, 3))    # Chevalier
    army2.add_unit(Unit(UnitType.SWORDSMAN, 8, 4)) # Épéiste
    army2.add_unit(Unit(UnitType.ARCHER, 8, 5))    # Archer
    
    # Assignation des armées
    braindead.set_army(army1)
    daft.set_army(army2)
    
    print(f"[OK] {army1.name}: 3 unites (position defensive)")
    print(f"[OK] {army2.name}: 3 unites (position offensive)")
    
    # Création du moteur de bataille
    print("\n[ETAPE 3] Configuration du champ de bataille...")
    engine = BattleEngine(width=12, height=8, max_turns=10)
    print(f"[OK] Champ: {engine.width}x{engine.height}")
    
    # Affichage de la position initiale
    print("\n[POSITION INITIALE]")
    print("=" * 50)
    print("Legende:")
    print("[R] R = Rouge (Braindead - DEFENSIF)")
    print("[B] B = Bleu (Daft - AGRESSIF)")
    print("K=Knight, A=Archer, P=Spearman, S=Swordsman")
    print("=" * 50)
    
    # Lancement de la bataille
    print("\n[DEBUT DE LA BATAILLE]")
    print("=" * 50)
    
    try:
        result = engine.simulate_battle(army1, army2, braindead, daft, verbose=True)
        
        # Analyse des résultats
        print("\n[ANALYSE DES RESULTATS]")
        print("=" * 50)
        
        if hasattr(result, 'winner'):
            winner = result.winner
            turns = result.turns
            print(f"[WIN] Vainqueur: {winner if winner else 'Match nul'}")
            print(f"[TIME] Tours ecoules: {turns}")
        else:
            print("[INFO] Bataille terminee")
        
        # Analyse des stratégies observées
        print("\n[STRATEGIES OBSERVEES]")
        print("=" * 50)
        print("[DEF] BRAINDEAD (Defensif):")
        print("   - Reste toujours en position")
        print("   - Ne bouge jamais")
        print("   - Attend l'attaque")
        
        print("\n[ATT] DAFT (Agressif):")
        print("   - Avance vers l'ennemi")
        print("   - Attaque des que possible")
        print("   - Recherche le combat")
        
    except Exception as e:
        print(f"[ERREUR] Erreur: {e}")

def test_visuel_rapide():
    """Test visuel rapide pour voir plusieurs batailles"""
    
    print("\n" + "=" * 70)
    print("TEST VISUEL RAPIDE - 3 BATAILLES")
    print("=" * 70)
    
    for i in range(3):
        print(f"\n--- BATAILLE {i+1}/3 ---")
        
        # Création rapide
        braindead = CaptainBraindead()
        daft = MajorDaft()
        
        army1 = Army("Rouge")
        army2 = Army("Bleue")
        
        # Armées très simples
        army1.add_unit(Unit(UnitType.KNIGHT, 1, 3))
        army1.add_unit(Unit(UnitType.ARCHER, 1, 4))
        
        army2.add_unit(Unit(UnitType.KNIGHT, 6, 3))
        army2.add_unit(Unit(UnitType.SWORDSMAN, 6, 4))
        
        braindead.set_army(army1)
        daft.set_army(army2)
        
        engine = BattleEngine(width=8, height=6, max_turns=8)
        
        try:
            result = engine.simulate_battle(army1, army2, braindead, daft, verbose=False)
            
            if hasattr(result, 'winner'):
                winner = result.winner
                turns = result.turns
                if winner == "Rouge":
                    print(f"[WIN] BRAINDEAD gagne en {turns} tours")
                elif winner == "Bleue":
                    print(f"[WIN] DAFT gagne en {turns} tours")
                else:
                    print(f"[DRAW] Match nul en {turns} tours")
            else:
                print("[INFO] Bataille terminee")
                
        except Exception as e:
            print(f"[ERREUR] Erreur: {e}")

def test_visuel_detaille():
    """Test visuel détaillé avec explications"""
    
    print("\n" + "=" * 70)
    print("TEST VISUEL DETAILLE - EXPLICATIONS")
    print("=" * 70)
    
    print("\n[EXPLICATION DES STRATEGIES]")
    print("=" * 50)
    print("[DEF] CAPTAIN BRAINDEAD (Defensif):")
    print("   - Strategie: Rester en place")
    print("   - Comportement: Ne bouge jamais")
    print("   - Avantage: Position defensive forte")
    print("   - Inconvenient: Ne prend pas l'initiative")
    
    print("\n[ATT] MAJOR DAFT (Agressif):")
    print("   - Strategie: Avancer et attaquer")
    print("   - Comportement: Bouge vers l'ennemi")
    print("   - Avantage: Prend l'initiative")
    print("   - Inconvenient: Peut se mettre en danger")
    
    print("\n[CE QUE VOUS ALLEZ VOIR]")
    print("=" * 50)
    print("1. [R] Les unites ROUGES (Braindead) restent immobiles")
    print("2. [B] Les unites BLEUES (Daft) avancent vers la gauche")
    print("3. [ATT] Quand Daft arrive a portee, il attaque")
    print("4. [DMG] Vous verrez les degats infliges")
    print("5. [WIN] Le vainqueur sera determine")
    
    # Demander confirmation
    print(f"\nVoulez-vous lancer le test detaille ? (o/n)")
    response = input().lower().strip()
    
    if response in ['o', 'oui', 'y', 'yes']:
        test_visuel_simple()

if __name__ == "__main__":
    try:
        # Test principal
        test_visuel_simple()
        
        # Demander si on veut voir le test rapide
        print(f"\nVoulez-vous voir 3 batailles rapides ? (o/n)")
        response = input().lower().strip()
        
        if response in ['o', 'oui', 'y', 'yes']:
            test_visuel_rapide()
        
        # Test détaillé avec explications
        test_visuel_detaille()
        
        print(f"\n[OK] Test visuel termine!")
        print("Vous avez maintenant une comprehension claire des strategies!")
        
    except Exception as e:
        print(f"\n[ERREUR] Erreur lors du test visuel : {e}")
        print("Verifiez que tous les fichiers sont presents")
