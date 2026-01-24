# Python Project 2025–2026: MedievAIl BAIttle GenerAIl


<details>
<summary>📑 Contents</summary>

- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Installation](#installation)

</details>

## Built With

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-00A300?style=for-the-badge)




### In-game Controls

#### Pygame (`PyScreen.py`)

- **Arrow keys**: pan camera (speed scales with zoom)
- **1 / 2**: zoom in / zoom out
- **C**: reset camera to center
- **Space**: pause / resume simulation (big overlay in middle)
- **Esc**: close the window (or exit load menu)
- **M**: toggle minimap
- **F1**: toggle stats panel  
- **F2 / F3**: show / hide Army 1 / Army 2 details  
- **F4**: toggle per-unit-type counts
- **Tab**: open quick-load menu (if implemented)
- **Mouse wheel / HZ**: not configured
- Army units show colored outlines; smooth motion handled automatically

---

#### Curses terminal view (`Screen.py`)

- **Arrow keys** or **H / J / K / L**: scroll viewport  
  (use uppercase **HJKL** or **Shift + arrows** to move faster)
- **Z / S / Q / D**: alternative ZQSD movement (uppercase for faster)
- **P**: pause / resume battle ticks
- **Tab**: pause and generate an **HTML snapshot**  
  (`battle_snapshot_*.html`) which opens in your browser
- **Esc**: exit the battle view
- **Save / Load menu** (if visible):
  - **S**: quick-save
  - **L**: open load menu
