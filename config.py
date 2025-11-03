"""
config.py - Configuration du MedievAIl Battle Simulator
======================================================

Ce fichier contient toutes les constantes et paramètres de configuration
utilisés dans le simulateur de batailles médiévales.

Modifiez ces valeurs pour ajuster le comportement du simulateur selon vos besoins.
"""

# =============================================================================
# CONFIGURATION DU CHAMP DE BATAILLE
# =============================================================================

# Taille par défaut du champ de bataille
DEFAULT_BATTLEFIELD_WIDTH = 20
DEFAULT_BATTLEFIELD_HEIGHT = 15

# Nombre maximum de tours par bataille (évite les batailles infinies)
DEFAULT_MAX_TURNS = 100

# =============================================================================
# CONFIGURATION DES UNITÉS
# =============================================================================

# Statistiques des chevaliers
KNIGHT_STATS = {
    'max_health': 100,
    'attack_damage': 25,
    'defense': 15,
    'speed': 2,
    'range': 1,
    'symbol': 'K',
    'color': '\033[91m'  # Rouge
}

# Statistiques des archers
ARCHER_STATS = {
    'max_health': 60,
    'attack_damage': 20,
    'defense': 5,
    'speed': 1,
    'range': 3,
    'symbol': 'A',
    'color': '\033[94m'  # Bleu
}

# Statistiques des piquiers
SPEARMAN_STATS = {
    'max_health': 80,
    'attack_damage': 15,
    'defense': 20,
    'speed': 1,
    'range': 1,
    'symbol': 'P',
    'color': '\033[92m'  # Vert
}

# Statistiques des épéistes
SWORDSMAN_STATS = {
    'max_health': 90,
    'attack_damage': 20,
    'defense': 10,
    'speed': 2,
    'range': 1,
    'symbol': 'S',
    'color': '\033[93m'  # Jaune
}

# =============================================================================
# BONUS DE COMBAT ENTRE TYPES D'UNITÉS
# =============================================================================

# Bonus de dégâts des piquiers contre les chevaliers
SPEARMAN_VS_KNIGHT_BONUS = 1.5

# Bonus de dégâts des archers contre les piquiers
ARCHER_VS_SPEARMAN_BONUS = 1.3

# =============================================================================
# CONFIGURATION DES SCÉNARIOS DE TEST
# =============================================================================

# Configuration de l'armée défensive (Captain Braindead)
DEFENSIVE_ARMY_CONFIG = {
    'position': (2, 5),  # Position de spawn
    'units': [
        {'type': 'knight', 'count': 3},
        {'type': 'archer', 'count': 5},
        {'type': 'spearman', 'count': 4}
    ]
}

# Configuration de l'armée offensive (Major Daft)
OFFENSIVE_ARMY_CONFIG = {
    'position': (15, 5),  # Position de spawn
    'units': [
        {'type': 'knight', 'count': 4},
        {'type': 'archer', 'count': 3},
        {'type': 'swordsman', 'count': 5}
    ]
}

# =============================================================================
# CONFIGURATION DE L'AFFICHAGE
# =============================================================================

# Caractères pour l'affichage du champ de bataille
BATTLEFIELD_EMPTY_CHAR = '.'
BATTLEFIELD_BORDER_CHAR = '│'
BATTLEFIELD_CORNER_CHARS = {
    'top_left': '╭',
    'top_right': '╮',
    'bottom_left': '╰',
    'bottom_right': '╯'
}

# Couleurs pour l'affichage
COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

# =============================================================================
# CONFIGURATION DES MESSAGES
# =============================================================================

# Messages d'état des unités
UNIT_MESSAGES = {
    'defend': "reste en position défensive",
    'attack': "attaque l'ennemi",
    'move': "se déplace vers l'ennemi",
    'idle': "reste immobile",
    'dead': "est éliminé"
}

# Messages de bataille
BATTLE_MESSAGES = {
    'start': "Début de la bataille",
    'end': "Fin de la bataille",
    'victory': "Victoire",
    'defeat': "Défaite",
    'draw': "Match nul",
    'turn': "Tour"
}

# =============================================================================
# CONFIGURATION DES TESTS
# =============================================================================

# Nombre de batailles pour les tests de consistance
CONSISTENCY_TEST_BATTLES = 5

# Nombre de batailles pour les tournois
TOURNAMENT_BATTLES = 10

# Configuration pour les batailles rapides (tests)
QUICK_BATTLE_CONFIG = {
    'width': 12,
    'height': 8,
    'max_turns': 20
}

# =============================================================================
# CONFIGURATION DES GÉNÉRAUX IA
# =============================================================================

# Noms des généraux
GENERAL_NAMES = {
    'braindead': 'Captain Braindead',
    'daft': 'Major Daft'
}

# Descriptions des stratégies
STRATEGY_DESCRIPTIONS = {
    'braindead': 'Stratégie défensive passive - reste sur place',
    'daft': 'Stratégie offensive simple - attaque l\'ennemi le plus proche'
}

# =============================================================================
# FONCTIONS UTILITAIRES DE CONFIGURATION
# =============================================================================

def get_unit_stats(unit_type: str) -> dict:
    """
    Retourne les statistiques d'un type d'unité
    
    Args:
        unit_type (str) : Type d'unité ('knight', 'archer', 'spearman', 'swordsman')
        
    Returns:
        dict : Dictionnaire contenant les statistiques de l'unité
    """
    stats_map = {
        'knight': KNIGHT_STATS,
        'archer': ARCHER_STATS,
        'spearman': SPEARMAN_STATS,
        'swordsman': SWORDSMAN_STATS
    }
    
    return stats_map.get(unit_type.lower(), KNIGHT_STATS)

def get_battlefield_size(size_name: str) -> tuple:
    """
    Retourne la taille du champ de bataille selon un nom prédéfini
    
    Args:
        size_name (str) : Nom de la taille ('small', 'medium', 'large')
        
    Returns:
        tuple : (width, height) du champ de bataille
    """
    sizes = {
        'small': (10, 8),
        'medium': (15, 10),
        'large': (20, 15),
        'huge': (30, 20)
    }
    
    return sizes.get(size_name.lower(), (DEFAULT_BATTLEFIELD_WIDTH, DEFAULT_BATTLEFIELD_HEIGHT))

def get_color_code(color_name: str) -> str:
    """
    Retourne le code couleur ANSI pour un nom de couleur
    
    Args:
        color_name (str) : Nom de la couleur
        
    Returns:
        str : Code couleur ANSI
    """
    return COLORS.get(color_name.lower(), COLORS['reset'])

# =============================================================================
# CONFIGURATION DE DÉVELOPPEMENT
# =============================================================================

# Mode debug (affiche plus d'informations)
DEBUG_MODE = False

# Sauvegarder les logs de bataille
SAVE_BATTLE_LOGS = True

# Dossier pour les logs
LOG_DIRECTORY = "battle_logs"

# Format des logs
LOG_FORMAT = "%Y-%m-%d_%H-%M-%S"
