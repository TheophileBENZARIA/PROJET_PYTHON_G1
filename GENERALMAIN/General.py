<<<<<<< HEAD
"""
General.py - Classes pour les généraux IA
==========================================

Ce module contient les classes pour les généraux IA qui commandent les armées.
Il définit une classe abstraite General et deux implémentations concrètes :
- CaptainBraindead : Général défensif qui ne donne aucun ordre proactif
- MajorDaft : Général agressif qui attaque l'ennemi le plus proche

Architecture :
- General (classe abstraite) : Définit l'interface commune à tous les généraux
- CaptainBraindead : Stratégie défensive passive
- MajorDaft : Stratégie offensive simple

Chaque général doit implémenter la méthode issue_orders() qui définit sa stratégie.
"""

from abc import ABC  # Pour créer une classe abstraite
from backend.Class.Units import units


class General(ABC):  
    """
    Classe abstraite pour les généraux IA
    
    Cette classe définit l'interface commune à tous les généraux.
    Elle utilise le pattern Abstract Base Class pour forcer les classes filles
    à implémenter la méthode issue_orders().
    
    Attributs :
        name (str) : Nom du général
        army (Optional[Army]) : Armée assignée à ce général (peut être None)
    
    Méthodes :
        set_army(army) : Assigne une armée au général
        issue_orders() : Méthode abstraite à implémenter par les classes filles
        get_name() : Retourne le nom du général
    """
    
    def __init__(self, name: str):  
        """
        Constructeur de la classe General
        
        Args:
            name (str) : Nom du général (ex: "Captain Braindead")
        """
        self.name = name  
        self.army: Optional[army] = None
    
    def set_army(self, army: army):
        """
        Assigne une armée à ce général
        
        Cette méthode permet d'associer une armée au général.
        L'armée doit être créée et peuplée d'unités avant d'être assignée.
        
        Args:
            army (Army) : L'armée à assigner au général
            
        Example:
            general = CaptainBraindead()
            army = Army("army_1", "Armée Rouge")
            general.set_army(army)  # Le général commande maintenant cette armée
        """
        self.army = army 
    
     
    def issue_orders(self, enemy_army: army, battlefield_width: int, battlefield_height: int) -> List[str]:
        """
        Donne des ordres à toutes les unités de l'armée
        
        Cette méthode abstraite doit être implémentée par chaque classe fille.
        Elle définit la stratégie du général en donnant des ordres à ses unités.
        
        Args:
            enemy_army (Army) : L'armée ennemie à combattre
            battlefield_width (int) : Largeur du champ de bataille
            battlefield_height (int) : Hauteur du champ de bataille
            
        Returns:
            List[str] : Liste des actions effectuées (pour le debug/affichage)
            
        Note:
            Cette méthode est appelée à chaque tour de bataille par le BattleEngine.
            Chaque général implémente sa propre stratégie dans cette méthode.
        """
        pass 
    
    def get_name(self) -> str:
        """Retourne le nom du général"""
        return self.name

class CaptainBraindead(General):
    """
    Captain Braindead - Général défensif passif
    
    Stratégie : Aucune stratégie proactive. Ses unités restent sur place
    et ne réagissent que si elles sont attaquées directement.
    
    - Ne donne aucun ordre stratégique
    - Ne bouge pas si aucun ennemi n'est visible
    - Attaque un ennemi visible dans sa ligne de vue
    - Se déplace vers l'ennemi uniquement s'il est visible
    - Réagit uniquement aux stimuli (vue / attaque)
    
    Utilisation : Général de référence pour tester les IA plus intelligentes.
    Permet de voir comment une armée défensive se comporte contre une armée offensive.
    """
    
    def __init__(self):
        """
        Constructeur de Captain Braindead
        
        Initialise le général avec son nom caractéristique.
        """
        super().__init__("Captain Braindead")  
    
    def issue_orders(self, enemy_army: army, battlefield_width: int, battlefield_height: int) -> List[str]:
        """
        Captain Braindead ne donne aucun ordre         
        Cette méthode implémente la stratégie défensive passive de Braindead.
        Toutes ses unités restent en position défensive et ne bougent pas.
        
        Args:
            enemy_army (Army) : L'armée ennemie (ignorée par Braindead)
            battlefield_width (int) : Largeur du champ (ignorée)
            battlefield_height (int) : Hauteur du champ (ignorée)
            
        Returns:
            List[str] : Liste des actions défensives effectuées
            
        Note:
            Cette stratégie est volontairement simple pour servir de baseline.
            Elle permet de tester les IA plus agressives comme Major Daft.
        """
        actions = []  
   
        if not self.army:
            return actions  
            
       
        alive_units = self.army.get_alive_units()
        
       
        for unit in alive_units:
                        # Cherche les ennemis dans la ligne de vue
            visible_enemies = unit.get_enemies_in_line_of_sight(enemy_army)

            if visible_enemies:
                # Prenons simplement le premier ennemi visible
                target = visible_enemies[0]

                # Si à portée -> attaque
                if unit.is_in_attack_range(target):
                    unit.action = "attack"
                    unit.target = target
                    actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) attacks enemy at ({target.x}, {target.y})")
                else:
                    # Sinon -> avance vers l'ennemi visible
                    unit.action = "move"
                    unit.move_towards(target.x, target.y)
                    actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) moves toward enemy at ({target.x}, {target.y})")
            else:
                # Aucun ennemi visible -> reste en position défensive
           
                unit.action = "defend"
         
                actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) stays in defensive position")
        
        return actions  

