# 🏰 MedievAIl Battle Simulator - Architecture Visuelle

## 📊 Schéma de l'Architecture du Projet

```
┌─────────────────────────────────────────────────────────────┐
│                    MEDIEVAIL BATTLE SIMULATOR                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🎮 MAIN.PY    │    │  🧪 TESTS       │    │ 📚 DOCS         │
│                 │    │                 │    │                 │
│ • Point d'entrée│    │ • test_system   │    │ • README.md     │
│ • Configuration │    │ • test_generals │    │ • GUIDE_UTIL    │
│ • Lancement     │    │ • test_visuel   │    │ • PROJET_COMPLET│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  ⚔️ BATTLE ENGINE │
                    │                 │
                    │ • Gestion tours │
                    │ • Résolution    │
                    │ • Conditions    │
                    │ • Affichage     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   🤖 GENERALS    │
                    │                 │
                    │ • Captain       │
                    │   Braindead     │
                    │ • Major Daft    │
                    │ • Stratégies    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   🏰 ARMIES      │
                    │                 │
                    │ • Collection    │
                    │ • Gestion       │
                    │ • Commandement   │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   ⚔️ UNITS       │
                    │                 │
                    │ • Knight        │
                    │ • Archer        │
                    │ • Spearman      │
                    │ • Swordsman     │
                    └─────────────────┘
```

## 🧠 Architecture des IA (Votre Partie)

```
┌─────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE ARTIFICIELLE                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐                    ┌─────────────────┐
│ 🛡️ BRAINDEAD    │                    │ ⚔️ MAJOR DAFT   │
│                 │                    │                 │
│ STRATÉGIE:      │                    │ STRATÉGIE:      │
│ • Défensive     │                    │ • Agressive     │
│ • Statique      │                    │ • Mobile        │
│ • Réactive      │                    │ • Proactive     │
│                 │                    │                 │
│ COMPORTEMENT:   │                    │ COMPORTEMENT:   │
│ • Reste en place│                    │ • Avance        │
│ • Attend attaque│                    │ • Cherche ennemi│
│ • Contre-attaque│                    │ • Attaque       │
└─────────────────┘                    └─────────────────┘
         │                                       │
         └─────────────────┬─────────────────────┘
                           │
                ┌─────────────────┐
                │  🎯 DÉCISIONS   │
                │                 │
                │ • Mouvement      │
                │ • Attaque        │
                │ • Défense        │
                │ • Position       │
                └─────────────────┘
```

## 📁 Structure des Fichiers

```
medieval_battle_simulator/
├── 🧠 General.py              ← VOS IA (Braindead & Daft)
├── ⚔️ BattleEngine.py         ← Moteur de bataille
├── 🏰 Army.py                 ← Gestion des armées
├── ⚔️ Unit.py                 ← Types d'unités
├── 🎮 main.py                 ← Programme principal
├── 🧪 test_system.py          ← Tests complets
├── 🧪 test_generals.py        ← Tests des IA
├── 🧪 test_visuel_simple.py   ← Tests visuels
├── 📚 README.md               ← Documentation
├── 📚 GUIDE_UTILISATION.md    ← Guide d'usage
└── 📚 PROJET_COMPLET.md       ← Documentation complète
```

## 🔍 Ce qui manque sur GitHub pour votre partie IA

### 1. 📋 Documentation des IA
- Explication détaillée des stratégies
- Comparaison Braindead vs Daft
- Exemples d'utilisation

### 2. 🧪 Tests spécialisés
- Tests de performance des IA
- Tests de stratégies
- Tests de comportement

### 3. 📊 Exemples d'utilisation
- Scénarios de bataille
- Configurations différentes
- Analyses de résultats

### 4. 🎯 Diagrammes de flux
- Flux de décision des IA
- Arbres de stratégie
- Schémas de comportement
