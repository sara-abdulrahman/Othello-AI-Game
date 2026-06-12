"""
themes.py — Visual theme definitions for Othello.

Each theme is a dictionary of named color tokens used throughout the UI.
All colors follow a muted, modern palette to reduce eye strain.
"""

# ---------------------------------------------------------------------------
# Color Token Reference
# ---------------------------------------------------------------------------
# bg_window   — outer window / screen background
# bg_board    — game board background
# bg_panel    — stats / side-panel background
# grid        — board grid lines
# disc_dark   — dark player disc fill (CPU / "X")
# disc_light  — light player disc fill (Human / "O")
# outline_dark  — dark disc border
# outline_light — light disc border
# valid_move  — valid-move dot color
# btn_bg      — button background
# btn_fg      — button text
# btn_hover   — button hover / active background
# label_fg    — secondary label / body text
# accent      — primary accent (titles, highlights)
# separator   — subtle divider lines
# ---------------------------------------------------------------------------

THEMES: dict[str, dict[str, str]] = {

    # ── Modern Dark ────────────────────────────────────────────────────────
    # Charcoal background, warm slate board, rose-gold accent.
    "Modern Dark": {
        "bg_window":    "#1A1C22",
        "bg_board":     "#242830",
        "bg_panel":     "#14161B",
        "grid":         "#2E3240",
        "disc_dark":    "#0F1115",
        "disc_light":   "#E8E4DC",
        "outline_dark": "#3A3F50",
        "outline_light":"#C4B8A8",
        "valid_move":   "#C98B6A",
        "btn_bg":       "#2C3040",
        "btn_fg":       "#D6CFCA",
        "btn_hover":    "#3E4560",
        "label_fg":     "#9098A8",
        "accent":       "#C98B6A",
        "separator":    "#2A2E3A",
    },

    # ── Sage Green ─────────────────────────────────────────────────────────
    # Forest-inspired, soft greens with warm off-white discs.
    "Sage Green": {
        "bg_window":    "#1E2620",
        "bg_board":     "#253028",
        "bg_panel":     "#181E1A",
        "grid":         "#2F3D32",
        "disc_dark":    "#101610",
        "disc_light":   "#F0EDE4",
        "outline_dark": "#3A4E3C",
        "outline_light":"#C8C4B8",
        "valid_move":   "#8EAF7A",
        "btn_bg":       "#2A3A2D",
        "btn_fg":       "#C8D4C0",
        "btn_hover":    "#3B5040",
        "label_fg":     "#7E9882",
        "accent":       "#8EAF7A",
        "separator":    "#252E27",
    },

    # ── Coffee ─────────────────────────────────────────────────────────────
    # Warm espresso tones, cream discs, caramel accent.
    "Coffee": {
        "bg_window":    "#221810",
        "bg_board":     "#2E2018",
        "bg_panel":     "#180E08",
        "grid":         "#3D2A1E",
        "disc_dark":    "#0E0804",
        "disc_light":   "#F5EED8",
        "outline_dark": "#4A3528",
        "outline_light":"#D4C4A0",
        "valid_move":   "#C4894A",
        "btn_bg":       "#3A2818",
        "btn_fg":       "#E0CEAC",
        "btn_hover":    "#543C28",
        "label_fg":     "#A08060",
        "accent":       "#C4894A",
        "separator":    "#2A1E12",
    },

    # ── Minimal Light ──────────────────────────────────────────────────────
    # Clean off-white with warm grey tones, slate accent.
    "Minimal Light": {
        "bg_window":    "#F4F2EE",
        "bg_board":     "#E8E5DF",
        "bg_panel":     "#ECEAE5",
        "grid":         "#CEC9C0",
        "disc_dark":    "#1C1C1E",
        "disc_light":   "#FFFFFF",
        "outline_dark": "#3A3A3C",
        "outline_light":"#B8B2A8",
        "valid_move":   "#6B7A8D",
        "btn_bg":       "#E0DDD6",
        "btn_fg":       "#3A3530",
        "btn_hover":    "#CCCAC4",
        "label_fg":     "#7A7570",
        "accent":       "#5A6678",
        "separator":    "#D8D4CC",
    },
}

# Default theme applied on first launch
DEFAULT_THEME = "Modern Dark"
