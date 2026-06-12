"""
languages.py — Localization strings for Othello.

Supported languages: English, Arabic (العربية), German (Deutsch).
Arabic strings are rendered RTL via arabic_reshaper + python-bidi at display time.
"""

LANGUAGES: dict[str, dict[str, str]] = {

    "English": {
        # ── Titles & navigation ──
        "title":            "OTHELLO",
        "subtitle":         "Strategy Board Game",
        "start":            "▶   Start Game",
        "settings":         "⚙   Settings",
        "exit":             "✕   Exit",
        "back":             "← Back to Menu",
        "menu":             "← Menu",

        # ── Settings screen ──
        "settings_title":   "Settings",
        "theme_label":      "Theme",
        "sound_label":      "Sound",
        "language_label":   "Language",
        "sound_on":         "Sound  ON",
        "sound_off":        "Sound  OFF",

        # ── In-game ──
        "new_game":         "New Game",
        "pass_turn":        "⏭  Pass Turn",
        "your_turn":        "Your Turn  (O)",
        "cpu_turn":         "Computer's Turn  (X)",
        "score":            "CPU: {x}   ·   You: {o}",
        "timer_you":        "⏱  You: {t}s",
        "timer_cpu":        "⏱  CPU: {t}s",

        # ── Statistics ──
        "stats_title":      "Session Stats",
        "wins":             "Wins: {n}",
        "losses":           "Losses: {n}",
        "draws":            "Draws: {n}",

        # ── Error / info messages ──
        "invalid_move":     "Invalid Move",
        "out_of_bounds":    "That cell is outside the board.",
        "occupied":         "That cell is already occupied.",
        "no_flip":          "No discs would be flipped by this move.",
        "no_moves_cpu":     "Computer has no valid moves — your turn again.",
        "no_moves_you":     "You have no valid moves — computer plays again.",
        "not_your_turn":    "It is not your turn yet.",
        "must_play":        "You have valid moves available — you must play.",

        # ── End-of-game ──
        "game_over":        "Game Over",
        "you_win":          "You win! 🎉",
        "cpu_wins":         "Computer wins.",
        "draw":             "It's a draw.",
        "final_score":      "CPU: {x}  ·  You: {o}\nYour time: {ht}s   ·   CPU: {ct}s",
        "play_again":       "Play Again",
        "play_again_q":     "Would you like to play again?",

        # ── About / credits ──
        "about_label":      "About",
        "contributors":     "Contributors",

        # ── Difficulty ──
        "difficulty_label": "Difficulty",
        "diff_easy":        "Easy",
        "diff_medium":      "Medium",
        "diff_hard":        "Hard",
    },

    "العربية": {
        "title":            "أوثيلو",
        "subtitle":         "لعبة الاستراتيجية",
        "start":            "▶   ابدأ اللعبة",
        "settings":         "⚙   الإعدادات",
        "exit":             "✕   خروج",
        "back":             "رجوع للقائمة",
        "menu":             "القائمة",

        "settings_title":   "الإعدادات",
        "theme_label":      "المظهر",
        "sound_label":      "الصوت",
        "language_label":   "اللغة",
        "sound_on":         "الصوت  مفعّل",
        "sound_off":        "الصوت  مكتوم",

        "new_game":         "لعبة جديدة",
        "pass_turn":        "⏭  تخطى الدور",
        "your_turn":        "دورك  (O)",
        "cpu_turn":         "دور الكمبيوتر  (X)",
        "score":            "CPU: {x}   ·   أنتِ: {o}",
        "timer_you":        "⏱ أنتِ: {t}ث",
        "timer_cpu":        "⏱ CPU: {t}ث",

        "stats_title":      "إحصائيات الجلسة",
        "wins":             "انتصارات: {n}",
        "losses":           "خسائر: {n}",
        "draws":            "تعادل: {n}",

        "invalid_move":     "حركة غير صحيحة",
        "out_of_bounds":    "الحركة خارج حدود اللوح.",
        "occupied":         "الخانة مشغولة بالفعل.",
        "no_flip":          "لا يوجد قرص سيُقلب بهذه الحركة.",
        "no_moves_cpu":     "الكمبيوتر ليس لديه حركات — دورك مرة أخرى.",
        "no_moves_you":     "ليس لديك حركات — الكمبيوتر يلعب مرة أخرى.",
        "not_your_turn":    "ليس دورك الآن.",
        "must_play":        "لديك حركات صالحة — يجب أن تلعب.",

        "game_over":        "انتهت اللعبة",
        "you_win":          "أنت الفائزة!",
        "cpu_wins":         "الكمبيوتر يفوز.",
        "draw":             "تعادل.",
        "final_score":      "النتيجة: أنت {o}  ·  الكمبيوتر {x}\nوقتك: {ht} ث   ·   الكمبيوتر: {ct} ث",
        "play_again":       "العب مجدداً",
        "play_again_q":     "هل تريد اللعب مرة أخرى",

        "about_label":      "حول",
        "contributors":     "المساهمون",

        # ── Difficulty ──
        "difficulty_label": "مستوى الصعوبة",
        "diff_easy":        "سهل",
        "diff_medium":      "متوسط",
        "diff_hard":        "صعب",
    },

    "Deutsch": {
        "title":            "OTHELLO",
        "subtitle":         "Strategiebrettspiel",
        "start":            "▶   Spiel starten",
        "settings":         "⚙   Einstellungen",
        "exit":             "✕   Beenden",
        "back":             "← Zurück zum Menü",
        "menu":             "← Menü",

        "settings_title":   "Einstellungen",
        "theme_label":      "Design",
        "sound_label":      "Ton",
        "language_label":   "Sprache",
        "sound_on":         "Ton  AN",
        "sound_off":        "Ton  AUS",

        "new_game":         "Neues Spiel",
        "pass_turn":        "⏭  Zug überspringen",
        "your_turn":        "Dein Zug  (O)",
        "cpu_turn":         "Computer ist dran  (X)",
        "score":            "CPU: {x}   ·   Du: {o}",
        "timer_you":        "⏱  Du: {t}s",
        "timer_cpu":        "⏱  CPU: {t}s",

        "stats_title":      "Spielstatistiken",
        "wins":             "Siege: {n}",
        "losses":           "Niederlagen: {n}",
        "draws":            "Unentschieden: {n}",

        "invalid_move":     "Ungültiger Zug",
        "out_of_bounds":    "Zug außerhalb des Spielfelds.",
        "occupied":         "Feld ist bereits belegt.",
        "no_flip":          "Keine Scheiben würden umgedreht.",
        "no_moves_cpu":     "Computer hat keine gültigen Züge — du bist wieder dran.",
        "no_moves_you":     "Du hast keine gültigen Züge — Computer spielt nochmal.",
        "not_your_turn":    "Du bist noch nicht dran.",
        "must_play":        "Du hast gültige Züge — du musst spielen.",

        "game_over":        "Spiel vorbei",
        "you_win":          "Du gewinnst! 🎉",
        "cpu_wins":         "Computer gewinnt.",
        "draw":             "Unentschieden.",
        "final_score":      "CPU: {x}  ·  Du: {o}\nDeine Zeit: {ht}s   ·   CPU: {ct}s",
        "play_again":       "Nochmal spielen",
        "play_again_q":     "Möchtest du nochmal spielen?",

        "about_label":      "Über",
        "contributors":     "Mitwirkende",

        # ── Difficulty ──
        "difficulty_label": "Schwierigkeitsgrad",
        "diff_easy":        "Leicht",
        "diff_medium":      "Mittel",
        "diff_hard":        "Schwer",
    },
}

# Default language on first launch
DEFAULT_LANGUAGE = "English"
