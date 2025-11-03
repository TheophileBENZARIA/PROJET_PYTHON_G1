"""
test_simple.py - Test simple sans emojis pour Windows
"""

from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft

def test_simple():
    print("=== TEST SIMPLE DES GENERAUX ===")
    
    # Test 1: Creer les generaux
    print("\n1. Creation des generaux...")
    braindead = CaptainBraindead()
    daft = MajorDaft()
    print(f"   - {braindead.get_name()} cree")
    print(f"   - {daft.get_name()} cree")
    
    # Test 2: Creer le moteur de bataille
    print("\n2. Creation du moteur de bataille...")
    engine = BattleEngine(width=10, height=6, max_turns=5)
    print(f"   - Moteur cree: {engine.width}x{engine.height}")
    
    # Test 3: Creer un scenario
    print("\n3. Creation du scenario...")
    army1, army2, general1, general2 = engine.create_test_scenario()
    print(f"   - {general1.get_name()}: {army1.get_unit_count()} unites")
    print(f"   - {general2.get_name()}: {army2.get_unit_count()} unites")
    
    # Test 4: Lancer une bataille courte
    print("\n4. Lancement de la bataille...")
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
    
    # Test 5: Afficher le resultat
    print(f"\n5. Resultat: {result.get_summary()}")
    print(f"   - Tours: {result.turns_taken}")
    print(f"   - Actions: {len(result.battle_log)}")
    
    print("\n=== TEST TERMINE AVEC SUCCES ===")

if __name__ == "__main__":
    test_simple()
