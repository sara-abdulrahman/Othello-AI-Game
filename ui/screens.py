"""
ui/screens.py — Application screens for Othello.

Screens:
    MainMenu       — title screen with Start / Settings / Exit
    SettingsScreen — theme, sound, and language configuration
    GameScreen     — interactive game board with HUD and statistics
"""

import copy
import time
import threading
import tkinter as tk

from game_logic import Othello
from ui.widgets import ModernButton, Separator, show_dialog, localize, render_arabic


def _make_label(parent, text: str, is_ar: bool, **kwargs) -> tk.Label:
    """
    Create a tk.Label with correct Arabic alignment and shaping applied.
    For Arabic: anchor=e, justify=right, text shaped via render_arabic.
    Pass any extra tk.Label kwargs (font, bg, fg, etc.)
    """
    display_text = render_arabic(text) if is_ar else text
    if is_ar:
        kwargs.setdefault("anchor", "e")
        kwargs.setdefault("justify", "right")
    return tk.Label(parent, text=display_text, **kwargs)


# ── Shared font definitions ───────────────────────────────────────────────────

FONT_TITLE   = ("Segoe UI", 46, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_BODY    = ("Segoe UI", 11)
FONT_LABEL   = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI",  9)


# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 1 — Main Menu
# ═══════════════════════════════════════════════════════════════════════════════

class MainMenu(tk.Frame):
    """
    Title screen shown on launch and after returning from a game.
    Displays the game title, decorative disc row, and three navigation buttons.
    """

    def __init__(self, master, app):
        colors  = app.colors()
        strings = app.strings()
        super().__init__(master, bg=colors["bg_window"], width=500, height=620)
        self.pack_propagate(False)

        is_arabic = app.is_arabic()

        # ── Subtle dot-grid background ──
        bg_canvas = tk.Canvas(
            self, width=500, height=620,
            bg=colors["bg_window"], highlightthickness=0,
        )
        bg_canvas.place(x=0, y=0)
        dot_spacing = 28
        for col_x in range(dot_spacing, 500, dot_spacing):
            for row_y in range(dot_spacing, 620, dot_spacing):
                bg_canvas.create_oval(
                    col_x - 1, row_y - 1, col_x + 1, row_y + 1,
                    fill=colors["grid"], outline="",
                )

        # ── Title ──
        tk.Label(
            self,
            text=render_arabic(strings["title"]) if is_arabic else strings["title"],
            font=FONT_TITLE,
            bg=colors["bg_window"],
            fg=colors["accent"],
            anchor="center",
            justify="center",
        ).pack(pady=(68, 2))

        tk.Label(
            self,
            text=render_arabic(strings["subtitle"]) if is_arabic else strings["subtitle"],
            font=("Segoe UI", 9),
            bg=colors["bg_window"],
            fg=colors["label_fg"],
        ).pack(pady=(0, 36))

        # ── Decorative disc row ──
        disc_canvas = tk.Canvas(
            self, width=136, height=38,
            bg=colors["bg_window"], highlightthickness=0,
        )
        disc_canvas.pack(pady=(0, 40))
        disc_colors = [
            colors["disc_dark"], colors["disc_light"],
            colors["disc_dark"], colors["disc_light"],
        ]
        for index, disc_color in enumerate(disc_colors):
            x_offset = 8 + index * 32
            disc_canvas.create_oval(
                x_offset, 5, x_offset + 26, 31,
                fill=disc_color,
                outline=colors["accent"],
                width=1,
            )

        # ── Navigation buttons ──
        # For Arabic, we reshape only the Arabic text and keep icons stable
        def make_btn_label(raw: str) -> str:
            if not is_arabic:
                return raw
            # Format: "ICON   arabic text" — split on triple space
            parts = raw.split("   ", 1)
            if len(parts) == 2:
                icon, arabic_text = parts[0].strip(), parts[1].strip()
                from ui.widgets import render_arabic
                return render_arabic(arabic_text) + "   " + icon
            return render_arabic(raw)

        button_definitions = [
            (make_btn_label(strings["start"]),    app.show_game,     "accent"),
            (make_btn_label(strings["settings"]), app.show_settings, "default"),
            (make_btn_label(strings["exit"]),     master.quit,       "ghost"),
        ]
        for label, command, variant in button_definitions:
            ModernButton(
                self,
                text=label,
                command=command,
                colors=colors,
                variant=variant,
                font_size=13,
            ).pack(pady=6)


# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 2 — Settings
# ═══════════════════════════════════════════════════════════════════════════════

class SettingsScreen(tk.Frame):
    """
    Settings screen for theme, sound toggle, and language selection.
    Theme swatches are displayed as small color-preview buttons.
    """

    def __init__(self, master, app):
        colors  = app.colors()
        strings = app.strings()
        super().__init__(master, bg=colors["bg_window"], width=500, height=700)
        
        self.app = app
        self.pack_propagate(False)

        is_arabic = app.is_arabic()

        # ── Header ──
        tk.Label(
            self,
            text=render_arabic(strings["settings_title"]) if is_arabic else strings["settings_title"],
            font=("Segoe UI", 28, "bold"),
            bg=colors["bg_window"],
            fg=colors["accent"],
            anchor="e" if is_arabic else "center",
            justify="right" if is_arabic else "center",
        ).pack(pady=(28, 6))

        Separator(self, colors).pack(fill="x", padx=30, pady=(0, 8))

        # ── Theme section ──
        self._section_label(render_arabic(strings["theme_label"]) if is_arabic else strings["theme_label"], colors, is_arabic)
        self._build_theme_swatches(colors, is_arabic)

        Separator(self, colors).pack(fill="x", padx=30, pady=(14, 8))

        # ── Sound section ──
        self._section_label(render_arabic(strings["sound_label"]) if is_arabic else strings["sound_label"], colors, is_arabic)
        self._build_sound_toggle(colors, strings, is_arabic)

        Separator(self, colors).pack(fill="x", padx=30, pady=(14, 8))

        # ── Language section ──
        self._section_label(render_arabic(strings["language_label"]) if is_arabic else strings["language_label"], colors, is_arabic)
        self._build_language_selector(colors, is_arabic)

        Separator(self, colors).pack(fill="x", padx=30, pady=(14, 8))

        # ── Difficulty section ──
        self._section_label(render_arabic(strings["difficulty_label"]) if is_arabic else strings["difficulty_label"], colors, is_arabic)
        self._build_difficulty_selector(colors, strings, is_arabic)

        Separator(self, colors).pack(fill="x", padx=30, pady=(14, 8))

        # ── About / contributors ──
        self._section_label(render_arabic(strings["about_label"]) if is_arabic else strings["about_label"], colors, is_arabic)
        self._build_contributors(colors, is_arabic)

        # ── Back button ──
        ModernButton(
            self,
            text=localize(strings["back"], is_arabic),
            command=app.show_menu,
            colors=colors,
            font_size=12,
            width=22,
        ).pack(pady=18)

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _section_label(self, text: str, colors: dict, is_arabic: bool = False):
        tk.Label(
            self, text=text,
            font=("Segoe UI", 11, "bold"),
            bg=colors["bg_window"],
            fg=colors["label_fg"],
            anchor="e" if is_arabic else "center",
            justify="right" if is_arabic else "center",
        ).pack(pady=(4, 8), fill="x", padx=30)

    def _build_theme_swatches(self, colors: dict, is_arabic: bool):
        """
        Render each theme as a small labelled color swatch button.
        Four themes fit neatly in a single row.
        """
        from themes import THEMES

        swatch_row = tk.Frame(self, bg=colors["bg_window"])
        swatch_row.pack(pady=(0, 4))

        for theme_name, theme_colors in THEMES.items():
            is_selected = theme_name == self.app.settings["theme"]

            cell = tk.Frame(
                swatch_row,
                bg=colors["bg_window"],
                padx=6, pady=4,
            )
            cell.pack(side=tk.LEFT)

            # Color preview swatch
            preview = tk.Canvas(
                cell, width=54, height=38,
                bg=theme_colors["bg_board"],
                highlightthickness=2,
                highlightbackground=(
                    theme_colors["accent"] if is_selected
                    else colors["separator"]
                ),
                cursor="hand2",
            )
            preview.pack()

            # Mini discs inside the swatch
            preview.create_oval( 4,  8, 22, 26, fill=theme_colors["disc_dark"],  outline="")
            preview.create_oval(28,  8, 46, 26, fill=theme_colors["disc_light"], outline="")

            # Theme label below swatch
            tk.Label(
                cell,
                text=theme_name,
                font=FONT_SMALL,
                bg=colors["bg_window"],
                fg=theme_colors["accent"] if is_selected else colors["label_fg"],
            ).pack(pady=(3, 0))

            # Click to apply
            preview.bind(
                "<Button-1>",
                lambda _e, name=theme_name: self._apply_setting("theme", name),
            )

    def _build_sound_toggle(self, colors: dict, strings: dict, is_arabic: bool):
        is_muted = self.app.settings["muted"]
        label    = strings["sound_off"] if is_muted else strings["sound_on"]

        ModernButton(
            self,
            text=localize(label, is_arabic),
            command=self._toggle_sound,
            colors=colors,
            variant="accent" if not is_muted else "default",
            font_size=11,
            width=18,
        ).pack(pady=(0, 4))

    def _build_language_selector(self, colors: dict, is_arabic: bool):
        from languages import LANGUAGES

        lang_row = tk.Frame(self, bg=colors["bg_window"])
        lang_row.pack(pady=(0, 4))

        for language_name in LANGUAGES:
            is_selected = language_name == self.app.settings["language"]
            btn = tk.Button(
                lang_row,
                text=language_name,
                font=("Segoe UI", 11, "bold"),
                bg=colors["accent"]  if is_selected else colors["btn_bg"],
                fg=colors["bg_window"] if is_selected else colors["btn_fg"],
                activebackground=colors["btn_hover"],
                relief="flat",
                padx=14,
                pady=7,
                cursor="hand2",
                command=lambda lg=language_name: self._apply_setting("language", lg),
            )
            btn.pack(side=tk.LEFT, padx=5)

    def _build_difficulty_selector(self, colors: dict, strings: dict, is_arabic: bool):
        """
        Three pill-style buttons: Easy / Medium / Hard.
        The active difficulty is highlighted with the accent color.
        Each button also shows the AI search depth for transparency.
        """
        LEVELS = [
            ("easy",   strings["diff_easy"],   "2"),
            ("medium", strings["diff_medium"],  "4"),
            ("hard",   strings["diff_hard"],    "6"),
        ]

        row = tk.Frame(self, bg=colors["bg_window"])
        row.pack(pady=(0, 4))

        current = self.app.settings["difficulty"]

        for key, label_text, depth_label in LEVELS:
            is_selected = key == current
            cell = tk.Frame(row, bg=colors["bg_window"])
            cell.pack(side=tk.LEFT, padx=6)

            btn = tk.Button(
                cell,
                text=localize(label_text, is_arabic),
                font=("Segoe UI", 11, "bold"),
                bg=colors["accent"]   if is_selected else colors["btn_bg"],
                fg=colors["bg_window"] if is_selected else colors["btn_fg"],
                activebackground=colors["btn_hover"],
                relief="flat",
                padx=18, pady=8,
                cursor="hand2",
                command=lambda k=key: self._apply_setting("difficulty", k),
            )
            btn.pack()

            # Depth hint below each button
            tk.Label(
                cell,
                text=f"depth {depth_label}",
                font=("Segoe UI", 8),
                bg=colors["bg_window"],
                fg=colors["accent"] if is_selected else colors["label_fg"],
            ).pack(pady=(2, 0))

    def _build_contributors(self, colors: dict, is_arabic: bool):
        """Display the contributor list neatly."""
        contributors = [
            ("Sara Muhammad",   "ساره محمد "),
            ("Sajed Osama",  "ساجد أسامه "),
            ("Mariam Hassan",     "مريم حسن "),
            ("Mahmoud Essam",    "محمود عصام "),
            ("Habiba Osama", "حبيبة أسامة  "),
        ]
        container = tk.Frame(self, bg=colors["bg_window"])
        container.pack(pady=(0, 4))

        for i, (english_name, arabic_name) in enumerate(contributors):
         display_name = arabic_name if is_arabic else english_name
         row, col = divmod(i, 2)
         tk.Label(
             container,
             text=localize(display_name, is_arabic),
             font=FONT_SMALL,
             bg=colors["bg_window"],
             fg=colors["label_fg"],
             padx=8,
             ).grid(row=row, column=col, sticky="w")

    def _apply_setting(self, key: str, value):
        self.app.settings[key] = value
        self.app.show_settings()

    def _toggle_sound(self):
        self.app.settings["muted"] = not self.app.settings["muted"]
        self.app.show_settings()


# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 3 — Game
# ═══════════════════════════════════════════════════════════════════════════════

class GameScreen(tk.Frame):
    """
    Main gameplay screen containing the board canvas, HUD, action buttons,
    and a statistics panel.
    """

    CANVAS_SIZE = 512   # Must be divisible by 8
    CELL_SIZE   = CANVAS_SIZE // 8    # 64 px per cell
    DISC_INSET  = 6     # Pixels from cell edge to disc boundary
    INDICATOR_RADIUS = 5  # Radius of valid-move dot

    def __init__(self, master, app):
        colors = app.colors()
        super().__init__(master, bg=colors["bg_window"])
        self.app = app

        # Game state
        self.engine       = Othello()
        self.board        = copy.deepcopy(self.engine.board)
        self.human_time   = 0.0
        self.cpu_time     = 0.0
        self._timer_on    = False
        self._active_timer = "human"   # "human" | "cpu"
        self._last_tick   = time.time()

        self._build_ui()
        self._refresh_board()
        self._start_timer("human")

    # ── UI Construction ───────────────────────────────────────────────────────

    @staticmethod
    def _ar_safe(text: str, is_ar: bool) -> str:
        """
        Render a string that may start with a non-Arabic symbol (e.g. ⏱).
        For Arabic: reshape only the Arabic part, keep the symbol at the end.
        """
        if not is_ar:
            return text
        from ui.widgets import render_arabic
        # Split on first space after leading non-letter chars
        parts = text.split(" ", 1)
        if len(parts) == 2 and not parts[0][-1].isalpha():
            icon, arabic_part = parts[0], parts[1]
            return render_arabic(arabic_part) + " " + icon
        return render_arabic(text)

    def _build_ui(self):
        colors  = self.app.colors()
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()

        # ── Top HUD ──
        top_bar = tk.Frame(self, bg=colors["bg_window"])
        top_bar.pack(fill="x", padx=14, pady=(10, 4))

        from ui.widgets import render_arabic
        if is_ar:
            menu_btn_text = render_arabic(strings["menu"])   # plain "القائمة" — no arrow
        else:
            menu_btn_text = strings["menu"]                  # "← Menu"
        menu_button = tk.Button(
            top_bar,
            text=menu_btn_text,
            font=("Segoe UI", 10, "bold"),
            bg=colors["btn_bg"], fg=colors["btn_fg"],
            activebackground=colors["btn_hover"],
            relief="flat", padx=10, pady=5,
            cursor="hand2",
            command=self._go_to_menu,
        )
        self.score_label = tk.Label(
            top_bar,
            text=strings["score"].format(x=2, o=2),
            font=("Segoe UI", 13, "bold"),
            bg=colors["bg_window"],
            fg=colors["label_fg"],
        )
        self.turn_label = tk.Label(
            top_bar,
            text=render_arabic(strings["your_turn"]) if is_ar else strings["your_turn"],
            font=("Segoe UI", 12, "bold"),
            bg=colors["bg_window"],
            fg=colors["accent"],
        )

        if is_ar:
            self.turn_label.pack(side=tk.LEFT)
            self.score_label.pack(side=tk.LEFT, expand=True)
            menu_button.pack(side=tk.RIGHT)
        else:
            menu_button.pack(side=tk.LEFT)
            self.score_label.pack(side=tk.LEFT, expand=True)
            self.turn_label.pack(side=tk.RIGHT)

        # ── Timer bar ──
        timer_bar = tk.Frame(self, bg=colors["bg_window"])
        timer_bar.pack(fill="x", padx=14, pady=(0, 4))

        timer_kwargs = dict(
            font=FONT_LABEL,
            bg=colors["bg_window"],
            fg=colors["label_fg"],
        )
        self.you_timer_label = tk.Label(
            timer_bar,
            text=GameScreen._ar_safe(strings["timer_you"].format(t=0), is_ar),
            **timer_kwargs,
        )
        self.cpu_timer_label = tk.Label(
            timer_bar,
            text=GameScreen._ar_safe(strings["timer_cpu"].format(t=0), is_ar),
            **timer_kwargs,
        )
        if is_ar:
            self.cpu_timer_label.pack(side=tk.LEFT)
            self.you_timer_label.pack(side=tk.RIGHT)
        else:
            self.you_timer_label.pack(side=tk.LEFT)
            self.cpu_timer_label.pack(side=tk.RIGHT)

        # ── Board canvas ──
        self.canvas = tk.Canvas(
            self,
            width=self.CANVAS_SIZE,
            height=self.CANVAS_SIZE,
            bg=colors["bg_board"],
            highlightthickness=2,
            highlightbackground=colors["grid"],
        )
        self.canvas.pack(padx=14, pady=4)
        self._draw_grid()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # ── Action buttons ──
        btn_row = tk.Frame(self, bg=colors["bg_window"])
        btn_row.pack(pady=6)

        def make_game_btn_label(raw: str) -> str:
            if not is_ar:
                return raw
            parts = raw.split("  ", 1)
            if len(parts) == 2:
                icon, arabic_text = parts[0].strip(), parts[1].strip()
                from ui.widgets import render_arabic
                return render_arabic(arabic_text) + "  " + icon
            from ui.widgets import render_arabic
            return render_arabic(raw)

        button_pairs = [
            (make_game_btn_label(strings["new_game"]),  self._start_new_game),
            (make_game_btn_label(strings["pass_turn"]), self._pass_turn),
        ]
        if is_ar:
            button_pairs.reverse()

        for label, command in button_pairs:
            tk.Button(
                btn_row,
                text=label,
                font=("Segoe UI", 11, "bold"),
                bg=colors["btn_bg"], fg=colors["btn_fg"],
                activebackground=colors["btn_hover"],
                relief="flat", padx=14, pady=6,
                cursor="hand2",
                command=command,
            ).pack(side=tk.LEFT, padx=6)

        # ── Statistics panel ──
        stats_panel = tk.Frame(self, bg=colors["bg_panel"], pady=8)
        stats_panel.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(
            stats_panel,
            text=localize(self.app.strings()["stats_title"], is_ar),
            font=("Segoe UI", 10, "bold"),
            bg=colors["bg_panel"],
            fg=colors["label_fg"],
        ).pack(pady=(0, 4))

        Separator(stats_panel, colors).pack(fill="x", padx=20, pady=(0, 6))

        stat_row = tk.Frame(stats_panel, bg=colors["bg_panel"])
        stat_row.pack()

        stat_font = ("Segoe UI", 10, "bold")
        stats = self.app.stats

        self.wins_label  = tk.Label(
            stat_row,
            text=localize(self.app.strings()["wins"].format(n=stats["wins"]), is_ar),
            font=stat_font,
            bg=colors["bg_panel"],
            fg="#7DBE8E",   # muted sage green
            padx=14,
        )
        self.losses_label = tk.Label(
            stat_row,
            text=localize(self.app.strings()["losses"].format(n=stats["losses"]), is_ar),
            font=stat_font,
            bg=colors["bg_panel"],
            fg="#C87878",   # muted rose
            padx=14,
        )
        self.draws_label = tk.Label(
            stat_row,
            text=localize(self.app.strings()["draws"].format(n=stats["draws"]), is_ar),
            font=stat_font,
            bg=colors["bg_panel"],
            fg="#A89060",   # muted gold
            padx=14,
        )

        ordered = (
            [self.draws_label, self.losses_label, self.wins_label]
            if is_ar else
            [self.wins_label, self.losses_label, self.draws_label]
        )
        for index, label_widget in enumerate(ordered):
            label_widget.grid(row=0, column=index)

        # ── AI Stats Panel ────────────────────────────────────────────────────
        ai_panel = tk.Frame(self, bg=colors["bg_panel"], pady=6)
        ai_panel.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(
            ai_panel,
            text=localize("🤖 AI", is_ar),
            font=("Segoe UI", 10, "bold"),
            bg=colors["bg_panel"],
            fg=colors["label_fg"],
        ).pack(pady=(0, 3))

        Separator(ai_panel, colors).pack(fill="x", padx=20, pady=(0, 5))

        ai_row = tk.Frame(ai_panel, bg=colors["bg_panel"])
        ai_row.pack()

        ai_stat_font = ("Segoe UI", 9)
        ai_muted = colors.get("label_fg", "#888888")

        self.ai_nodes_label = tk.Label(
            ai_row, text="Nodes: —", font=ai_stat_font,
            bg=colors["bg_panel"], fg=ai_muted, padx=10,
        )
        self.ai_depth_label = tk.Label(
            ai_row, text="Depth: —", font=ai_stat_font,
            bg=colors["bg_panel"], fg=ai_muted, padx=10,
        )
        self.ai_score_label = tk.Label(
            ai_row, text="Score: —", font=ai_stat_font,
            bg=colors["bg_panel"], fg=ai_muted, padx=10,
        )

        ai_labels = [self.ai_nodes_label, self.ai_depth_label, self.ai_score_label]
        if is_ar:
            ai_labels.reverse()
        for idx, lbl in enumerate(ai_labels):
            lbl.grid(row=0, column=idx)

    # ── Board drawing ─────────────────────────────────────────────────────────

    def _draw_grid(self):
        colors = self.app.colors()
        for i in range(9):
            position = i * self.CELL_SIZE
            # Vertical lines
            self.canvas.create_line(
                position, 0, position, self.CANVAS_SIZE,
                width=1, fill=colors["grid"],
            )
            # Horizontal lines
            self.canvas.create_line(
                0, position, self.CANVAS_SIZE, position,
                width=1, fill=colors["grid"],
            )

    def _draw_disc(self, row: int, col: int, fill: str, outline: str):
        inset = self.DISC_INSET
        x1 = col * self.CELL_SIZE + inset
        y1 = row * self.CELL_SIZE + inset
        x2 = (col + 1) * self.CELL_SIZE - inset
        y2 = (row + 1) * self.CELL_SIZE - inset
        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=fill, outline=outline, width=1,
            tags="disc",
        )

    def _draw_valid_indicator(self, row: int, col: int):
        """Draw a small dot at the centre of a valid-move cell."""
        cx = col * self.CELL_SIZE + self.CELL_SIZE // 2
        cy = row * self.CELL_SIZE + self.CELL_SIZE // 2
        r  = self.INDICATOR_RADIUS
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=self.app.colors()["valid_move"],
            outline="",
            tags="indicator",
        )

    def _refresh_board(self):
        """Redraw all discs and valid-move indicators from current board state."""
        colors  = self.app.colors()
        strings = self.app.strings()

        self.canvas.delete("disc", "indicator")

        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                if cell == "X":
                    self._draw_disc(row, col, colors["disc_dark"],  colors["outline_dark"])
                elif cell == "O":
                    self._draw_disc(row, col, colors["disc_light"], colors["outline_light"])

        x_count, o_count = self.engine.count(self.board)
        self.score_label.config(text=strings["score"].format(x=x_count, o=o_count))

        # Show valid-move dots only on the human's turn
        if self._is_human_turn():
            for row, col in self.engine.valid_moves(self.board, "O"):
                self._draw_valid_indicator(row, col)

        if self.engine.terminal(self.board):
            self.master.after(300, self._handle_game_over)

    # ── Timer ─────────────────────────────────────────────────────────────────

    def _start_timer(self, whose: str):
        self._timer_on     = True
        self._active_timer = whose
        self._last_tick    = time.time()
        self._tick()

    def _stop_timer(self):
        self._timer_on = False

    def _tick(self):
        if not self._timer_on:
            return
        now   = time.time()
        delta = now - self._last_tick
        self._last_tick = now

        if self._active_timer == "human":
            self.human_time += delta
        else:
            self.cpu_time += delta

        strings = self.app.strings()
        is_ar   = self.app.is_arabic()
        self.you_timer_label.config(
            text=GameScreen._ar_safe(strings["timer_you"].format(t=int(self.human_time)), is_ar)
        )
        self.cpu_timer_label.config(
            text=GameScreen._ar_safe(strings["timer_cpu"].format(t=int(self.cpu_time)), is_ar)
        )
        self.master.after(500, self._tick)

    def _reset_timers(self):
        self._stop_timer()
        self.human_time = 0.0
        self.cpu_time   = 0.0
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()
        self.you_timer_label.config(
            text=GameScreen._ar_safe(strings["timer_you"].format(t=0), is_ar)
        )
        self.cpu_timer_label.config(
            text=GameScreen._ar_safe(strings["timer_cpu"].format(t=0), is_ar)
        )

    # ── Turn helpers ──────────────────────────────────────────────────────────

    def _is_human_turn(self) -> bool:
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()
        return self.turn_label.cget("text") == localize(strings["your_turn"], is_ar)

    def _set_turn(self, whose: str):
        """Update the turn label. `whose` is "human" or "cpu"."""
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()
        text_key = "your_turn" if whose == "human" else "cpu_turn"
        self.turn_label.config(text=localize(strings[text_key], is_ar))

    # ── Event handlers ────────────────────────────────────────────────────────

    def _on_canvas_click(self, event):
        if not self._is_human_turn():
            return

        strings = self.app.strings()
        is_ar   = self.app.is_arabic()
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE

        is_valid, error_message = self.engine.validate_move(
            self.board, row, col, strings
        )
        if not is_valid:
            show_dialog(
                self.master,
                strings["invalid_move"],
                error_message,
                self.app.colors(),
                is_arabic=is_ar,
            )
            return

        self.app.play_sound("place")
        self.board = self.engine.make_move(self.board, row, col, "O")
        self._refresh_board()

        if self.engine.terminal(self.board):
            return

        if not self.engine.valid_moves(self.board, "X"):
            show_dialog(
                self.master, "",
                strings["no_moves_cpu"],
                self.app.colors(), is_arabic=is_ar,
            )
            return

        self._set_turn("cpu")
        self._stop_timer()
        self._start_timer("cpu")
        self.master.after(700, self._cpu_play)

    def _cpu_play(self):
        """Run AI search in a background thread so the timer ticks during thinking."""
        import threading

        DEPTH_MAP = {"easy": 2, "medium": 4, "hard": 6}
        depth = DEPTH_MAP.get(self.app.settings["difficulty"], 4)

        def run_ai():
            new_board, ai_stats = self.engine.best_move(self.board, depth=depth)
            # Schedule UI update back on the main thread
            self.master.after(0, lambda: self._finish_cpu_turn(new_board, ai_stats))

        threading.Thread(target=run_ai, daemon=True).start()

    def _finish_cpu_turn(self, new_board: list, ai_stats: dict | None = None):
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()

        self.board = new_board
        self.app.play_sound("place")
        self._refresh_board()

        # Update AI Stats Panel
        if ai_stats and hasattr(self, "ai_nodes_label"):
            nodes = ai_stats.get("nodes", 0)
            depth = ai_stats.get("depth", 0)
            score = ai_stats.get("score", 0)
            nodes_str = f"{nodes:,}" if nodes < 1_000_000 else f"{nodes/1_000_000:.1f}M"
            self.ai_nodes_label.config(text=f"Nodes: {nodes_str}")
            self.ai_depth_label.config(text=f"Depth: {depth}")
            score_prefix = "+" if score > 0 else ""
            self.ai_score_label.config(text=f"Score: {score_prefix}{score}")

        if self.engine.terminal(self.board):
            return

        if not self.engine.valid_moves(self.board, "O"):
            show_dialog(
                self.master, "",
                strings["no_moves_you"],
                self.app.colors(), is_arabic=is_ar,
            )
            self._cpu_play()
            return

        self._set_turn("human")
        self._stop_timer()
        self._start_timer("human")

    def _pass_turn(self):
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()

        if not self._is_human_turn():
            show_dialog(
                self.master, "",
                strings["not_your_turn"],
                self.app.colors(), is_arabic=is_ar,
            )
            return

        # Player can always pass — no restriction
        self._set_turn("cpu")
        self._stop_timer()
        self._start_timer("cpu")
        self._cpu_play()

    def _handle_game_over(self):
        self._stop_timer()
        strings = self.app.strings()
        is_ar   = self.app.is_arabic()

        x_count, o_count = self.engine.count(self.board)

        if o_count > x_count:
            result_text = strings["you_win"]
            self.app.stats["wins"]   += 1
            self.app.play_sound("win")
        elif x_count > o_count:
            result_text = strings["cpu_wins"]
            self.app.stats["losses"] += 1
            self.app.play_sound("lose")
        else:
            result_text = strings["draw"]
            self.app.stats["draws"]  += 1

        # Refresh stat labels
        stats = self.app.stats
        self.wins_label.config(
            text=localize(strings["wins"].format(n=stats["wins"]), is_ar)
        )
        self.losses_label.config(
            text=localize(strings["losses"].format(n=stats["losses"]), is_ar)
        )
        self.draws_label.config(
            text=localize(strings["draws"].format(n=stats["draws"]), is_ar)
        )

        score_line = strings["final_score"].format(
            x=x_count, o=o_count,
            ht=int(self.human_time),
            ct=int(self.cpu_time),
        )
        # Keep result and score on separate lines so bidi handles each line cleanly
        final_message = result_text + "\n" + score_line
        show_dialog(
            self.master,
            strings["game_over"],
            final_message,
            self.app.colors(),
            is_arabic=is_ar,
        )

        wants_replay = show_dialog(
            self.master,
            strings["play_again"],
            strings["play_again_q"],
            self.app.colors(),
            kind="yesno",
            is_arabic=is_ar,
        )
        if wants_replay:
            self._start_new_game()

    def _start_new_game(self):
        self.engine = Othello()
        self.board  = copy.deepcopy(self.engine.board)
        self._set_turn("human")
        self._reset_timers()
        self._refresh_board()
        self._start_timer("human")

    def _go_to_menu(self):
        self._stop_timer()
        self.app.show_menu()