class MajorDaft(General):
    """
    Major Daft - Général agressif simple
    
    Stratégie : Attaque agressive et directe. Toutes ses unités se dirigent
    vers l'ennemi le plus proche et l'attaquent dès qu'elles sont à portée.
    
    Comportement :
    - Trouve l'ennemi le plus proche pour chaque unité
    - Se déplace vers l'ennemi si pas à portée d'attaque
    - Attaque l'ennemi dès qu'il est à portée
    - Pas de stratégie complexe, juste "attaque tout ce qui bouge"
    
    Utilisation : Général agressif de base pour tester les défenses.
    Montre comment une armée offensive se comporte contre une armée défensive.
    """
    
    def __init__(self):
        """
        Constructeur de Major Daft
        
        Initialise le général avec son nom caractéristique.
        """
        super().__init__("Major Daft")  # Appelle le constructeur parent avec le nom
    
    def issue_orders(self, enemy_army: army, battlefield_width: int, battlefield_height: int) -> List[str]:
        """
        Major Daft ordonne à toutes ses unités d'avancer vers l'ennemi le plus proche
        
        Cette méthode implémente la stratégie agressive de Daft :
        1. Pour chaque unité, trouve l'ennemi le plus proche
        2. Si l'ennemi est à portée d'attaque → attaque
        3. Sinon → se déplace vers l'ennemi
        
        Args:
            enemy_army (Army) : L'armée ennemie à combattre
            battlefield_width (int) : Largeur du champ de bataille
            battlefield_height (int) : Hauteur du champ de bataille
            
        Returns:
            List[str] : Liste des actions offensives effectuées
            
        Note:
            Cette stratégie est simple mais efficace contre des défenses statiques.
            Elle peut être facilement battue par des stratégies plus sophistiquées.
        """
        actions = []  
        
        
        if not self.army:
            return actions  
            
       
        alive_units = self.army.get_alive_units()
        
        alive_enemies = enemy_army.get_alive_units()
        
        
        if not alive_enemies:
            return actions 
        
        
        for unit in alive_units:
            # Trouver l'ennemi le plus proche de cette unité
            closest_enemy = self._find_closest_enemy(unit, alive_enemies)
            
            if closest_enemy: 
                
                if unit.can_attack(closest_enemy):
                   
                    unit.target_unit = closest_enemy  # Définit la cible
                    unit.action = "attack"  
                    # Ajoute un message d'attaque à la liste
                    actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) attacks enemy at ({closest_enemy.x}, {closest_enemy.y})")
                else:
                    # L'ennemi n'est pas à portée → SE DÉPLACER !
                    new_position = self._move_towards_target(unit, closest_enemy, battlefield_width, battlefield_height)
                    
                    
                    if new_position != (unit.x, unit.y):
                       
                        unit.move_to(new_position[0], new_position[1])
                        unit.target_unit = closest_enemy  # Définit la cible pour le prochain tour
                        # Ajoute un message de déplacement à la liste
                        actions.append(f"{unit.unit_type.value} moves from ({unit.last_x}, {unit.last_y}) to ({unit.x}, {unit.y})")
                    else:
                        # L'unité ne peut pas bouger (bloquée par les limites du champ)
                        unit.action = "idle"  # Met l'action à "idle"
                        # Ajoute un message d'immobilité à la liste
                        actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) cannot move closer to enemy")
            else:
                # Aucun ennemi trouvé (ne devrait pas arriver normalement)
                unit.action = "idle"  # Met l'action à "idle"
                # Ajoute un message d'absence d'ennemi à la liste
                actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) has no enemies to target")
        
        return actions  # Retourne la liste des actions offensives
    
    def _find_closest_enemy(self, unit: units, enemies: List[units]) -> Optional[units]:
        """
        Trouve l'ennemi le plus proche d'une unité donnée
        
        Cette méthode helper calcule la distance de Manhattan entre l'unité
        et tous les ennemis, puis retourne l'ennemi le plus proche.
        
        Args:
            unit (Unit) : L'unité pour laquelle chercher l'ennemi le plus proche
            enemies (List[Unit]) : Liste des ennemis à considérer
            
        Returns:
            Optional[Unit] : L'ennemi le plus proche, ou None si la liste est vide
            
        Note:
            Utilise la distance de Manhattan (|x1-x2| + |y1-y2|) pour calculer
            la proximité. Cette distance est appropriée pour un mouvement sur grille.
        """
        
        if not enemies:
            return None
            
        closest_enemy = None  
        min_distance = float('inf')  # Distance minimale (commence à l'infini)
        
        
        for enemy in enemies:
            
            distance = unit.get_distance_to(enemy)
            
            # Si cette distance est plus petite que la distance minimale actuelle
            if distance < min_distance:
                min_distance = distance 
                closest_enemy = enemy  
                
        return closest_enemy  # Retourner l'ennemi le plus proche trouvé
    
    def _move_towards_target(self, unit: units, target: units, battlefield_width: int, battlefield_height: int) -> Tuple[int, int]:
        """
        Calcule la nouvelle position pour se rapprocher de la cible
        
        Cette méthode helper calcule la meilleure position pour une unité
        afin qu'elle se rapproche de sa cible, en respectant les limites du champ de bataille.
   
            
        Returns:
            Tuple[int, int] : Nouvelle position (x, y) pour l'unité
            
        Note:
            La stratégie de déplacement privilégie le mouvement horizontal
            si la distance horizontale est plus grande que la verticale.
            Cela évite les mouvements en diagonale et simplifie la logique.
        """
        # Calculer la direction vers la cible
        dx = target.x - unit.x  # Différence en X (positif = cible à droite)
        dy = target.y - unit.y  # Différence en Y (positif = cible en bas)
        
        # Si l'unité est déjà sur la cible, ne pas bouger
        if dx == 0 and dy == 0:
            return (unit.x, unit.y)  # Retourner la position actuelle
        
        # Initialiser la nouvelle position avec la position actuelle
        new_x = unit.x
        new_y = unit.y
        
        # Déterminer la direction de mouvement selon la distance la plus grande
        if abs(dx) > abs(dy):
            # La distance horizontale est plus grande → se déplacer horizontalement
            if dx > 0:  # Cible à droite
                # Se déplacer vers la droite (limité par la vitesse et les limites du champ)
                new_x = min(unit.x + unit.speed, battlefield_width - 1)
            else:  # Cible à gauche
                # Se déplacer vers la gauche (limité par la vitesse et les limites du champ)
                new_x = max(unit.x - unit.speed, 0)
        else:
            # La distance verticale est plus grande ou égale → se déplacer verticalement
            if dy > 0:  # Cible en bas
                # Se déplacer vers le bas (limité par la vitesse et les limites du champ)
                new_y = min(unit.y + unit.speed, battlefield_height - 1)
            else:  # Cible en haut
                # Se déplacer vers le haut (limité par la vitesse et les limites du champ)
                new_y = max(unit.y - unit.speed, 0)
        
        # Vérifier et corriger les limites du champ de bataille
        # S'assurer que les coordonnées restent dans les limites [0, width-1] et [0, height-1]
        new_x = max(0, min(new_x, battlefield_width - 1))
        new_y = max(0, min(new_y, battlefield_height - 1))
        
        return (new_x, new_y)  # Retourner la nouvelle position calculée
