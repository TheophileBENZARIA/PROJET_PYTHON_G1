"""
GUIDE_UTILISATION.md - Guide d'utilisation du MedievAIl Battle Simulator
=======================================================================

Ce guide explique comment utiliser le simulateur de batailles médiévales
et comment créer vos propres scénarios de bataille.

## 📋 Table des matières

1. [Installation et lancement](#installation-et-lancement)
2. [Utilisation de base](#utilisation-de-base)
3. [Création de scénarios personnalisés](#création-de-scénarios-personnalisés)
4. [Configuration avancée](#configuration-avancée)
5. [Exemples pratiques](#exemples-pratiques)
6. [Dépannage](#dépannage)

## 🚀 Installation et lancement

### Prérequis
- Python 3.7 ou plus récent
- Aucune dépendance externe requise

### Lancement rapide
```bash
# Aller dans le dossier du projet
cd medieval_battle_simulator

# Lancer la simulation principale
python main.py

# Lancer les exemples
python examples.py

# Lancer les tests
python test_system.py
```

## 🎮 Utilisation de base

### Simulation simple
```python
from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft

# Créer le moteur de bataille
engine = BattleEngine(width=20, height=15)

# Créer un scénario de test
army1, army2, general1, general2 = engine.create_test_scenario()

# Lancer la bataille
result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)

# Afficher le résultat
print(result.get_summary())
```

### Types d'unités disponibles
- **Knight (K)** : Chevalier - Fort, lent, combat rapproché
- **Archer (A)** : Archer - Faible, portée longue, combat à distance  
- **Spearman (P)** : Piquier - Défensif, bonus contre cavalerie
- **Swordsman (S)** : Épéiste - Polyvalent, équilibré

### Généraux IA disponibles
- **Captain Braindead** : Stratégie défensive passive
- **Major Daft** : Stratégie offensive simple

## 🛠️ Création de scénarios personnalisés

### Créer des armées personnalisées
```python
from Army import Army
from Unit import Unit, UnitType
from General import CaptainBraindead, MajorDaft

# Créer les généraux
general1 = CaptainBraindead()
general2 = MajorDaft()

# Créer l'armée défensive
army_defensive = Army("defensive", "Armée Défensive")
army_defensive.spawn_units_at_position(2, 5, [
    {'type': UnitType.SPEARMAN, 'count': 8},
    {'type': UnitType.ARCHER, 'count': 6},
    {'type': UnitType.KNIGHT, 'count': 2}
])

# Créer l'armée offensive
army_offensive = Army("offensive", "Armée Offensive")
army_offensive.spawn_units_at_position(15, 5, [
    {'type': UnitType.KNIGHT, 'count': 6},
    {'type': UnitType.SWORDSMAN, 'count': 8},
    {'type': UnitType.ARCHER, 'count': 2}
])

# Assigner les armées aux généraux
general1.set_army(army_defensive)
general2.set_army(army_offensive)
```

### Créer des unités individuellement
```python
# Créer des unités à des positions spécifiques
army = Army("custom", "Armée Personnalisée")

# Ajouter des unités une par une
army.add_unit(Unit(UnitType.KNIGHT, 5, 5))    # Chevalier au centre
army.add_unit(Unit(UnitType.ARCHER, 4, 5))    # Archer à gauche
army.add_unit(Unit(UnitType.ARCHER, 6, 5))    # Archer à droite
army.add_unit(Unit(UnitType.SPEARMAN, 5, 4))  # Piquier en avant
```

## ⚙️ Configuration avancée

### Modifier les paramètres de bataille
```python
# Créer un moteur avec des paramètres personnalisés
engine = BattleEngine(
    width=25,        # Largeur du champ
    height=20,       # Hauteur du champ
    max_turns=50     # Nombre maximum de tours
)
```

### Modifier les statistiques des unités
```python
# Les statistiques sont définies dans Unit.py
# Vous pouvez les modifier directement dans le fichier

# Exemple pour un chevalier plus fort :
KNIGHT_STATS = {
    'max_health': 150,    # Plus de santé
    'attack_damage': 30,  # Plus de dégâts
    'defense': 20,        # Plus de défense
    'speed': 1,           # Plus lent
    'range': 1,
    'symbol': 'K',
    'color': '\033[91m'
}
```

## 📚 Exemples pratiques

### Exemple 1 : Bataille équilibrée
```python
from BattleEngine import BattleEngine
from General import CaptainBraindead, MajorDaft

# Créer une bataille équilibrée
engine = BattleEngine(width=15, height=10)
army1, army2, general1, general2 = engine.create_test_scenario()

# Lancer la bataille
result = engine.simulate_battle(army1, army2, general1, general2, verbose=True)
print(f"Résultat : {result.get_summary()}")
```

### Exemple 2 : Test de consistance
```python
# Lancer plusieurs batailles pour tester la consistance
engine = BattleEngine(width=12, height=8, max_turns=20)

braindead_wins = 0
daft_wins = 0

for i in range(10):
    army1, army2, general1, general2 = engine.create_test_scenario()
    result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)
    
    if result.winner == army1:
        braindead_wins += 1
    else:
        daft_wins += 1

print(f"Braindead : {braindead_wins} victoires")
print(f"Daft : {daft_wins} victoires")
```

### Exemple 3 : Analyse des résultats
```python
# Analyser les résultats d'une bataille
result = engine.simulate_battle(army1, army2, general1, general2, verbose=False)

print(f"Tours écoulés : {result.turns_taken}")
print(f"Unités perdues armée 1 : {result.units_lost_army1}")
print(f"Unités perdues armée 2 : {result.units_lost_army2}")
print(f"Actions enregistrées : {len(result.battle_log)}")

# Afficher les dernières actions
for action in result.battle_log[-5:]:
    print(f"  {action}")
```

## 🔧 Dépannage

### Problèmes courants

**Erreur : "Module not found"**
```bash
# Vérifiez que vous êtes dans le bon dossier
cd medieval_battle_simulator
python main.py
```

**Erreur : "Army has no units"**
```python
# Assurez-vous d'ajouter des unités à l'armée avant de l'assigner au général
army = Army("test", "Test Army")
army.add_unit(Unit(UnitType.KNIGHT, 0, 0))  # Ajouter une unité
general.set_army(army)  # Puis assigner l'armée
```

**Bataille qui ne se termine jamais**
```python
# Réduisez le nombre maximum de tours
engine = BattleEngine(width=10, height=8, max_turns=20)
```

### Vérification du système
```bash
# Lancer les tests pour vérifier que tout fonctionne
python test_system.py
```

## 📖 API Reference

### Classes principales

**Unit**
- `Unit(unit_type, x, y)` : Créer une unité
- `attack(target)` : Attaquer une unité cible
- `move_to(x, y)` : Se déplacer vers une position
- `take_damage(damage)` : Subir des dégâts

**Army**
- `Army(army_id, name)` : Créer une armée
- `add_unit(unit)` : Ajouter une unité
- `get_alive_units()` : Récupérer les unités vivantes
- `spawn_units_at_position(x, y, configs)` : Spawner des unités

**General**
- `set_army(army)` : Assigner une armée
- `issue_orders(enemy_army, width, height)` : Donner des ordres

**BattleEngine**
- `BattleEngine(width, height, max_turns)` : Créer le moteur
- `simulate_battle(army1, army2, general1, general2)` : Lancer une bataille
- `create_test_scenario()` : Créer un scénario de test

## 🎯 Prochaines étapes

1. **Créer vos propres généraux IA** en héritant de la classe `General`
2. **Ajouter de nouveaux types d'unités** dans `Unit.py`
3. **Implémenter des scénarios complexes** avec plusieurs armées
4. **Créer une interface graphique** pour visualiser les batailles
5. **Organiser des tournois automatiques** entre plusieurs généraux

## 📞 Support

Si vous rencontrez des problèmes ou avez des questions :
1. Vérifiez que tous les fichiers sont présents
2. Lancez `python test_system.py` pour diagnostiquer les problèmes
3. Consultez les exemples dans `examples.py`
4. Vérifiez la configuration dans `config.py`
