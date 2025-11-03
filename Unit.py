"""
MedievAIl Battle Simulator - Classes pour les unités militaires médiévales
"""

import uuid
from enum import Enum
from typing import Tuple, Optional, List

class UnitType(Enum):
    """Types d'unités militaires"""
    KNIGHT = "knight"      # Chevalier - unité lourde, forte en combat rapproché
    ARCHER = "archer"       # Archer - unité à distance, faible en combat rapproché
    SPEARMAN = "spearman"   # Piquier - unité défensive, efficace contre la cavalerie
    SWORDSMAN = "swordsman" # Épéiste - unité polyvalente

class Unit:
    """Classe représentant une unité militaire médiévale"""
    
    def __init__(self, unit_type: UnitType, x: int = 0, y: int = 0, army_id: str = None):
        self.id = str(uuid.uuid4())
        self.unit_type = unit_type
        self.army_id = army_id  # ID de l'armée à laquelle appartient cette unité
        
        # Position
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        
        # Caractéristiques de combat
        self._set_unit_stats()
        
        # État de l'unité
        self.health = self.max_health
        self.is_alive = True
        self.action = "idle"  # idle, move, attack, defend
        
        # Cible actuelle
        self.target_unit: Optional['Unit'] = None
        self.target_position: Optional[Tuple[int, int]] = None
        
    def _set_unit_stats(self):
        """Définit les statistiques selon le type d'unité"""
        if self.unit_type == UnitType.KNIGHT:
            self.max_health = 100
            self.attack_damage = 25
            self.defense = 15
            self.speed = 2
            self.range = 1
            self.symbol = "K"
            self.color = "\033[91m"  # Rouge
            
        elif self.unit_type == UnitType.ARCHER:
            self.max_health = 60
            self.attack_damage = 20
            self.defense = 5
            self.speed = 1
            self.range = 3
            self.symbol = "A"
            self.color = "\033[94m"  # Bleu
            
        elif self.unit_type == UnitType.SPEARMAN:
            self.max_health = 80
            self.attack_damage = 15
            self.defense = 20
            self.speed = 1
            self.range = 1
            self.symbol = "P"
            self.color = "\033[92m"  # Vert
            
        elif self.unit_type == UnitType.SWORDSMAN:
            self.max_health = 90
            self.attack_damage = 20
            self.defense = 10
            self.speed = 2
            self.range = 1
            self.symbol = "S"
            self.color = "\033[93m"  # Jaune
    
    def take_damage(self, damage: int) -> bool:
        """
        Inflige des dégâts à l'unité
        Returns: True si l'unité est encore vivante, False si elle meurt
        """
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            self.action = "dead"
            return False
        
        return True
    
    def attack(self, target: 'Unit') -> bool:
        """
        Attaque une unité cible
        Returns: True si l'attaque réussit, False sinon
        """
        if not self.is_alive or not target.is_alive:
            return False
            
        # Vérifier la portée
        distance = self.get_distance_to(target)
        if distance > self.range:
            return False
            
        # Calculer les dégâts avec bonus selon le type d'unité
        damage = self.attack_damage
        
        # Bonus de dégâts selon les types d'unités
        if self.unit_type == UnitType.SPEARMAN and target.unit_type == UnitType.KNIGHT:
            damage = int(damage * 1.5)  # Bonus contre la cavalerie
        elif self.unit_type == UnitType.ARCHER and target.unit_type == UnitType.SPEARMAN:
            damage = int(damage * 1.3)  # Bonus contre les piquiers
            
        return target.take_damage(damage)
    
    def move_to(self, x: int, y: int):
        """Déplace l'unité vers une nouvelle position"""
        if not self.is_alive:
            return
            
        self.last_x = self.x
        self.last_y = self.y
        self.x = x
        self.y = y
        self.action = "move"
    
    def get_distance_to(self, other: 'Unit') -> int:
        """Calcule la distance de Manhattan vers une autre unité"""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def get_distance_to_position(self, x: int, y: int) -> int:
        """Calcule la distance de Manhattan vers une position"""
        return abs(self.x - x) + abs(self.y - y)
    
    def can_attack(self, target: 'Unit') -> bool:
        """Vérifie si l'unité peut attaquer la cible"""
        if not self.is_alive or not target.is_alive:
            return False
        return self.get_distance_to(target) <= self.range
    
    def __str__(self):
        """Représentation textuelle de l'unité"""
        if not self.is_alive:
            return "X"
        return f"{self.color}{self.symbol}\033[0m"
    
    def get_info(self) -> str:
        """Retourne les informations détaillées de l'unité"""
        status = "Alive" if self.is_alive else "Dead"
        return f"{self.unit_type.value.capitalize()} ({self.symbol}) - HP: {self.health}/{self.max_health} - {status} - Pos: ({self.x}, {self.y})"
