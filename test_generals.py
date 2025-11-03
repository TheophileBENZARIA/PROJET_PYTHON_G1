"""
test_generals.py - Test spécifique des généraux Daft et Braindead
===============================================================

Ce fichier teste spécifiquement les deux généraux IA :
- Captain Braindead (défensif)
- Major Daft (agressif)
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft
from Army import Army
from Unit import Unit, UnitType

def test_braindead_strategy():
    """Test de la stratégie défensive de Captain Braindead"""
    print("🧪 Test de Captain Braindead (Stratégie défensive)")
    print("-" * 50)
    
    # Créer le général
    braindead = CaptainBraindead()
    print(f"✅ Général créé : {braindead.get_name()}")
    
    # Créer une armée de test
    army = Army("test_army", "Armée de Test")
    army.add_unit(Unit(UnitType.KNIGHT, 5, 5))
    army.add_unit(Unit(UnitType.ARCHER, 6, 6))
    army.add_unit(Unit(UnitType.SPEARMAN, 7, 7))
    
    # Assigner l'armée au général
    braindead.set_army(army)
    print(f"✅ Armée assignée : {army.get_unit_count()} unités")
    
    # Créer une armée ennemie (vide pour le test)
    enemy_army = Army("enemy", "Armée Ennemie")
    
    # Tester les ordres
    orders = braindead.issue_orders(enemy_army, 10, 10)
    print(f"✅ Ordres donnés : {len(orders)} actions")
    
    # Vérifier que toutes les unités restent en défense
    for order in orders:
        print(f"  📋 {order}")
        assert "stays in defensive position" in order, "Braindead devrait donner des ordres défensifs"
    
    # Vérifier que les unités ont l'action "defend"
    for unit in army.get_alive_units():
        assert unit.action == "defend", f"L'unité {unit.unit_type.value} devrait être en défense"
    
    print("✅ Captain Braindead fonctionne correctement !")
    return True

def test_daft_strategy():
    """Test de la stratégie agressive de Major Daft"""
    print("\n🧪 Test de Major Daft (Stratégie agressive)")
    print("-" * 50)
    
    # Créer le général
    daft = MajorDaft()
    print(f"✅ Général créé : {daft.get_name()}")
    
    # Créer une armée de test
    army = Army("test_army", "Armée de Test")
    army.add_unit(Unit(UnitType.KNIGHT, 5, 5))
    army.add_unit(Unit(UnitType.ARCHER, 6, 6))
    
    # Créer une armée ennemie avec des unités
    enemy_army = Army("enemy", "Armée Ennemie")
    enemy_army.add_unit(Unit(UnitType.SWORDSMAN, 8, 8))  # Ennemi loin
    enemy_army.add_unit(Unit(UnitType.ARCHER, 7, 7))    # Ennemi plus proche
    
    # Assigner l'armée au général
    daft.set_army(army)
    print(f"✅ Armée assignée : {army.get_unit_count()} unités")
    print(f"✅ Ennemis présents : {enemy_army.get_unit_count()} unités")
    
    # Tester les ordres
    orders = daft.issue_orders(enemy_army, 10, 10)
    print(f"✅ Ordres donnés : {len(orders)} actions")
    
    # Vérifier que les ordres sont offensifs
    offensive_actions = 0
    for order in orders:
        print(f"  📋 {order}")
        if "attacks enemy" in order or "moves from" in order:
            offensive_actions += 1
    
    assert offensive_actions > 0, "Daft devrait donner des ordres offensifs"
    
    print("✅ Major Daft fonctionne correctement !")
    return True

def test_battle_between_generals():
    """Test d'une bataille entre les deux généraux"""
    print("\n⚔️ Test de bataille : Braindead vs Daft")
    print("-" * 50)
    
    # Créer le moteur de bataille
    engine = BattleEngine(width=12, height=8, max_turns=15)
    print(f"✅ Moteur de bataille créé : {engine.width}x{engine.height}")
    
    # Créer un scénario de test
    army1, army2, general1, general2 = engine.create_test_scenario()
    print(f"✅ Scénario créé :")
    print(f"  - {general1.get_name()} : {army1.get_unit_count()} unités")
    print(f"  - {general2.get_name()} : {army2.get_unit_count()} unités")
    
    # Lancer la bataille
    print(f"\n🚀 Lancement de la bataille...")
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
    
    # Afficher le résultat
    print(f"\nResultat de la bataille :")
    print(f"  {result.get_summary()}")
    print(f"  Tours écoulés : {result.turns_taken}")
    print(f"  Actions enregistrées : {len(result.battle_log)}")
    
    # Vérifier qu'une bataille s'est bien déroulée
    assert result.turns_taken > 0, "La bataille devrait avoir pris au moins 1 tour"
    assert len(result.battle_log) > 0, "Le log de bataille ne devrait pas être vide"
    
    print("✅ Bataille entre généraux réussie !")
    return True

def test_multiple_battles():
    """Test de plusieurs batailles pour voir qui gagne le plus souvent"""
    print("\nTest de consistance : 5 batailles rapides")
    print("-" * 50)
    
    engine = BattleEngine(width=10, height=6, max_turns=10)
    
    braindead_wins = 0
    daft_wins = 0
    draws = 0
    
    for i in range(5):
        print(f"\nBataille {i+1}/5 :")
        
        # Créer un nouveau scénario
        army1, army2, general1, general2 = engine.create_test_scenario()
        
        # Lancer la bataille sans affichage détaillé
        result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)
        
        # Compter les victoires
        if result.is_draw:
            draws += 1
            print(f"  🤝 Match nul après {result.turns_taken} tours")
        elif result.winner == army1:  # Braindead gagne
            braindead_wins += 1
            print(f"  🛡️ {general1.get_name()} gagne en {result.turns_taken} tours")
        else:  # Daft gagne
            daft_wins += 1
            print(f"  ⚔️ {general2.get_name()} gagne en {result.turns_taken} tours")
    
    # Afficher les statistiques
    print(f"\n📊 Résultats sur 5 batailles :")
    print(f"  🛡️ Captain Braindead : {braindead_wins} victoires")
    print(f"  ⚔️ Major Daft : {daft_wins} victoires")
    print(f"  🤝 Matchs nuls : {draws}")
    
    if braindead_wins > daft_wins:
        print(f"  Captain Braindead est plus efficace !")
    elif daft_wins > braindead_wins:
        print(f"  Major Daft est plus efficace !")
    else:
        print(f"  🤝 Les deux généraux sont équilibrés !")
    
    print("✅ Test de consistance terminé !")
    return True

def main():
    """Fonction principale pour tester les généraux"""
    print("🚀 Test des généraux IA : Captain Braindead vs Major Daft")
    print("=" * 60)
    
    try:
        # Tester chaque général individuellement
        test_braindead_strategy()
        test_daft_strategy()
        
        # Tester une bataille entre eux
        test_battle_between_generals()
        
        # Tester la consistance
        test_multiple_battles()
        
        print("\nTOUS LES TESTS DES GENERAUX SONT PASSES !")
        print("Captain Braindead et Major Daft fonctionnent parfaitement !")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests : {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
