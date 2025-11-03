"""
BattleEngine.py - Moteur de bataille pour orchestrer les combats entre généraux IA
"""

from typing import List, Optional, Tuple, Dict
import time
from Unit import Unit, UnitType
from Army import Army
from General import General, CaptainBraindead, MajorDaft

class BattleResult:
    """Classe pour stocker les résultats d'une bataille"""
    
    def __init__(self):
        self.winner: Optional[Army] = None
        self.loser: Optional[Army] = None
        self.turns_taken: int = 0
        self.units_lost_army1: int = 0
        self.units_lost_army2: int = 0
        self.battle_log: List[str] = []
        self.is_draw: bool = False
        
    def add_log(self, message: str):
        """Ajoute un message au log de bataille"""
        self.battle_log.append(message)
        
    def get_summary(self) -> str:
        """Retourne un résumé de la bataille"""
        if self.is_draw:
            return f"BATAILLE NULLE après {self.turns_taken} tours"
        elif self.winner:
            return f"VICTOIRE de l'armée '{self.winner.name}' après {self.turns_taken} tours"
        else:
            return "Résultat indéterminé"

class BattleEngine:
    """Moteur principal pour gérer les batailles entre généraux IA"""
    
    def __init__(self, width: int = 20, height: int = 15, max_turns: int = 100):
        self.width = width
        self.height = height
        self.max_turns = max_turns
        self.battlefield: List[List[Optional[Unit]]] = [[None for _ in range(width)] for _ in range(height)]
        
    def clear_battlefield(self):
        """Vide le champ de bataille"""
        self.battlefield = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def place_army_on_battlefield(self, army: Army, start_x: int, start_y: int):
        """Place une armée sur le champ de bataille"""
        for unit in army.get_alive_units():
            if 0 <= unit.x < self.width and 0 <= unit.y < self.height:
                self.battlefield[unit.y][unit.x] = unit
    
    def update_battlefield(self, army1: Army, army2: Army):
        """Met à jour le champ de bataille avec les positions actuelles des unités"""
        self.clear_battlefield()
        
        # Placer toutes les unités vivantes
        for army in [army1, army2]:
            for unit in army.get_alive_units():
                if 0 <= unit.x < self.width and 0 <= unit.y < self.height:
                    self.battlefield[unit.y][unit.x] = unit
    
    def execute_attacks(self, army1: Army, army2: Army) -> List[str]:
        """Exécute toutes les attaques des unités"""
        attack_log = []
        
        # Collecter toutes les unités qui veulent attaquer
        attacking_units = []
        for army in [army1, army2]:
            for unit in army.get_alive_units():
                if unit.action == "attack" and unit.target_unit:
                    attacking_units.append(unit)
        
        # Exécuter les attaques
        for unit in attacking_units:
            if unit.target_unit and unit.target_unit.is_alive:
                success = unit.attack(unit.target_unit)
                if success:
                    attack_log.append(f"{unit.unit_type.value} ({unit.army_id}) attaque {unit.target_unit.unit_type.value} ({unit.target_unit.army_id}) - Dégâts: {unit.attack_damage}")
                    
                    if not unit.target_unit.is_alive:
                        attack_log.append(f"  → {unit.target_unit.unit_type.value} ({unit.target_unit.army_id}) est éliminé!")
                else:
                    attack_log.append(f"{unit.unit_type.value} ({unit.army_id}) rate son attaque sur {unit.target_unit.unit_type.value} ({unit.target_unit.army_id})")
        
        return attack_log
    
    def simulate_battle(self, army1: Army, army2: Army, general1: General, general2: General, verbose: bool = True) -> BattleResult:
        """
        Simule une bataille complète entre deux armées dirigées par leurs généraux respectifs
        """
        result = BattleResult()
        
        if verbose:
            print(f"\n=== DÉBUT DE LA BATAILLE ===")
            print(f"Armée 1: {army1.name} dirigée par {general1.get_name()}")
            print(f"Armée 2: {army2.name} dirigée par {general2.get_name()}")
            print(f"Champ de bataille: {self.width}x{self.height}")
            print(f"Unités armée 1: {army1.get_unit_count()}")
            print(f"Unités armée 2: {army2.get_unit_count()}")
            print("=" * 50)
        
        # Initialiser le champ de bataille
        self.update_battlefield(army1, army2)
        
        turn = 0
        while turn < self.max_turns:
            turn += 1
            
            if verbose:
                print(f"\n--- TOUR {turn} ---")
            
            # Vérifier si une armée est vaincue
            if army1.is_defeated():
                result.winner = army2
                result.loser = army1
                result.turns_taken = turn
                result.add_log(f"Armée '{army1.name}' vaincue au tour {turn}")
                break
            elif army2.is_defeated():
                result.winner = army1
                result.loser = army2
                result.turns_taken = turn
                result.add_log(f"Armée '{army2.name}' vaincue au tour {turn}")
                break
            
            # Les généraux donnent leurs ordres
            if verbose:
                print(f"\n{general1.get_name()} donne ses ordres:")
            orders1 = general1.issue_orders(army2, self.width, self.height)
            for order in orders1:
                result.add_log(f"Tour {turn} - {general1.get_name()}: {order}")
                if verbose:
                    print(f"  {order}")
            
            if verbose:
                print(f"\n{general2.get_name()} donne ses ordres:")
            orders2 = general2.issue_orders(army1, self.width, self.height)
            for order in orders2:
                result.add_log(f"Tour {turn} - {general2.get_name()}: {order}")
                if verbose:
                    print(f"  {order}")
            
            # Mettre à jour le champ de bataille avec les nouveaux mouvements
            self.update_battlefield(army1, army2)
            
            # Exécuter les attaques
            attack_log = self.execute_attacks(army1, army2)
            for attack in attack_log:
                result.add_log(f"Tour {turn} - Combat: {attack}")
                if verbose:
                    print(f"  Combat: {attack}")
            
            # Afficher l'état du champ de bataille
            if verbose:
                self.display_battlefield()
                print(f"Unités restantes - {army1.name}: {army1.get_unit_count()}, {army2.name}: {army2.get_unit_count()}")
        
        # Si on arrive ici, c'est un match nul (limite de tours atteinte)
        if turn >= self.max_turns:
            result.is_draw = True
            result.turns_taken = turn
            result.add_log(f"Match nul après {self.max_turns} tours")
        
        # Calculer les pertes
        result.units_lost_army1 = len(army1.get_dead_units())
        result.units_lost_army2 = len(army2.get_dead_units())
        
        if verbose:
            print(f"\n=== FIN DE LA BATAILLE ===")
            print(result.get_summary())
            print(f"Pertes - {army1.name}: {result.units_lost_army1}, {army2.name}: {result.units_lost_army2}")
        
        return result
    
    def display_battlefield(self):
        """Affiche le champ de bataille dans le terminal"""
        print("\nChamp de bataille:")
        
        # En-tête avec numéros de colonnes
        header = "   "
        for x in range(self.width):
            header += f"{x:2d}"
        print(header)
        
        # Lignes du champ de bataille
        for y in range(self.height):
            line = f"{y:2d} "
            for x in range(self.width):
                unit = self.battlefield[y][x]
                if unit:
                    line += f"{unit} "
                else:
                    line += ". "
            print(line)
    
    def create_test_scenario(self) -> Tuple[Army, Army, General, General]:
        """Crée un scénario de test avec les deux généraux"""
        
        # Créer les armées
        army1 = Army("army_1", "Armée Rouge")
        army2 = Army("army_2", "Armée Bleue")
        
        # Créer les généraux
        general1 = CaptainBraindead()
        general2 = MajorDaft()
        
        # Assigner les armées aux généraux
        general1.set_army(army1)
        general2.set_army(army2)
        
        # Spawner les unités
        # Armée 1 (Braindead) - Position défensive à gauche
        army1.spawn_units_at_position(2, 5, [
            {'type': UnitType.KNIGHT, 'count': 3},
            {'type': UnitType.ARCHER, 'count': 5},
            {'type': UnitType.SPEARMAN, 'count': 4}
        ])
        
        # Armée 2 (Daft) - Position offensive à droite
        army2.spawn_units_at_position(15, 5, [
            {'type': UnitType.KNIGHT, 'count': 4},
            {'type': UnitType.ARCHER, 'count': 3},
            {'type': UnitType.SWORDSMAN, 'count': 5}
        ])
        
        return army1, army2, general1, general2
