"""
Army.py - Classe pour représenter une armée médiévale
"""

from typing import List, Optional, Tuple
from Unit import Unit, UnitType
import random

class Army:
    """Classe représentant une armée médiévale"""
    
    def __init__(self, army_id: str, name: str = ""):
        self.army_id = army_id
        self.name = name
        self.units: List[Unit] = []
        self.general = None  # Sera assigné plus tard
        
    def add_unit(self, unit: Unit):
        """Ajoute une unité à l'armée"""
        unit.army_id = self.army_id
        self.units.append(unit)
    
    def remove_unit(self, unit: Unit):
        """Retire une unité de l'armée"""
        if unit in self.units:
            self.units.remove(unit)
    
    def get_alive_units(self) -> List[Unit]:
        """Retourne toutes les unités vivantes de l'armée"""
        return [unit for unit in self.units if unit.is_alive]
    
    def get_dead_units(self) -> List[Unit]:
        """Retourne toutes les unités mortes de l'armée"""
        return [unit for unit in self.units if not unit.is_alive]
    
    def is_defeated(self) -> bool:
        """Vérifie si l'armée est vaincue (plus d'unités vivantes)"""
        return len(self.get_alive_units()) == 0
    
    def get_unit_count(self) -> int:
        """Retourne le nombre d'unités vivantes"""
        return len(self.get_alive_units())
    
    def get_total_health(self) -> int:
        """Retourne la santé totale de toutes les unités vivantes"""
        return sum(unit.health for unit in self.get_alive_units())
    
    def get_units_by_type(self, unit_type: UnitType) -> List[Unit]:
        """Retourne toutes les unités vivantes d'un type donné"""
        return [unit for unit in self.get_alive_units() if unit.unit_type == unit_type]
    
    def get_closest_enemy_unit(self, position: Tuple[int, int], enemy_army: 'Army') -> Optional[Unit]:
        """Trouve l'unité ennemie la plus proche d'une position donnée"""
        alive_enemies = enemy_army.get_alive_units()
        if not alive_enemies:
            return None
            
        closest_unit = None
        min_distance = float('inf')
        
        for enemy in alive_enemies:
            distance = abs(position[0] - enemy.x) + abs(position[1] - enemy.y)
            if distance < min_distance:
                min_distance = distance
                closest_unit = enemy
                
        return closest_unit
    
    def get_units_in_range(self, position: Tuple[int, int], range_distance: int) -> List[Unit]:
        """Retourne toutes les unités vivantes dans un rayon donné"""
        units_in_range = []
        for unit in self.get_alive_units():
            distance = abs(position[0] - unit.x) + abs(position[1] - unit.y)
            if distance <= range_distance:
                units_in_range.append(unit)
        return units_in_range
    
    def spawn_units_at_position(self, x: int, y: int, unit_configs: List[dict]):
        """
        Spawn des unités à une position donnée
        unit_configs: Liste de dictionnaires avec 'type' et 'count'
        Exemple: [{'type': UnitType.KNIGHT, 'count': 5}, {'type': UnitType.ARCHER, 'count': 10}]
        """
        for config in unit_configs:
            unit_type = config['type']
            count = config['count']
            
            for i in range(count):
                # Position légèrement décalée pour éviter la superposition
                offset_x = x + (i % 3) - 1
                offset_y = y + (i // 3) - 1
                
                unit = Unit(unit_type, offset_x, offset_y, self.army_id)
                self.add_unit(unit)
    
    def get_army_stats(self) -> dict:
        """Retourne les statistiques de l'armée"""
        alive_units = self.get_alive_units()
        
        stats = {
            'total_units': len(alive_units),
            'total_health': self.get_total_health(),
            'unit_types': {}
        }
        
        for unit_type in UnitType:
            units_of_type = self.get_units_by_type(unit_type)
            stats['unit_types'][unit_type.value] = len(units_of_type)
            
        return stats
    
    def __str__(self):
        """Représentation textuelle de l'armée"""
        alive_count = len(self.get_alive_units())
        total_count = len(self.units)
        return f"Army '{self.name}' ({self.army_id}): {alive_count}/{total_count} units alive"
