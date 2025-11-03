"""
MedievAIl Battle Simulator - Documentation Complète
====================================================

Ce projet simule des batailles médiévales automatiques entre des généraux IA.
Inspiré d'Age of Empires II, mais entièrement automatisé avec des IA qui commandent les armées.

## 🏗️ Architecture du Projet

### Classes Principales :
1. **Unit** - Représente une unité militaire (chevalier, archer, etc.)
2. **Army** - Représente une armée composée d'unités
3. **General** - Classe abstraite pour les généraux IA
4. **CaptainBraindead** - Général défensif (ne bouge pas)
5. **MajorDaft** - Général agressif (attaque tout)
6. **BattleEngine** - Moteur de bataille qui orchestre les combats

### Types d'Unités :
- **Knight (K)** - Chevalier : Fort, lent, combat rapproché
- **Archer (A)** - Archer : Faible, portée longue, combat à distance
- **Spearman (P)** - Piquier : Défensif, bonus contre cavalerie
- **Swordsman (S)** - Épéiste : Polyvalent, équilibré

## 🎯 Objectifs du Projet

1. Créer un moteur de combat fonctionnel
2. Implémenter deux généraux IA de base
3. Permettre des simulations de batailles automatiques
4. Préparer l'extension avec des IA plus intelligentes
5. Organiser des tournois entre généraux

## 🚀 Utilisation

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

## 📊 Résultats de Bataille

Chaque bataille produit un objet `BattleResult` contenant :
- Le gagnant et le perdant
- Nombre de tours écoulés
- Unités perdues par armée
- Log complet des actions
- Statut (victoire/défaite/match nul)

## 🔧 Extension Future

Le projet est conçu pour être facilement extensible :
- Ajouter de nouveaux types d'unités
- Créer des généraux IA plus intelligents
- Implémenter des scénarios de bataille complexes
- Ajouter une interface graphique
- Organiser des tournois automatiques

## 📁 Structure des Fichiers

```
medieval_battle_simulator/
├── Unit.py           # Classes des unités militaires
├── Army.py           # Gestion des armées
├── General.py         # Généraux IA (Braindead, Daft)
├── BattleEngine.py   # Moteur de bataille principal
├── main.py           # Point d'entrée du programme
└── README.md         # Cette documentation
```
"""
