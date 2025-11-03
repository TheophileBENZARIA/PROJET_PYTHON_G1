"""
test_system.py - Tests du système MedievAIl Battle Simulator
===========================================================

Ce fichier contient des tests unitaires et d'intégration pour vérifier
que tous les composants du simulateur fonctionnent correctement.

Tests inclus :
- Test des unités individuelles
- Test des armées
- Test des généraux IA
- Test du moteur de bataille
- Test des scénarios
"""

import sys
import os

# Ajouter le dossier du projet au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Unit import Unit, UnitType
from Army import Army
from General import CaptainBraindead, MajorDaft
from BattleEngine import BattleEngine, BattleResult

def test_unit_creation():
    """Test de création et de base des unités"""
    print("Test 1 : Creation des unites")
    
    # Créer une unité de chaque type
    knight = Unit(UnitType.KNIGHT, 5, 5)
    archer = Unit(UnitType.ARCHER, 6, 6)
    spearman = Unit(UnitType.SPEARMAN, 7, 7)
    swordsman = Unit(UnitType.SWORDSMAN, 8, 8)
    
    # Vérifier les statistiques de base
    assert knight.max_health == 100, "Santé du chevalier incorrecte"
    assert archer.range == 3, "Portée de l'archer incorrecte"
    assert spearman.defense == 20, "Défense du piquier incorrecte"
    assert swordsman.speed == 2, "Vitesse de l'épéiste incorrecte"
    
    # Vérifier que les unités sont vivantes
    assert knight.is_alive, "Le chevalier devrait être vivant"
    assert archer.is_alive, "L'archer devrait être vivant"
    
    print("Test des unites : REUSSI")

def test_unit_combat():
    """Test du système de combat entre unités"""
    print("\nTest 2 : Combat entre unites")
    
    # Créer deux unités pour le combat
    attacker = Unit(UnitType.KNIGHT, 0, 0)
    defender = Unit(UnitType.ARCHER, 1, 0)  # À portée d'attaque
    
    # Vérifier l'état initial
    initial_health = defender.health
    assert defender.is_alive, "Le défenseur devrait être vivant"
    
    # Lancer une attaque
    attack_success = attacker.attack(defender)
    assert attack_success, "L'attaque devrait réussir"
    
    # Vérifier que le défenseur a pris des dégâts
    assert defender.health < initial_health, "Le défenseur devrait avoir pris des dégâts"
    
    print("Test du combat : REUSSI")

def test_army_management():
    """Test de la gestion des armées"""
    print("\nTest 3 : Gestion des armees")
    
    # Créer une armée
    army = Army("test_army", "Armée de Test")
    
    # Vérifier l'état initial
    assert army.get_unit_count() == 0, "L'armée devrait être vide"
    assert army.is_defeated(), "L'armée vide devrait être considérée comme vaincue"
    
    # Ajouter des unités
    army.add_unit(Unit(UnitType.KNIGHT, 0, 0))
    army.add_unit(Unit(UnitType.ARCHER, 1, 1))
    
    # Vérifier l'état après ajout
    assert army.get_unit_count() == 2, "L'armée devrait avoir 2 unités"
    assert not army.is_defeated(), "L'armée ne devrait pas être vaincue"
    
    # Tester la récupération par type
    knights = army.get_units_by_type(UnitType.KNIGHT)
    assert len(knights) == 1, "Il devrait y avoir 1 chevalier"
    
    print("Test des armees : REUSSI")

def test_generals():
    """Test des généraux IA"""
    print("\nTest 4 : Generaux IA")
    
    # Créer les généraux
    braindead = CaptainBraindead()
    daft = MajorDaft()
    
    # Vérifier les noms
    assert braindead.get_name() == "Captain Braindead", "Nom de Braindead incorrect"
    assert daft.get_name() == "Major Daft", "Nom de Daft incorrect"
    
    # Créer des armées de test
    army1 = Army("army1", "Armée 1")
    army2 = Army("army2", "Armée 2")
    
    # Ajouter quelques unités
    army1.add_unit(Unit(UnitType.KNIGHT, 0, 0))
    army2.add_unit(Unit(UnitType.ARCHER, 5, 5))
    
    # Assigner les armées aux généraux
    braindead.set_army(army1)
    daft.set_army(army2)
    
    # Tester les ordres
    orders1 = braindead.issue_orders(army2, 10, 10)
    orders2 = daft.issue_orders(army1, 10, 10)
    
    # Vérifier que des ordres ont été donnés
    assert len(orders1) > 0, "Braindead devrait donner des ordres"
    assert len(orders2) > 0, "Daft devrait donner des ordres"
    
    print("Test des generaux : REUSSI")

