# 🎮 Schéma Visuel - Exécution du Projet MedievAIl

## 📊 Flux d'Exécution Principal (main.py)

```
┌─────────────────────────────────────────────────────────────┐
│                    🚀 LANCEMENT DU PROJET                    │
│                     py main.py                              │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              📋 INITIALISATION DES COMPOSANTS               │
└─────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 🤖 CRÉATION     │  │ ⚔️ CRÉATION     │  │ 🏰 CRÉATION     │
│   GÉNÉRAUX      │  │   MOTEUR        │  │   ARMÉES        │
│                 │  │   BATAILLE      │  │                 │
│ • Braindead     │  │                 │  │ • Armée Rouge   │
│ • Daft          │  │ • Champ 20x10   │  │ • Armée Bleue   │
│ • Stratégies    │  │ • Max 15 tours  │  │ • Unités        │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    🎯 CONFIGURATION                        │
│                 Position des armées                        │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    ⚔️ DÉBUT DE LA BATAILLE                  │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │   🔄 BOUCLE      │
                    │   PRINCIPALE    │
                    │                 │
                    │ Tour 1 → Tour N │
                    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 🛡️ BRAINDEAD    │  │ ⚔️ MAJOR DAFT   │  │ 🎮 RÉSOLUTION   │
│   DONNE ORDRES  │  │   DONNE ORDRES  │  │   DES ACTIONS   │
│                 │  │                 │  │                 │
│ • Reste en place│  │ • Avance        │  │ • Mouvements    │
│ • Attend        │  │ • Attaque       │  │ • Combats       │
│ • Défend        │  │ • Cherche ennemi│  │ • Dégâts        │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    📊 AFFICHAGE VISUEL                      │
│                 Champ de bataille                           │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │   ❓ FIN ?      │
                    │                 │
                    │ • Victoire ?   │
                    │ • Tours max ?  │
                    │ • Continuer ?  │
                    └─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
        ┌─────────────────┐      ┌─────────────────┐
        │   🏆 FIN        │      │   🔄 SUIVANT    │
        │                 │      │                 │
        │ • Résultats     │      │ • Tour suivant │
        │ • Statistiques  │      │ • Actions      │
        │ • Vainqueur     │      │ • Affichage    │
        └─────────────────┘      └─────────────────┘
```

## 🧠 Flux de Décision des IA

### 🛡️ Captain Braindead (Défensif)
```
┌─────────────────┐
│   🛡️ BRAINDEAD  │
│   ORDRE REÇU    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   📍 POSITION   │
│   ACTUELLE      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   ❓ ENNEMI     │
│   À PORTÉE ?    │
└─────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌─────────┐
│   ✅    │ │   ❌    │
│ ATTAQUE │ │ RESTE   │
│         │ │ EN      │
│         │ │ PLACE   │
└─────────┘ └─────────┘
```

### ⚔️ Major Daft (Agressif)
```
┌─────────────────┐
│   ⚔️ MAJOR DAFT │
│   ORDRE REÇU    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   🔍 CHERCHE    │
│   ENNEMI LE     │
│   PLUS PROCHE   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   📏 CALCULE    │
│   DISTANCE      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   ❓ À PORTÉE   │
│   D'ATTAQUE ?   │
└─────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌─────────┐
│   ✅    │ │   ❌    │
│ ATTAQUE │ │ AVANCE  │
│         │ │ VERS    │
│         │ │ ENNEMI  │
└─────────┘ └─────────┘
```

## 🎯 Exemple d'Exécution Visuelle

```
TOUR 1:
┌─────────────────────────────────────────┐
│ 🛡️ BRAINDEAD: "Reste en position"      │
│ ⚔️ DAFT: "Avance vers l'ennemi"         │
│                                         │
│ Champ:                                  │
│  0 1 2 3 4 5 6 7 8 9                   │
│ 0 . . . . . . . . . .                   │
│ 1 . . 🔴 . . . . . 🔵 .                 │
│ 2 . . 🔴 . . . . . 🔵 .                 │
│ 3 . . 🔴 . . . . . 🔵 .                 │
└─────────────────────────────────────────┘

TOUR 2:
┌─────────────────────────────────────────┐
│ 🛡️ BRAINDEAD: "Reste en position"      │
│ ⚔️ DAFT: "Avance vers l'ennemi"         │
│                                         │
│ Champ:                                  │
│  0 1 2 3 4 5 6 7 8 9                   │
│ 0 . . . . . . . . . .                   │
│ 1 . . 🔴 . . . . 🔵 . .                 │
│ 2 . . 🔴 . . . . 🔵 . .                 │
│ 3 . . 🔴 . . . . 🔵 . .                 │
└─────────────────────────────────────────┘

TOUR 3:
┌─────────────────────────────────────────┐
│ 🛡️ BRAINDEAD: "Reste en position"      │
│ ⚔️ DAFT: "ATTAQUE !"                    │
│                                         │
│ Champ:                                  │
│  0 1 2 3 4 5 6 7 8 9                   │
│ 0 . . . . . . . . . .                   │
│ 1 . . 🔴 . . . 🔵 . . .                 │
│ 2 . . 🔴 . . . 🔵 . . .                 │
│ 3 . . 🔴 . . . 🔵 . . .                 │
│                                         │
│ 💥 COMBAT ! Dégâts infligés             │
└─────────────────────────────────────────┘
```

## 📊 Résultats Finaux

```
┌─────────────────────────────────────────┐
│              🏆 RÉSULTATS               │
│                                         │
│ • Vainqueur: Major Daft                 │
│ • Tours écoulés: 8                      │
│ • Unités Braindead: 2 survivantes       │
│ • Unités Daft: 3 survivantes           │
│                                         │
│ 📈 Analyse:                             │
│ • Daft a pris l'initiative             │
│ • Braindead a résisté défensivement    │
│ • Stratégie agressive payante          │
└─────────────────────────────────────────┘
```