=======
"""
General.py - Classes pour les généraux IA
==========================================

Ce module contient les classes pour les généraux IA qui commandent les armées.
Il définit une classe abstraite General et deux implémentations concrètes :
- CaptainBraindead : Général défensif qui ne donne aucun ordre proactif
- MajorDaft : Général agressif qui attaque l'ennemi le plus proche

Architecture :
- General (classe abstraite) : Définit l'interface commune à tous les généraux
- CaptainBraindead : Stratégie défensive passive
- MajorDaft : Stratégie offensive simple

Chaque général doit implémenter la méthode issue_orders() qui définit sa stratégie.
"""

from abc import ABC  # Pour créer une classe abstraite
from typing import List, Optional, Tuple  # Pour le typage des variables
from backend import units  # Import de notre classe Unit
from backend.Class import army


class General(ABC):  
    """
    Classe abstraite pour les généraux IA
    
    Cette classe définit l'interface commune à tous les généraux.
    Elle utilise le pattern Abstract Base Class pour forcer les classes filles
    à implémenter la méthode issue_orders().
    
    Attributs :
        name (str) : Nom du général
        army (Optional[Army]) : Armée assignée à ce général (peut être None)
    
    Méthodes :
        set_army(army) : Assigne une armée au général
        issue_orders() : Méthode abstraite à implémenter par les classes filles
        get_name() : Retourne le nom du général
    """
    
    def __init__(self, name: str):  
        """
        Constructeur de la classe General
        
        Args:
            name (str) : Nom du général (ex: "Captain Braindead")
        """
        self.name = name  
        self.army: Optional[army] = None
    
    def set_army(self, army: army):
        """
        Assigne une armée à ce général
        
        Cette méthode permet d'associer une armée au général.
        L'armée doit être créée et peuplée d'unités avant d'être assignée.
        
        Args:
            army (Army) : L'armée à assigner au général
            
        Example:
            general = CaptainBraindead()
            army = Army("army_1", "Armée Rouge")
            general.set_army(army)  # Le général commande maintenant cette armée
        """
        self.army = army 
    
     
    def issue_orders(self, enemy_army: army, battlefield_width: int, battlefield_height: int) -> List[str]:
        """
        Donne des ordres à toutes les unités de l'armée
        
        Cette méthode abstraite doit être implémentée par chaque classe fille.
        Elle définit la stratégie du général en donnant des ordres à ses unités.
        
        Args:
            enemy_army (Army) : L'armée ennemie à combattre
            battlefield_width (int) : Largeur du champ de bataille
            battlefield_height (int) : Hauteur du champ de bataille
            
        Returns:
            List[str] : Liste des actions effectuées (pour le debug/affichage)
            
        Note:
            Cette méthode est appelée à chaque tour de bataille par le BattleEngine.
            Chaque général implémente sa propre stratégie dans cette méthode.
        """
        pass 
    
    def get_name(self) -> str:
        """Retourne le nom du général"""
        return self.name