def test_battle_engine():
    """Test du moteur de bataille"""
    print("\nTest 5 : Moteur de bataille")
    
    # Créer le moteur de bataille
    engine = BattleEngine(width=10, height=8, max_turns=5)
    
    # Vérifier les dimensions
    assert engine.width == 10, "Largeur du champ incorrecte"
    assert engine.height == 8, "Hauteur du champ incorrecte"
    
    # Créer un scénario de test
    army1, army2, general1, general2 = engine.create_test_scenario()
    
    # Vérifier que les armées ont été créées
    assert army1.get_unit_count() > 0, "L'armée 1 devrait avoir des unités"
    assert army2.get_unit_count() > 0, "L'armée 2 devrait avoir des unités"
    
    # Vérifier que les généraux ont des armées
    assert general1.army is not None, "Le général 1 devrait avoir une armée"
    assert general2.army is not None, "Le général 2 devrait avoir une armée"
    
    print("Test du moteur de bataille : REUSSI")

def test_battle_simulation():
    """Test d'une simulation de bataille complète"""
    print("\nTest 6 : Simulation de bataille")
    
    # Créer le moteur de bataille
    engine = BattleEngine(width=8, height=6, max_turns=10)
    
    # Créer un scénario simple
    army1, army2, general1, general2 = engine.create_test_scenario()
    
    # Lancer une bataille courte
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)
    
    # Vérifier le résultat
    assert isinstance(result, BattleResult), "Le résultat devrait être un BattleResult"
    assert result.turns_taken > 0, "La bataille devrait avoir pris au moins 1 tour"
    assert len(result.battle_log) > 0, "Le log de bataille ne devrait pas être vide"
    
    # Vérifier qu'une armée a gagné ou que c'est un match nul
    assert result.winner is not None or result.is_draw, "Il devrait y avoir un gagnant ou un match nul"
    
    print("Test de simulation : REUSSI")

def test_edge_cases():
    """Test des cas limites"""
    print("\nTest 7 : Cas limites")
    
    # Test avec armée vide
    army_empty = Army("empty", "Armée Vide")
    assert army_empty.is_defeated(), "Une armée vide devrait être vaincue"
    
    # Test avec général sans armée
    general_no_army = CaptainBraindead()
    orders = general_no_army.issue_orders(Army("enemy", "Ennemi"), 10, 10)
    assert len(orders) == 0, "Un général sans armée ne devrait pas donner d'ordres"
    
    # Test avec unité morte
    dead_unit = Unit(UnitType.KNIGHT, 0, 0)
    dead_unit.take_damage(200)  # Plus de dégâts que la santé max
    assert not dead_unit.is_alive, "L'unité devrait être morte"
    
    print("Test des cas limites : REUSSI")

def run_all_tests():
    """Lance tous les tests du système"""
    print("MedievAIl Battle Simulator - Tests du systeme")
    print("=" * 60)
    
    try:
        # Exécuter tous les tests
        test_unit_creation()
        test_unit_combat()
        test_army_management()
        test_generals()
        test_battle_engine()
        test_battle_simulation()
        test_edge_cases()
        
        print("\nTOUS LES TESTS SONT PASSES !")
        print("Le système MedievAIl Battle Simulator fonctionne correctement.")
        
        return True
        
    except AssertionError as e:
        print(f"\nECHEC DU TEST : {e}")
        return False
    except Exception as e:
        print(f"\nERREUR INATTENDUE : {e}")
        return False

def performance_test():
    """Test de performance avec de nombreuses unités"""
    print("\nTest 8 : Test de performance")
    
    # Créer une bataille avec beaucoup d'unités
    engine = BattleEngine(width=15, height=10, max_turns=20)
    
    # Créer des armées plus grandes
    army1 = Army("large1", "Grande Armée 1")
    army2 = Army("large2", "Grande Armée 2")
    
    # Spawner beaucoup d'unités
    army1.spawn_units_at_position(2, 5, [
        {'type': UnitType.KNIGHT, 'count': 10},
        {'type': UnitType.ARCHER, 'count': 15},
        {'type': UnitType.SPEARMAN, 'count': 12}
    ])
    
    army2.spawn_units_at_position(12, 5, [
        {'type': UnitType.KNIGHT, 'count': 12},
        {'type': UnitType.SWORDSMAN, 'count': 15},
        {'type': UnitType.ARCHER, 'count': 10}
    ])
    
    # Créer les généraux
    general1 = CaptainBraindead()
    general2 = MajorDaft()
    
    general1.set_army(army1)
    general2.set_army(army2)
    
    print(f"Unités totales : {army1.get_unit_count() + army2.get_unit_count()}")
    
    # Lancer la bataille
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)
    
    print(f"Bataille terminée en {result.turns_taken} tours")
    print(f"Actions enregistrées : {len(result.battle_log)}")
    
    print("Test de performance : REUSSI")

if __name__ == "__main__":
    """
    Point d'entrée pour les tests
    
    Quand on lance ce fichier directement, on exécute tous les tests
    """
    success = run_all_tests()
    
    if success:
        print("\nLancement du test de performance...")
        performance_test()
        print("\nTous les tests sont termines avec succes !")
    else:
        print("\nCertains tests ont echoue. Verifiez le code.")
        sys.exit(1)
