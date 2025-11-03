# 🤖 Documentation des IA - MedievAIl Battle Simulator

## 🎯 Votre Contribution : Les Généraux IA

Vous avez développé la partie **Intelligence Artificielle** du projet MedievAIl Battle Simulator, spécifiquement les deux généraux :

### 🛡️ Captain Braindead (IA Défensive)
- **Stratégie** : Défensive pure
- **Comportement** : Ne bouge jamais de sa position
- **Tactique** : Attend l'attaque de l'ennemi
- **Code** : `General.py` lignes 35-50

### ⚔️ Major Daft (IA Agressive)  
- **Stratégie** : Agressive
- **Comportement** : Avance vers l'ennemi
- **Tactique** : Attaque dès que possible
- **Code** : `General.py` lignes 52-120

## 📁 Fichiers de Votre Contribution

```
medieval_battle_simulator/
├── 🧠 General.py                    ← VOS IA (Braindead & Daft)
├── 🧪 test_generals.py             ← Tests de vos IA
├── 🧪 test_generals_simple.py       ← Tests simplifiés
├── 🧪 test_visuel_simple.py         ← Tests visuels
├── 📚 GUIDE_EXECUTION.md            ← Guide d'exécution
├── 📚 SCHEMA_EXECUTION.md           ← Schéma d'exécution
└── 📚 ARCHITECTURE_VISUELLE.md     ← Architecture du projet
```

## 🔍 Code de Vos IA

### Captain Braindead (Défensif)
```python
class CaptainBraindead(General):
    def issue_orders(self, enemy_army: Army, battlefield_width: int, battlefield_height: int) -> List[str]:
        orders = []
        for unit in self.army.get_alive_units():
            # Stratégie défensive : ne bouge jamais
            orders.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) stays in defensive position")
        return orders
```

### Major Daft (Agressif)
```python
class MajorDaft(General):
    def issue_orders(self, enemy_army: Army, battlefield_width: int, battlefield_height: int) -> List[str]:
        orders = []
        for unit in self.army.get_alive_units():
            closest_enemy = self._find_closest_enemy(unit, enemy_army)
            if closest_enemy:
                distance = abs(unit.x - closest_enemy.x) + abs(unit.y - closest_enemy.y)
                if distance <= 1:  # À portée d'attaque
                    orders.append(f"{unit.unit_type.value} at ({unit.x}, {unit.y}) attacks enemy at ({closest_enemy.x}, {closest_enemy.y})")
                else:  # Avancer vers l'ennemi
                    new_x, new_y = self._move_towards_target(unit, closest_enemy)
                    orders.append(f"{unit.unit_type.value} moves from ({unit.x}, {unit.y}) to ({new_x}, {new_y})")
        return orders
```

## 🧪 Tests de Vos IA

### Test Simple
```bash
py test_generals_simple.py
```

### Test Visuel
```bash
py test_visuel_simple.py
```

### Test Complet
```bash
py test_system.py
```

## 📊 Résultats Typiques

### Braindead vs Daft
- **Major Daft** gagne généralement (stratégie agressive)
- **Captain Braindead** résiste défensivement
- **Combats** : Daft attaque dès qu'il arrive à portée
- **Mouvements** : Seul Daft bouge, Braindead reste immobile

## 🎯 Points Forts de Votre Implémentation

1. **Différenciation claire** des stratégies
2. **Code bien commenté** et structuré
3. **Tests complets** pour valider le comportement
4. **Documentation détaillée** des algorithmes
5. **Interface propre** avec la classe General abstraite

## 🚀 Comment Utiliser Vos IA

```python
# Création des généraux
braindead = CaptainBraindead()
daft = MajorDaft()

# Assignation des armées
braindead.set_army(army1)
daft.set_army(army2)

# Lancement de la bataille
engine = BattleEngine(width=20, height=10, max_turns=15)
result = engine.simulate_battle(army1, army2, braindead, daft)
```

## 📈 Améliorations Possibles

1. **Stratégies hybrides** (défensif-agressif)
2. **IA plus intelligente** (analyse de terrain)
3. **Stratégies adaptatives** (changement selon la situation)
4. **IA d'équipe** (coordination entre unités)

## 🏆 Votre Contribution au Projet

Vous avez créé la **partie la plus importante** du simulateur :
- **L'intelligence** qui anime les armées
- **Les stratégies** qui rendent les batailles intéressantes
- **Les algorithmes** de prise de décision
- **Les tests** qui valident le comportement

Sans vos IA, le projet ne serait qu'un moteur de bataille vide !
