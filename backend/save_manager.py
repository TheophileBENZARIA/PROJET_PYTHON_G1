# backend/save_manager.py
import os
import pickle

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")

os.makedirs(SAVE_DIR, exist_ok=True)

def save_battle(battle, filename="battle.save"):
    """Save the full battle state into the saves/ folder"""
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "wb") as f:
        pickle.dump(battle, f)
    print(f"Battle saved to {filepath}")

def load_battle(filename="battle.save"):
    """Load a saved battle from the saves/ folder"""
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "rb") as f:
        battle = pickle.load(f)
    print(f"Battle loaded from {filepath}")
    return battle
