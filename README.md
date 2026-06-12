<<<<<<< HEAD
# Othello — Strategy Board Game

A polished desktop implementation of the classic Othello / Reversi board game,
built with Python and Tkinter.  Features a Minimax AI with Alpha-Beta pruning,
four carefully designed themes, and full multi-language support including Arabic RTL.

---

## Screenshots

> Main Menu · Game Board · Settings

---

## Features

| Feature | Details |
|---|---|
| **AI Engine** | Minimax with Alpha-Beta pruning (depth 4) |
| **Themes** | Modern Dark · Sage Green · Coffee · Minimal Light |
| **Languages** | English · Arabic (RTL) · Deutsch |
| **Statistics** | Per-session wins / losses / draws |
| **Timers** | Per-player move timers |
| **Sound** | Optional system beeps (Windows) |
| **Portable** | Pure Tkinter — no extra GUI framework needed |

---

## Getting Started

### Requirements

- Python 3.10+
- `arabic_reshaper`
- `python-bidi`

```bash
pip install arabic-reshaper python-bidi
```

### Run

```bash
python main.py
```

---

## Project Structure

```
othello/
├── main.py          # Entry point & App controller
├── game_logic.py    # Othello engine (board, moves, AI)
├── themes.py        # Color theme definitions
├── languages.py     # UI string localization
├── ui/
│   ├── screens.py   # MainMenu, SettingsScreen, GameScreen
│   └── widgets.py   # ModernButton, Separator, show_dialog
└── assets/          # Reserved for icons / images
```

---

## How to Play

1. Launch the game — you play as **O** (light discs), the computer plays as **X** (dark discs).
2. Click any cell highlighted by a **valid-move dot** to place your disc.
3. Discs are flipped in all directions where you sandwich the opponent's discs.
4. If you have no valid moves, use **Pass Turn**.
5. The game ends when neither player can move. Most discs wins.

---

## AI Design

The computer uses **Minimax search** with **Alpha-Beta pruning** at depth 4.

The static evaluation function considers:
- **Disc difference** — raw count of X minus O discs
- **Corner control** — corners are worth +5 / −5 because they can never be flipped

Alpha-Beta pruning typically reduces the effective branching factor from ~10 to ~4,
making depth-4 search fast enough for fluid gameplay.

---

## Architecture Notes

- **`game_logic.py`** is fully independent of Tkinter — it can be imported and tested in isolation.
- **`themes.py`** and **`languages.py`** are pure data modules — no logic, easy to extend.
- **`App`** in `main.py` acts as a dependency-injection hub; screens receive it as a parameter and never import each other.
- All Arabic strings are processed through `arabic_reshaper` + `python-bidi` at render time, keeping the data layer clean.

---

## Extending the Project

**Add a new theme** — edit `themes.py` and add an entry to the `THEMES` dict.  
**Add a language** — edit `languages.py` and add an entry to the `LANGUAGES` dict.  
**Increase AI strength** — increase the `depth` parameter in `Othello.best_move()`.  
**Custom board size** — the engine uses `range(8)` throughout; parameterise `board_size` to support variants.

---

## Contributors

- Sara M. Abdelrahman
- Sajed O. Abdelrahman
- Mariam H. Mohamed
- Mahmoud E. Mahmoud
- Habiba O. Saadeldeen

---

## License

MIT — free to use, modify, and distribute.
=======
# Othello-AI-Game
AI-powered Othello game built with Python and Tkinter, featuring Minimax, Alpha-Beta Pruning, Move Ordering, advanced heuristics, multilingual support, and save/load functionality.
>>>>>>> 1635654f0c2c589de738835a79ac3132d4d38183
