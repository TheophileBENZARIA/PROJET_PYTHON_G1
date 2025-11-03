"""
test_generals_simple.py - Test simple des généraux Daft et Braindead
====================================================================

Version simplifiée sans emojis pour Windows
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft
from Army import Army
from Unit import Unit, UnitType

def test_braindead_strategy():
    """Test de la stratégie défensive de Captain Braindead"""
    print("Test de Captain Braindead (Strategie defensive)")
    print("-" * 50)
    
    # Créer le général
    braindead = CaptainBraindead()
    print(f"General cree : {braindead.get_name()}")
    
    # Créer une armée de test
    army = Army("test_army", "Armee de Test")
    army.add_unit(Unit(UnitType.KNIGHT, 5, 5))
    army.add_unit(Unit(UnitType.ARCHER, 6, 6))
    army.add_unit(Unit(UnitType.SPEARMAN, 7, 7))
    
    # Assigner l'armée au général
    braindead.set_army(army)
    print(f"Armee assignee : {army.get_unit_count()} unites")
    
    # Créer une armée ennemie (vide pour le test)
    enemy_army = Army("enemy", "Armee Ennemie")
    
    # Tester les ordres
    orders = braindead.issue_orders(enemy_army, 10, 10)
    print(f"Ordres donnes : {len(orders)} actions")
    
    # Vérifier que toutes les unités restent en défense
    for order in orders:
        print(f"  {order}")
        assert "stays in defensive position" in order, "Braindead devrait donner des ordres defensifs"
    
    # Vérifier que les unités ont l'action "defend"
    for unit in army.get_alive_units():
        assert unit.action == "defend", f"L'unite {unit.unit_type.value} devrait etre en defense"
    
    print("Captain Braindead fonctionne correctement !")
    return True

def test_daft_strategy():
    """Test de la stratégie agressive de Major Daft"""
    print("\nTest de Major Daft (Strategie aggressive)")
    print("-" * 50)
    
    # Créer le général
    daft = MajorDaft()
    print(f"General cree : {daft.get_name()}")
    
    # Créer une armée de test
    army = Army("test_army", "Armee de Test")
    army.add_unit(Unit(UnitType.KNIGHT, 5, 5))
    army.add_unit(Unit(UnitType.ARCHER, 6, 6))
    
    # Créer une armée ennemie avec des unités
    enemy_army = Army("enemy", "Armee Ennemie")
    enemy_army.add_unit(Unit(UnitType.SWORDSMAN, 8, 8))  # Ennemi loin
    enemy_army.add_unit(Unit(UnitType.ARCHER, 7, 7))    # Ennemi plus proche
    
    # Assigner l'armée au général
    daft.set_army(army)
    print(f"Armee assignee : {army.get_unit_count()} unites")
    print(f"Ennemis presents : {enemy_army.get_unit_count()} unites")
    
    # Tester les ordres
    orders = daft.issue_orders(enemy_army, 10, 10)
    print(f"Ordres donnes : {len(orders)} actions")
    
    # Vérifier que les ordres sont offensifs
    offensive_actions = 0
    for order in orders:
        print(f"  {order}")
        if "attacks enemy" in order or "moves from" in order:
            offensive_actions += 1
    
    assert offensive_actions > 0, "Daft devrait donner des ordres offensifs"
    
    print("Major Daft fonctionne correctement !")
    return True

def test_battle_between_generals():
    """Test d'une bataille entre les deux généraux"""
    print("\nTest de bataille : Braindead vs Daft")
    print("-" * 50)
    
    # Créer le moteur de bataille
    engine = BattleEngine(width=12, height=8, max_turns=15)
    print(f"Moteur de bataille cree : {engine.width}x{engine.height}")
    
    # Créer un scénario de test
    army1, army2, general1, general2 = engine.create_test_scenario()
    print(f"Scenario cree :")
    print(f"  - {general1.get_name()} : {army1.get_unit_count()} unites")
    print(f"  - {general2.get_name()} : {army2.get_unit_count()} unites")
    
    # Lancer la bataille
    print(f"\nLancement de la bataille...")
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
    
    # Afficher le résultat
    print(f"\nResultat de la bataille :")
    print(f"  {result.get_summary()}")
    print(f"  Tours ecoules : {result.turns_taken}")
    print(f"  Actions enregistrees : {len(result.battle_log)}")
    
    # Vérifier qu'une bataille s'est bien déroulée
    assert result.turns_taken > 0, "La bataille devrait avoir pris au moins 1 tour"
    assert len(result.battle_log) > 0, "Le log de bataille ne devrait pas etre vide"
    
    print("Bataille entre generaux reussie !")
    return True

def main():
    """Fonction principale pour tester les généraux"""
    print("Test des generaux IA : Captain Braindead vs Major Daft")
    print("=" * 60)
    
    try:
        # Tester chaque général individuellement
        test_braindead_strategy()
        test_daft_strategy()
        
        # Tester une bataille entre eux
        test_battle_between_generals()
        
        print("\nTOUS LES TESTS DES GENERAUX SONT PASSES !")
        print("Captain Braindead et Major Daft fonctionnent parfaitement !")
        
    except Exception as e:
        print(f"\nErreur lors des tests : {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
