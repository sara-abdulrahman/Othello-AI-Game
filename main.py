"""
main.py — Application entry point for Othello.

Initialises the Tkinter root window, wires up the App controller,
and starts the main event loop.

Run with:
    python main.py
"""

import threading
import tkinter as tk

from themes    import THEMES, DEFAULT_THEME
from languages import LANGUAGES, DEFAULT_LANGUAGE
from ui.screens import MainMenu, SettingsScreen, GameScreen

try:
    import winsound
    _HAS_WINSOUND = True
except ImportError:
    _HAS_WINSOUND = False


# ═══════════════════════════════════════════════════════════════════════════════
#  Application Controller
# ═══════════════════════════════════════════════════════════════════════════════

class App:
    """
    Central application controller.

    Owns all persistent state (settings, session statistics) and provides
    helper methods used by every screen.  Screen transitions are handled here
    so individual screens never import each other.
    """

    # Window geometry for each screen
    _GEOMETRY = {
        "menu":     "500x620",
        "settings": "500x820",
        "game":     "560x760",
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Othello")
        self.root.resizable(False, False)

        # Persistent user preferences
        self.settings: dict = {
            "theme":    DEFAULT_THEME,
            "language": DEFAULT_LANGUAGE,
            "muted":    False,
            "difficulty": "medium",  # "easy" | "medium" | "hard"
        }

        # Session-wide statistics (reset only on app restart)
        self.stats: dict = {
            "wins":   0,
            "losses": 0,
            "draws":  0,
        }

        self._active_frame: tk.Frame | None = None

        self.show_menu()

    # ── Convenience accessors ────────────────────────────────────────────────

    def colors(self) -> dict:
        """Return the active theme color dictionary."""
        return THEMES[self.settings["theme"]]

    def strings(self) -> dict:
        """Return the active language string dictionary."""
        return LANGUAGES[self.settings["language"]]

    def is_arabic(self) -> bool:
        return self.settings["language"] == "العربية"

    # ── Screen transitions ───────────────────────────────────────────────────

    def _switch_screen(self, screen_class, geometry_key: str):
        """Destroy the current screen frame and replace it with a new one."""
        if self._active_frame is not None:
            self._active_frame.destroy()
        self.root.geometry(self._GEOMETRY[geometry_key])
        self._active_frame = screen_class(self.root, self)
        self._active_frame.pack(fill="both", expand=True)

    def show_menu(self):
        self._switch_screen(MainMenu, "menu")

    def show_settings(self):
        self._switch_screen(SettingsScreen, "settings")

    def show_game(self):
        self._switch_screen(GameScreen, "game")

    # ── Sound ────────────────────────────────────────────────────────────────

    def play_sound(self, kind: str):
        """
        Play a brief system beep if sound is enabled and winsound is available.

        kind — one of: "place" | "win" | "lose"
        """
        if self.settings["muted"] or not _HAS_WINSOUND:
            return

        sound_map = {
            "place": (800,  80),
            "win":   (1000, 300),
            "lose":  (300,  300),
        }
        frequency, duration = sound_map.get(kind, (700, 100))
        threading.Thread(
            target=lambda: winsound.Beep(frequency, duration),
            daemon=True,
        ).start()


# ═══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
