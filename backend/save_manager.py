import os
import json
import pickle
from typing import Any
from pathlib import Path

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
os.makedirs(SAVE_DIR, exist_ok=True)


# --- Deprecated pickle save/load (kept for compatibility) ---
def save_battle_pickle(battle, filename="battle.save"):
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "wb") as f:
        pickle.dump(battle, f)
    print(f"[pickle] Battle saved to {filepath}")


def load_battle_pickle(filename="battle.save"):
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "rb") as f:
        battle = pickle.load(f)
    print(f"[pickle] Battle loaded from {filepath}")
    return battle


# --- JSON-based stable save/load (recommended) ---
def save_battle_json(battle, filename="battle.json"):
    """
    Save a JSON snapshot of the battle state.
    filename should end with .json (recommended).
    """
    filepath = os.path.join(SAVE_DIR, filename)
    data = battle.to_dict()
    # write atomic: write to temp then move
    tmp = Path(filepath).with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, filepath)
    print(f"[json] Battle saved to {filepath}")


def load_battle_json(filename="battle.json"):
    """
    Load JSON snapshot and reconstruct Battle object from dict.
    """
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    from backend.battle import Battle
    battle = Battle.from_dict(data)
    print(f"[json] Battle loaded from {filepath}")
    return battle