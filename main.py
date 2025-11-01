"""
main.py - Point d'entrée principal du MedievAIl Battle Simulator
================================================================

Ce fichier contient le code principal pour lancer des simulations de batailles
entre les généraux IA Captain Braindead et Major Daft.

Usage:
    python main.py

Fonctionnalités:
- Lance une bataille de test entre Braindead et Daft
- Affiche le déroulement de la bataille en temps réel
- Montre le résultat final et les statistiques
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft

def main():
    """
    Fonction principale qui lance une simulation de bataille
    
    Cette fonction :
    1. Crée le moteur de bataille
    2. Génère un scénario de test
    3. Lance la simulation
    4. Affiche les résultats
    """
    print("MedievAIl Battle Simulator")
    print("=" * 50)
    print("Simulation de bataille entre généraux IA")
    print("Captain Braindead (Défensif) vs Major Daft (Agressif)")
    print("=" * 50)
    
    # Créer le moteur de bataille avec un champ de 20x15 cases
    engine = BattleEngine(width=20, height=15, max_turns=50)
    
    # Créer un scénario de test avec les deux généraux
    army1, army2, general1, general2 = engine.create_test_scenario()
    
    print(f"\nConfiguration de la bataille :")
    print(f"Champ de bataille : {engine.width}x{engine.height}")
    print(f"Armée 1 : {army1.name} ({army1.get_unit_count()} unités)")
    print(f"Armée 2 : {army2.name} ({army2.get_unit_count()} unités)")
    print(f"Général 1 : {general1.get_name()}")
    print(f"Général 2 : {general2.get_name()}")
    
    # Lancer la simulation de bataille
    print(f"\nDebut de la bataille !")
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
    
    # Afficher le résumé final
    print(f"\nRESULTAT FINAL")
    print("=" * 30)
    print(result.get_summary())
    print(f"Unités perdues - {army1.name}: {result.units_lost_army1}")
    print(f"Unités perdues - {army2.name}: {result.units_lost_army2}")
    
    # Afficher quelques statistiques supplémentaires
    print(f"\nStatistiques detaillees :")
    print(f"Tours écoulés : {result.turns_taken}")
    print(f"Actions enregistrées : {len(result.battle_log)}")
    
    # Afficher les dernières actions de la bataille
    if result.battle_log:
        print(f"\nDernieres actions de la bataille :")
        for action in result.battle_log[-5:]:  # Afficher les 5 dernières actions
            print(f"  {action}")

def run_multiple_battles():
    """
    Lance plusieurs batailles pour tester la consistance des résultats
    
    Cette fonction lance 5 batailles rapides (sans affichage détaillé)
    pour voir quelle stratégie gagne le plus souvent.
    """
    print("\n🔄 Test de consistance - 5 batailles rapides")
    print("=" * 50)
    
    engine = BattleEngine(width=15, height=10, max_turns=30)
    
    braindead_wins = 0
    daft_wins = 0
    draws = 0
    
    for i in range(5):
        print(f"\nBataille {i+1}/5 :")
        
        # Créer un nouveau scénario pour chaque bataille
        army1, army2, general1, general2 = engine.create_test_scenario()
        
        # Lancer la bataille sans affichage détaillé
        result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)
        
        # Compter les victoires
        if result.is_draw:
            draws += 1
            print(f"  Match nul après {result.turns_taken} tours")
        elif result.winner == army1:  # Braindead gagne
            braindead_wins += 1
            print(f"  {general1.get_name()} gagne en {result.turns_taken} tours")
        else:  # Daft gagne
            daft_wins += 1
            print(f"  {general2.get_name()} gagne en {result.turns_taken} tours")
    
    # Afficher les statistiques finales
    print(f"\n📈 Résultats sur 5 batailles :")
    print(f"Captain Braindead : {braindead_wins} victoires")
    print(f"Major Daft : {daft_wins} victoires")
    print(f"Matchs nuls : {draws}")
    
    if braindead_wins > daft_wins:
        print(f"Captain Braindead est plus efficace !")
    elif daft_wins > braindead_wins:
        print(f"Major Daft est plus efficace !")
    else:
        print(f"Les deux generaux sont equilibres !")

if __name__ == "__main__":
    """
    Point d'entrée du programme
    
    Quand on lance le script directement, on exécute la fonction main()
    """
    try:
        # Lancer la bataille principale
        main()
        
        # Demander si on veut lancer des tests supplémentaires
        print(f"\nVoulez-vous lancer des tests de consistance ? (o/n)")
        response = input().lower().strip()
        
        if response in ['o', 'oui', 'y', 'yes']:
            run_multiple_battles()
        
        print(f"\nSimulation terminee !")
        
    except KeyboardInterrupt:
        print(f"\nSimulation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\nErreur lors de la simulation : {e}")
        print(f"Vérifiez que tous les fichiers sont présents et correctement configurés")
