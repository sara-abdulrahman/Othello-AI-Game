"""
ui/widgets.py — Reusable UI components for Othello.

Contains:
  - render_arabic : RTL shaping helper (apply ONCE, just before display)
  - localize      : convenience wrapper
  - ModernButton  : flat themed button with hover
  - Separator     : 1-px divider
  - show_dialog   : themed modal (info / yes-no)

Arabic text rule
----------------
Every string goes through render_arabic() exactly ONE time, at the last
possible moment — i.e. as the `text=` argument of a tk widget.
Never call it on strings that are passed between functions; shape them at
the widget call site only.
"""

import tkinter as tk


# ── Arabic / RTL helper ───────────────────────────────────────────────────────

def render_arabic(text: str) -> str:
    """
    Shape and reorder Arabic text for Tkinter.
    Tkinter draws characters LTR, so we use arabic_reshaper to connect
    glyphs correctly, then get_display to reverse word order so that
    right-aligned labels read correctly from right to left.
    """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return "\n".join(
            get_display(arabic_reshaper.reshape(line))
            for line in text.split("\n")
        )
    except Exception:
        return text


def localize(text: str, is_arabic: bool) -> str:
    """Shape text for RTL display when is_arabic is True."""
    return render_arabic(text) if is_arabic else text


# ── Modern flat button ────────────────────────────────────────────────────────

class ModernButton(tk.Button):
    """
    Flat, theme-aware button with hover colour feedback.

    Variants:
        "default" — subtle background
        "accent"  — filled with theme accent colour
        "ghost"   — near-invisible, for low-priority actions
    """

    def __init__(
        self,
        parent,
        text: str,
        command,
        colors: dict,
        variant: str = "default",
        font_size: int = 12,
        width: int = 26,
        **kwargs,
    ):
        self._colors    = colors
        self._variant   = variant
        bg_color, fg_color, hover_color = self._resolve_colors(colors, variant)
        self._normal_bg = bg_color
        self._hover_bg  = hover_color

        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", font_size, "bold"),
            bg=bg_color,
            fg=fg_color,
            activebackground=hover_color,
            activeforeground=fg_color,
            relief="flat",
            overrelief="flat",
            bd=0,
            padx=20,
            pady=11,
            cursor="hand2",
            width=width,
            **kwargs,
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    @staticmethod
    def _resolve_colors(colors: dict, variant: str) -> tuple:
        if variant == "accent":
            return colors["accent"], colors["bg_window"], colors["btn_hover"]
        if variant == "ghost":
            return colors["bg_window"], colors["label_fg"], colors["bg_panel"]
        return colors["btn_bg"], colors["btn_fg"], colors["btn_hover"]

    def _on_enter(self, _e): self.config(bg=self._hover_bg)
    def _on_leave(self, _e): self.config(bg=self._normal_bg)


# ── Separator ─────────────────────────────────────────────────────────────────

class Separator(tk.Frame):
    """One-pixel horizontal rule."""

    def __init__(self, parent, colors: dict, **kwargs):
        super().__init__(parent, height=1, bg=colors["separator"], **kwargs)


# ── Modal dialog ──────────────────────────────────────────────────────────────

def show_dialog(
    parent,
    title: str,
    message: str,
    colors: dict,
    kind: str = "info",
    is_arabic: bool = False,
) -> bool:
    """
    Themed modal dialog.  title and message must be PLAIN (un-shaped) strings.
    This function applies render_arabic() internally at widget-creation time.

    Returns True if the user clicked Yes (kind="yesno"), False otherwise.
    """
    dialog = tk.Toplevel(parent)
    dialog.title("")
    dialog.resizable(False, False)
    dialog.grab_set()
    dialog.configure(bg=colors["bg_window"])

    # ── Centre over parent ──
    parent.update_idletasks()
    px, py = parent.winfo_rootx(), parent.winfo_rooty()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    dw, dh = 380, 200
    dialog.geometry(f"{dw}x{dh}+{px + (pw - dw)//2}+{py + (ph - dh)//2}")

    # ── Title ──
    if title:
        shaped_title = render_arabic(title) if is_arabic else title
        tk.Label(
            dialog,
            text=shaped_title,
            font=("Segoe UI", 12, "bold"),
            bg=colors["bg_window"],
            fg=colors["accent"],
            anchor="e" if is_arabic else "w",
            justify="right" if is_arabic else "left",
        ).pack(pady=(18, 0), padx=24, fill="x")

    # ── Message ──
    if is_arabic:
        # Shape each line independently to preserve number direction
        shaped_msg = "\n".join(render_arabic(ln) for ln in message.split("\n"))
    else:
        shaped_msg = message
    tk.Label(
        dialog,
        text=shaped_msg,
        font=("Segoe UI", 11),
        bg=colors["bg_window"],
        fg=colors["label_fg"],
        wraplength=340,
        justify="right" if is_arabic else "center",
    ).pack(pady=(10, 14), padx=24)

    Separator(dialog, colors).pack(fill="x", padx=24)

    # ── Buttons ──
    result  = {"value": False}
    btn_row = tk.Frame(dialog, bg=colors["bg_window"])
    btn_row.pack(pady=12)

    btn_kw = dict(colors=colors, font_size=10, width=10)

    if kind == "yesno":
        # Shape short Arabic words explicitly
        yes_text = render_arabic("نعم") if is_arabic else "Yes"
        no_text  = render_arabic("لا")  if is_arabic else "No"

        def on_yes():
            result["value"] = True
            dialog.destroy()

        def on_no():
            result["value"] = False
            dialog.destroy()

        # In Arabic layout: Yes on left, No on right (visually natural for RTL)
        if is_arabic:
            ModernButton(btn_row, text=no_text,  command=on_no,
                         **btn_kw).pack(side=tk.LEFT, padx=6)
            ModernButton(btn_row, text=yes_text, command=on_yes,
                         variant="accent", **btn_kw).pack(side=tk.LEFT, padx=6)
        else:
            ModernButton(btn_row, text=yes_text, command=on_yes,
                         variant="accent", **btn_kw).pack(side=tk.LEFT, padx=6)
            ModernButton(btn_row, text=no_text,  command=on_no,
                         **btn_kw).pack(side=tk.LEFT, padx=6)
    else:
        ModernButton(btn_row, text="OK", command=dialog.destroy,
                     variant="accent", **btn_kw).pack()

    dialog.wait_window()
    return result["value"]