class CaptainBraindead(General):
    """
    Captain Braindead - Général défensif passif
    
    Stratégie : Aucune stratégie proactive. Ses unités restent sur place
    et ne réagissent que si elles sont attaquées directement.
    
    - Ne donne aucun ordre stratégique
    - Ne bouge pas si aucun ennemi n'est visible
    - Attaque un ennemi visible dans sa ligne de vue
    - Se déplace vers l'ennemi uniquement s'il est visible
    - Réagit uniquement aux stimuli (vue / attaque)
    
    Utilisation : Général de référence pour tester les IA plus intelligentes.
    Permet de voir comment une armée défensive se comporte contre une armée offensive.
    """
    
    def __init__(self):
        """
        Constructeur de Captain Braindead
        
        Initialise le général avec son nom caractéristique.
        """
        super().__init__("Captain Braindead")  
    
    def issue_orders(self, enemy_army: army, battlefield_width: int, battlefield_height: int) -> List[str]:
        """
        Captain Braindead ne donne aucun ordre         
        Cette méthode implémente la stratégie défensive passive de Braindead.
        Toutes ses unités restent en position défensive et ne bougent pas.
        
        Args:
            enemy_army (Army) : L'armée ennemie (ignorée par Braindead)
            battlefield_width (int) : Largeur du champ (ignorée)
            battlefield_height (int) : Hauteur du champ (ignorée)
            
        Returns:
            List[str] : Liste des actions défensives effectuées
            
        Note:
            Cette stratégie est volontairement simple pour servir de baseline.
            Elle permet de tester les IA plus agressives comme Major Daft.
        """
        actions = []  
   
        if not self.army:
            return actions  
            
       
        alive_units = self.army.get_alive_units()
        
       
        for unit in alive_units:
                        # Cherche les ennemis dans la ligne de vue
            visible_enemies = unit.get_enemies_in_line_of_sight(enemy_army)

            if visible_enemies:
                # Prenons simplement le premier ennemi visible
                target = visible_enemies[0]

                # Si à portée -> attaque
                if unit.is_in_attack_range(target):
                    unit.action = "attack"
                    unit.target = target
                    actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) attacks enemy at ({target.x}, {target.y})")
                else:
                    # Sinon -> avance vers l'ennemi visible
                    unit.action = "move"
                    unit.move_towards(target.x, target.y)
                    actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) moves toward enemy at ({target.x}, {target.y})")
            else:
                # Aucun ennemi visible -> reste en position défensive
           
                unit.action = "defend"
         
                actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) stays in defensive position")
        
        return actions  

