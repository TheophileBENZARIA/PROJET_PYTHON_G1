# 🎮 Guide d'Exécution - MedievAIl Battle Simulator

## 🚀 Comment lancer le projet

### 1. **Commande principale :**
```bash
py main.py
```

### 2. **Ce qui se passe étape par étape :**

```
┌─────────────────────────────────────────────────────────────┐
│                    🎬 SÉQUENCE D'EXÉCUTION                 │
└─────────────────────────────────────────────────────────────┘

1️⃣ INITIALISATION
   ├── Création de Captain Braindead (IA défensive)
   ├── Création de Major Daft (IA agressive)
   ├── Création des armées (Rouge vs Bleue)
   └── Configuration du champ de bataille (20x10)

2️⃣ POSITIONNEMENT
   ├── Armée Rouge (Braindead) → Position défensive (gauche)
   ├── Armée Bleue (Daft) → Position offensive (droite)
   └── Affichage de la position initiale

3️⃣ BOUCLE DE BATAILLE (Tours 1 à 15)
   ├── Tour N:
   │   ├── 🛡️ Braindead donne ses ordres (reste en place)
   │   ├── ⚔️ Daft donne ses ordres (avance/attaque)
   │   ├── 🎮 Résolution des actions
   │   └── 📊 Affichage du champ de bataille
   └── Vérification des conditions de fin

4️⃣ RÉSULTATS FINAUX
   ├── Détermination du vainqueur
   ├── Statistiques de la bataille
   └── Analyse des stratégies
```

## 🎯 Exemple de Sortie Console

```
MedievAIl Battle Simulator

Configuration de la bataille :
- Champ: 20x10
- Tours maximum: 15
- Généraux: Captain Braindead vs Major Daft

Debut de la bataille !

=== DÉBUT DE LA BATAILLE ===
Armée 1: Armée Rouge dirigée par Captain Braindead
Armée 2: Armée Bleue dirigée par Major Daft
Champ de bataille: 20x10
Unités armée 1: 12
Unités armée 2: 12
==================================================

--- TOUR 1 ---

Captain Braindead donne ses ordres:
  knight at (2, 3) stays in defensive position
  archer at (3, 3) stays in defensive position
  ...

Major Daft donne ses ordres:
  knight moves from (15, 3) to (13, 3)
  archer moves from (16, 3) to (15, 3)
  ...

Champ de bataille:
    0 1 2 3 4 5 6 7 8 910111213141516171819
 0 . . . . . . . . . . . . . . . . . . . . 
 1 . . . . . . . . . . . . . . . . . . . . 
 2 . . . . . . . . . . . . . . . . . . . . 
 3 . . 🔴 🔴 🔴 . . . . . . . . 🔵 🔵 🔵 . . . 
 4 . . 🔴 🔴 🔴 . . . . . . . . 🔵 🔵 🔵 . . . 
 5 . . 🔴 🔴 🔴 . . . . . . . . 🔵 🔵 🔵 . . . 
 6 . . 🔴 🔴 🔴 . . . . . . . . 🔵 🔵 🔵 . . . 
 7 . . . . . . . . . . . . . . . . . . . . 
 8 . . . . . . . . . . . . . . . . . . . . 
 9 . . . . . . . . . . . . . . . . . . . . 
Unités restantes - Armée Rouge: 12, Armée Bleue: 12

--- TOUR 2 ---
[Continuez jusqu'à la fin...]

=== FIN DE LA BATAILLE ===
Vainqueur: Armée Bleue (Major Daft)
Tours écoulés: 8
Pertes - Armée Rouge: 5, Armée Bleue: 2

RESULTAT FINAL
Major Daft est plus efficace !
```

## 🧪 Tests Disponibles

### **Test des généraux uniquement :**
```bash
py test_generals_simple.py
```

### **Test visuel complet :**
```bash
py test_visuel_simple.py
```

### **Test du système complet :**
```bash
py test_system.py
```

### **Exemples d'utilisation :**
```bash
py examples.py
```

## 📊 Ce que vous verrez visuellement

1. **🔴 Unités Rouges** (Braindead) : Restent immobiles
2. **🔵 Unités Bleues** (Daft) : Avancent vers la gauche
3. **⚔️ Combats** : Quand Daft arrive à portée
4. **💥 Dégâts** : Affichage des dégâts infligés
5. **🏆 Résultat** : Vainqueur et statistiques

## 🎯 Points Clés à Observer

- **Braindead** ne bouge JAMAIS de sa position
- **Daft** avance constamment vers l'ennemi
- **Les combats** commencent quand Daft arrive à portée
- **Les dégâts** varient selon le type d'unité
- **Le vainqueur** est déterminé par les unités survivantes
