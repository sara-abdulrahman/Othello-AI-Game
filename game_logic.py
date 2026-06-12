"""
game_logic.py — Core Othello / Reversi engine.

Contains the board model, move validation, disc-flipping rules,
terminal detection, board evaluation, and Minimax with Alpha-Beta pruning.

No UI dependencies — this module is fully self-contained and testable.
"""

import copy


class Othello:
    """
    Othello board and AI engine.

    Board representation:
        8×8 list-of-lists where each cell is one of:
            " "  — empty
            "X"  — dark player (CPU)
            "O"  — light player (Human)
    """

    DIRECTIONS = [
        (-1,  0),  # N
        ( 1,  0),  # S
        ( 0, -1),  # W
        ( 0,  1),  # E
        (-1, -1),  # NW
        (-1,  1),  # NE
        ( 1, -1),  # SW
        ( 1,  1),  # SE
    ]

    # Corner positions — high strategic value in evaluation
    CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]

    def __init__(self):
        self.board = [[" "] * 8 for _ in range(8)]
        # Standard starting position
        self.board[3][3] = "O"
        self.board[3][4] = "X"
        self.board[4][3] = "X"
        self.board[4][4] = "O"

    # ── Utility ─────────────────────────────────────────────────────────────

    @staticmethod
    def opponent(player: str) -> str:
        return "O" if player == "X" else "X"

    @staticmethod
    def in_bounds(row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    # ── Move rules ──────────────────────────────────────────────────────────

    def can_flip(self, board: list, row: int, col: int, player: str) -> bool:
        """Return True if placing `player` at (row, col) flips at least one disc."""
        opp = self.opponent(player)
        for delta_row, delta_col in self.DIRECTIONS:
            r, c = row + delta_row, col + delta_col
            found_opponent = False
            while self.in_bounds(r, c):
                if board[r][c] == opp:
                    found_opponent = True
                elif board[r][c] == player:
                    if found_opponent:
                        return True
                    break
                else:
                    break
                r += delta_row
                c += delta_col
        return False

    def valid_moves(self, board: list, player: str) -> list[tuple[int, int]]:
        """Return a list of (row, col) pairs where `player` may legally place a disc."""
        return [
            (row, col)
            for row in range(8)
            for col in range(8)
            if board[row][col] == " " and self.can_flip(board, row, col, player)
        ]

    def validate_move(
        self, board: list, row: int, col: int, strings: dict
    ) -> tuple[bool, str]:
        """
        Validate a human move attempt.
        Returns (True, "") on success or (False, error_message) on failure.
        `strings` is the active language dictionary for localised messages.
        """
        if not self.in_bounds(row, col):
            return False, strings["out_of_bounds"]
        if board[row][col] != " ":
            return False, strings["occupied"]
        if not self.can_flip(board, row, col, "O"):
            return False, strings["no_flip"]
        return True, ""

    def flip_discs(self, board: list, row: int, col: int, player: str) -> None:
        """Flip all discs captured by placing `player` at (row, col). Mutates `board`."""
        opp = self.opponent(player)
        for delta_row, delta_col in self.DIRECTIONS:
            r, c = row + delta_row, col + delta_col
            captured = []
            while self.in_bounds(r, c):
                if board[r][c] == opp:
                    captured.append((r, c))
                elif board[r][c] == player:
                    for flip_row, flip_col in captured:
                        board[flip_row][flip_col] = player
                    break
                else:
                    break
                r += delta_row
                c += delta_col

    def make_move(self, board: list, row: int, col: int, player: str) -> list:
        """Return a new board state after placing `player` at (row, col)."""
        new_board = copy.deepcopy(board)
        new_board[row][col] = player
        self.flip_discs(new_board, row, col, player)
        return new_board

    # ── State queries ────────────────────────────────────────────────────────

    def terminal(self, board: list) -> bool:
        """Return True when neither player has any valid move (game over)."""
        return (
            not self.valid_moves(board, "X")
            and not self.valid_moves(board, "O")
        )

    def count(self, board: list) -> tuple[int, int]:
        """Return (x_count, o_count) disc totals."""
        x_count = sum(row.count("X") for row in board)
        o_count = sum(row.count("O") for row in board)
        return x_count, o_count

    # ── AI: Evaluation & Minimax ─────────────────────────────────────────────

    # Edge positions (non-corner border cells)
    EDGES = [
        (r, c)
        for r in range(8) for c in range(8)
        if (r == 0 or r == 7 or c == 0 or c == 7)
        and (r, c) not in [(0, 0), (0, 7), (7, 0), (7, 7)]
    ]

    def evaluate(self, board: list) -> int:
        """
        Static board evaluation from X's perspective (positive = good for CPU).
        Combines disc difference, corner bonuses, edge control, and mobility.
        """
        x_count, o_count = self.count(board)
        score = x_count - o_count

        # Corner control — highest strategic value
        for row, col in self.CORNERS:
            if board[row][col] == "X":
                score += 10
            elif board[row][col] == "O":
                score -= 10

        # Edge control — moderate strategic value
        for row, col in self.EDGES:
            if board[row][col] == "X":
                score += 2
            elif board[row][col] == "O":
                score -= 2

        # Mobility — more available moves = more options = better position
        x_moves = len(self.valid_moves(board, "X"))
        o_moves = len(self.valid_moves(board, "O"))
        if x_moves + o_moves > 0:
            score += 3 * (x_moves - o_moves)

        return score

    def minimax(
        self,
        board: list,
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
        _counter: list | None = None,
    ) -> float:
        """
        Minimax search with Alpha-Beta pruning.

        Args:
            board:          Current board state.
            depth:          Remaining search depth.
            is_maximizing:  True when it is X's (CPU's) turn to maximise.
            alpha:          Best score the maximiser can guarantee.
            beta:           Best score the minimiser can guarantee.
            _counter:       Mutable [int] list used to count nodes visited.

        Returns:
            Evaluated score at this node.
        """
        if _counter is not None:
            _counter[0] += 1

        if depth == 0 or self.terminal(board):
            return self.evaluate(board)

        player = "X" if is_maximizing else "O"
        moves = self.valid_moves(board, player)

        # Pass turn when the active player has no moves
        if not moves:
            return self.minimax(board, depth - 1, not is_maximizing, alpha, beta, _counter)

        if is_maximizing:
            best_score = float("-inf")
            for row, col in moves:
                child_board = self.make_move(board, row, col, player)
                score = self.minimax(child_board, depth - 1, False, alpha, beta, _counter)
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # β cut-off
            return best_score
        else:
            best_score = float("inf")
            for row, col in moves:
                child_board = self.make_move(board, row, col, player)
                score = self.minimax(child_board, depth - 1, True, alpha, beta, _counter)
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # α cut-off
            return best_score

    def best_move(self, board: list, depth: int = 4) -> tuple[list, dict]:
        """
        Return (new_board, ai_stats) after the CPU plays its optimal move.
        ai_stats = {"nodes": int, "depth": int, "score": int}
        Uses Minimax with Alpha-Beta pruning at the given search depth.
        """
        moves = self.valid_moves(board, "X")
        if not moves:
            return board, {"nodes": 0, "depth": depth, "score": 0}

        best_value = float("-inf")
        best_position = None
        counter = [0]

        for row, col in moves:
            candidate_board = self.make_move(board, row, col, "X")
            value = self.minimax(
                candidate_board,
                depth - 1,
                is_maximizing=False,
                alpha=float("-inf"),
                beta=float("inf"),
                _counter=counter,
            )
            if value > best_value:
                best_value = value
                best_position = (row, col)

        new_board = self.make_move(board, best_position[0], best_position[1], "X")
        ai_stats = {"nodes": counter[0], "depth": depth, "score": int(best_value)}
        return new_board, ai_stats