class MajorDaft(General):
    """
    Major Daft - Général agressif simple
    
    Stratégie : Attaque agressive et directe. Toutes ses unités se dirigent
    vers l'ennemi le plus proche et l'attaquent dès qu'elles sont à portée.
    
    Comportement :
    - Trouve l'ennemi le plus proche pour chaque unité
    - Se déplace vers l'ennemi si pas à portée d'attaque
    - Attaque l'ennemi dès qu'il est à portée
    - Pas de stratégie complexe, juste "attaque tout ce qui bouge"
    
    Utilisation : Général agressif de base pour tester les défenses.
    Montre comment une armée offensive se comporte contre une armée défensive.
    """
    
    def __init__(self):
        """
        Constructeur de Major Daft
        
        Initialise le général avec son nom caractéristique.
        """
        super().__init__("Major Daft")  # Appelle le constructeur parent avec le nom
    
    def issue_orders(self, enemy_army: army, battlefield_width: int, battlefield_height: int) -> List[str]:
        """
        Major Daft ordonne à toutes ses unités d'avancer vers l'ennemi le plus proche
        
        Cette méthode implémente la stratégie agressive de Daft :
        1. Pour chaque unité, trouve l'ennemi le plus proche
        2. Si l'ennemi est à portée d'attaque → attaque
        3. Sinon → se déplace vers l'ennemi
        
        Args:
            enemy_army (Army) : L'armée ennemie à combattre
            battlefield_width (int) : Largeur du champ de bataille
            battlefield_height (int) : Hauteur du champ de bataille
            
        Returns:
            List[str] : Liste des actions offensives effectuées
            
        Note:
            Cette stratégie est simple mais efficace contre des défenses statiques.
            Elle peut être facilement battue par des stratégies plus sophistiquées.
        """
        actions = []  
        
        
        if not self.army:
            return actions  
            
       
        alive_units = self.army.get_alive_units()
        
        alive_enemies = enemy_army.get_alive_units()
        
        
        if not alive_enemies:
            return actions 
        
        
        for unit in alive_units:
            # Trouver l'ennemi le plus proche de cette unité
            closest_enemy = self._find_closest_enemy(unit, alive_enemies)
            
            if closest_enemy: 
                
                if unit.can_attack(closest_enemy):
                   
                    unit.target_unit = closest_enemy  # Définit la cible
                    unit.action = "attack"  
                    # Ajoute un message d'attaque à la liste
                    actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) attacks enemy at ({closest_enemy.x}, {closest_enemy.y})")
                else:
                    # L'ennemi n'est pas à portée → SE DÉPLACER !
                    new_position = self._move_towards_target(unit, closest_enemy, battlefield_width, battlefield_height)
                    
                    
                    if new_position != (unit.x, unit.y):
                       
                        unit.move_to(new_position[0], new_position[1])
                        unit.target_unit = closest_enemy  # Définit la cible pour le prochain tour
                        # Ajoute un message de déplacement à la liste
                        actions.append(f"{unit.unit_type.value} moves from ({unit.last_x}, {unit.last_y}) to ({unit.x}, {unit.y})")
                    else:
                        # L'unité ne peut pas bouger (bloquée par les limites du champ)
                        unit.action = "idle"  # Met l'action à "idle"
                        # Ajoute un message d'immobilité à la liste
                        actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) cannot move closer to enemy")
            else:
                # Aucun ennemi trouvé (ne devrait pas arriver normalement)
                unit.action = "idle"  # Met l'action à "idle"
                # Ajoute un message d'absence d'ennemi à la liste
                actions.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) has no enemies to target")
        
        return actions  # Retourne la liste des actions offensives
    
    def _find_closest_enemy(self, unit: units, enemies: List[units]) -> Optional[units]:
        """
        Trouve l'ennemi le plus proche d'une unité donnée
        
        Cette méthode helper calcule la distance de Manhattan entre l'unité
        et tous les ennemis, puis retourne l'ennemi le plus proche.
        
        Args:
            unit (Unit) : L'unité pour laquelle chercher l'ennemi le plus proche
            enemies (List[Unit]) : Liste des ennemis à considérer
            
        Returns:
            Optional[Unit] : L'ennemi le plus proche, ou None si la liste est vide
            
        Note:
            Utilise la distance de Manhattan (|x1-x2| + |y1-y2|) pour calculer
            la proximité. Cette distance est appropriée pour un mouvement sur grille.
        """
        
        if not enemies:
            return None
            
        closest_enemy = None  
        min_distance = float('inf')  # Distance minimale (commence à l'infini)
        
        
        for enemy in enemies:
            
            distance = unit.get_distance_to(enemy)
            
            # Si cette distance est plus petite que la distance minimale actuelle
            if distance < min_distance:
                min_distance = distance 
                closest_enemy = enemy  
                
        return closest_enemy  # Retourner l'ennemi le plus proche trouvé
    
    def _move_towards_target(self, unit: units, target: units, battlefield_width: int, battlefield_height: int) -> Tuple[int, int]:
        """
        Calcule la nouvelle position pour se rapprocher de la cible
        
        Cette méthode helper calcule la meilleure position pour une unité
        afin qu'elle se rapproche de sa cible, en respectant les limites du champ de bataille.
   
            
        Returns:
            Tuple[int, int] : Nouvelle position (x, y) pour l'unité
            
        Note:
            La stratégie de déplacement privilégie le mouvement horizontal
            si la distance horizontale est plus grande que la verticale.
            Cela évite les mouvements en diagonale et simplifie la logique.
        """
        # Calculer la direction vers la cible
        dx = target.x - unit.x  # Différence en X (positif = cible à droite)
        dy = target.y - unit.y  # Différence en Y (positif = cible en bas)
        
        # Si l'unité est déjà sur la cible, ne pas bouger
        if dx == 0 and dy == 0:
            return (unit.x, unit.y)  # Retourner la position actuelle
        
        # Initialiser la nouvelle position avec la position actuelle
        new_x = unit.x
        new_y = unit.y
        
        # Déterminer la direction de mouvement selon la distance la plus grande
        if abs(dx) > abs(dy):
            # La distance horizontale est plus grande → se déplacer horizontalement
            if dx > 0:  # Cible à droite
                # Se déplacer vers la droite (limité par la vitesse et les limites du champ)
                new_x = min(unit.x + unit.speed, battlefield_width - 1)
            else:  # Cible à gauche
                # Se déplacer vers la gauche (limité par la vitesse et les limites du champ)
                new_x = max(unit.x - unit.speed, 0)
        else:
            # La distance verticale est plus grande ou égale → se déplacer verticalement
            if dy > 0:  # Cible en bas
                # Se déplacer vers le bas (limité par la vitesse et les limites du champ)
                new_y = min(unit.y + unit.speed, battlefield_height - 1)
            else:  # Cible en haut
                # Se déplacer vers le haut (limité par la vitesse et les limites du champ)
                new_y = max(unit.y - unit.speed, 0)
        
        # Vérifier et corriger les limites du champ de bataille
        # S'assurer que les coordonnées restent dans les limites [0, width-1] et [0, height-1]
        new_x = max(0, min(new_x, battlefield_width - 1))
        new_y = max(0, min(new_y, battlefield_height - 1))
        
        return (new_x, new_y)  # Retourner la nouvelle position calculée
>>>>>>> 71325c1 (Initial commit)
