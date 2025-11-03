"""
examples.py - Exemples d'utilisation du MedievAIl Battle Simulator
=================================================================

Ce fichier contient des exemples concrets d'utilisation du simulateur
pour différents scénarios de bataille.

Exemples inclus :
1. Bataille basique entre Braindead et Daft
2. Bataille avec armées personnalisées
3. Test de différents types d'unités
4. Simulation de tournoi
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft
from Army import Army
from Unit import Unit, UnitType

def example_basic_battle():
    """
    Exemple 1 : Bataille basique entre les deux généraux par défaut
    
    Cet exemple montre comment lancer une bataille simple avec
    les configurations par défaut du simulateur.
    """
    print("Exemple 1 : Bataille basique")
    print("-" * 40)
    
    # Créer le moteur de bataille
    engine = BattleEngine(width=15, height=10, max_turns=30)
    
    # Créer un scénario de test
    army1, army2, general1, general2 = engine.create_test_scenario()
    
    # Lancer la bataille
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
    
    print(f"Résultat : {result.get_summary()}")
    return result

def example_custom_armies():
    """
    Exemple 2 : Bataille avec armées personnalisées
    
    Cet exemple montre comment créer des armées avec des compositions
    d'unités spécifiques et les faire s'affronter.
    """
    print("\nExemple 2 : Armees personnalisees")
    print("-" * 40)
    
    # Créer les généraux
    general1 = CaptainBraindead()
    general2 = MajorDaft()
    
    # Créer l'armée défensive (Braindead)
    army_defensive = Army("defensive", "Armée Défensive")
    army_defensive.spawn_units_at_position(2, 5, [
        {'type': UnitType.SPEARMAN, 'count': 8},  # Beaucoup de piquiers
        {'type': UnitType.ARCHER, 'count': 6},    # Quelques archers
        {'type': UnitType.KNIGHT, 'count': 2}     # Peu de chevaliers
    ])
    
    # Créer l'armée offensive (Daft)
    army_offensive = Army("offensive", "Armée Offensive")
    army_offensive.spawn_units_at_position(12, 5, [
        {'type': UnitType.KNIGHT, 'count': 6},     # Beaucoup de chevaliers
        {'type': UnitType.SWORDSMAN, 'count': 8},  # Beaucoup d'épéistes
        {'type': UnitType.ARCHER, 'count': 2}      # Peu d'archers
    ])
    
    # Assigner les armées aux généraux
    general1.set_army(army_defensive)
    general2.set_army(army_offensive)
    
    # Créer le moteur et lancer la bataille
    engine = BattleEngine(width=15, height=10, max_turns=40)
    result = engine.simulate_battle(army_defensive, army_offensive, general1, general2, verbose=True)
    
    print(f"Résultat : {result.get_summary()}")
    return result

def example_unit_types_test():
    """
    Exemple 3 : Test des différents types d'unités
    
    Cet exemple crée des armées spécialisées pour tester
    les avantages et inconvénients de chaque type d'unité.
    """
    print("\nExemple 3 : Test des types d'unites")
    print("-" * 40)
    
    # Créer les généraux
    general1 = CaptainBraindead()
    general2 = MajorDaft()
    
    # Armée spécialisée en cavalerie
    army_cavalry = Army("cavalry", "Armée Cavalerie")
    army_cavalry.spawn_units_at_position(2, 3, [
        {'type': UnitType.KNIGHT, 'count': 10}  # Seulement des chevaliers
    ])
    
    # Armée spécialisée en infanterie
    army_infantry = Army("infantry", "Armée Infanterie")
    army_infantry.spawn_units_at_position(12, 3, [
        {'type': UnitType.SPEARMAN, 'count': 10}  # Seulement des piquiers
    ])
    
    # Assigner les armées
    general1.set_army(army_cavalry)
    general2.set_army(army_infantry)
    
    # Lancer la bataille
    engine = BattleEngine(width=15, height=7, max_turns=25)
    result = engine.simulate_battle(army_cavalry, army_infantry, general1, general2, verbose=True)
    
    print(f"Résultat : {result.get_summary()}")
    print("Note : Les piquiers ont un bonus contre les chevaliers !")
    return result

def example_tournament():
    """
    Exemple 4 : Simulation de tournoi
    
    Cet exemple lance plusieurs batailles pour déterminer
    quel général est le plus efficace en moyenne.
    """
    print("\nExemple 4 : Tournoi entre generaux")
    print("-" * 40)
    
    engine = BattleEngine(width=12, height=8, max_turns=20)
    
    braindead_wins = 0
    daft_wins = 0
    draws = 0
    total_turns = 0
    
    print("Lancement de 10 batailles...")
    
    for i in range(10):
        # Créer un nouveau scénario pour chaque bataille
        army1, army2, general1, general2 = engine.create_test_scenario()
        
        # Lancer la bataille sans affichage détaillé
        result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)
        
        # Compter les résultats
        total_turns += result.turns_taken
        
        if result.is_draw:
            draws += 1
        elif result.winner == army1:  # Braindead gagne
            braindead_wins += 1
        else:  # Daft gagne
            daft_wins += 1
        
        print(f"Bataille {i+1}: {result.get_summary()}")
    
    # Afficher les statistiques du tournoi
    print(f"\nResultats du tournoi (10 batailles) :")
    print(f"Captain Braindead : {braindead_wins} victoires ({braindead_wins/10*100:.1f}%)")
    print(f"Major Daft : {daft_wins} victoires ({daft_wins/10*100:.1f}%)")
    print(f"Matchs nuls : {draws} ({draws/10*100:.1f}%)")
    print(f"Tours moyens par bataille : {total_turns/10:.1f}")
    
    # Déterminer le champion
    if braindead_wins > daft_wins:
        print(f"Champion : Captain Braindead !")
    elif daft_wins > braindead_wins:
        print(f"Champion : Major Daft !")
    else:
        print(f"Egalite parfaite !")

def example_manual_unit_creation():
    """
    Exemple 5 : Création manuelle d'unités
    
    Cet exemple montre comment créer des unités individuellement
    et les placer à des positions spécifiques.
    """
    print("\nExemple 5 : Creation manuelle d'unites")
    print("-" * 40)
    
    # Créer les généraux
    general1 = CaptainBraindead()
    general2 = MajorDaft()
    
    # Créer les armées
    army1 = Army("manual1", "Armée Manuelle 1")
    army2 = Army("manual2", "Armée Manuelle 2")
    
    # Créer des unités individuellement et les placer
    # Armée 1 - Formation défensive
    army1.add_unit(Unit(UnitType.KNIGHT, 3, 4))    # Chevalier au centre
    army1.add_unit(Unit(UnitType.SPEARMAN, 2, 4))   # Piquier à gauche
    army1.add_unit(Unit(UnitType.SPEARMAN, 4, 4))   # Piquier à droite
    army1.add_unit(Unit(UnitType.ARCHER, 3, 3))     # Archer en arrière
    
    # Armée 2 - Formation offensive
    army2.add_unit(Unit(UnitType.KNIGHT, 12, 4))    # Chevalier au centre
    army2.add_unit(Unit(UnitType.SWORDSMAN, 11, 4)) # Épéiste à gauche
    army2.add_unit(Unit(UnitType.SWORDSMAN, 13, 4)) # Épéiste à droite
    army2.add_unit(Unit(UnitType.ARCHER, 12, 5))    # Archer en avant
    
    # Assigner les armées
    general1.set_army(army1)
    general2.set_army(army2)
    
    # Lancer la bataille
    engine = BattleEngine(width=16, height=8, max_turns=25)
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
    
    print(f"Résultat : {result.get_summary()}")
    return result

def run_all_examples():
    """
    Lance tous les exemples d'utilisation
    
    Cette fonction exécute tous les exemples pour démontrer
    les différentes fonctionnalités du simulateur.
    """
    print("MedievAIl Battle Simulator - Exemples d'utilisation")
    print("=" * 60)
    
    try:
        # Exécuter tous les exemples
        example_basic_battle()
        example_custom_armies()
        example_unit_types_test()
        example_tournament()
        example_manual_unit_creation()
        
        print("\nTous les exemples ont ete executes avec succes !")
        print("Vous pouvez maintenant creer vos propres scenarios de bataille.")
        
    except Exception as e:
        print(f"\nErreur lors de l'execution des exemples : {e}")
        print("Verifiez que tous les fichiers sont presents et correctement configures")

if __name__ == "__main__":
    """
    Point d'entrée pour les exemples
    
    Quand on lance ce fichier directement, on exécute tous les exemples
    """
    run_all_examples()
