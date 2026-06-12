"""
tests/test_game_logic.py — Unit tests for game_logic.py

Run with:
    pytest tests/test_game_logic.py -v

No Tkinter required — game_logic.py is fully self-contained.
"""

import sys
import os
import copy
import pytest

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game_logic import Othello


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def game():
    """Fresh Othello instance with standard starting position."""
    return Othello()


@pytest.fixture
def empty_board():
    """Completely empty 8×8 board."""
    return [[" "] * 8 for _ in range(8)]


# ── Utility methods ───────────────────────────────────────────────────────────

class TestUtility:
    def test_opponent_of_x_is_o(self, game):
        assert game.opponent("X") == "O"

    def test_opponent_of_o_is_x(self, game):
        assert game.opponent("O") == "X"

    def test_in_bounds_center(self, game):
        assert game.in_bounds(4, 4) is True

    def test_in_bounds_corner(self, game):
        assert game.in_bounds(0, 0) is True
        assert game.in_bounds(7, 7) is True

    def test_in_bounds_negative_row(self, game):
        assert game.in_bounds(-1, 0) is False

    def test_in_bounds_negative_col(self, game):
        assert game.in_bounds(0, -1) is False

    def test_in_bounds_out_of_range(self, game):
        assert game.in_bounds(8, 0) is False
        assert game.in_bounds(0, 8) is False


# ── Starting position ─────────────────────────────────────────────────────────

class TestInitialBoard:
    def test_starting_discs_count(self, game):
        x_count, o_count = game.count(game.board)
        assert x_count == 2
        assert o_count == 2

    def test_starting_disc_positions(self, game):
        b = game.board
        assert b[3][3] == "O"
        assert b[3][4] == "X"
        assert b[4][3] == "X"
        assert b[4][4] == "O"

    def test_remaining_cells_empty(self, game):
        b = game.board
        occupied = {(3, 3), (3, 4), (4, 3), (4, 4)}
        for r in range(8):
            for c in range(8):
                if (r, c) not in occupied:
                    assert b[r][c] == " "


# ── Valid moves ───────────────────────────────────────────────────────────────

class TestValidMoves:
    def test_x_has_4_moves_at_start(self, game):
        moves = game.valid_moves(game.board, "X")
        assert len(moves) == 4

    def test_o_has_4_moves_at_start(self, game):
        moves = game.valid_moves(game.board, "O")
        assert len(moves) == 4

    def test_x_start_moves_are_correct(self, game):
        moves = set(game.valid_moves(game.board, "X"))
        expected = {(2, 3), (3, 2), (4, 5), (5, 4)}
        assert moves == expected

    def test_o_start_moves_are_correct(self, game):
        moves = set(game.valid_moves(game.board, "O"))
        expected = {(2, 4), (3, 5), (4, 2), (5, 3)}
        assert moves == expected

    def test_no_moves_on_full_board(self, game, empty_board):
        # Fill the board entirely with X — O has no moves
        for r in range(8):
            for c in range(8):
                empty_board[r][c] = "X"
        moves = game.valid_moves(empty_board, "O")
        assert moves == []

    def test_moves_only_on_empty_cells(self, game):
        moves = game.valid_moves(game.board, "X")
        for r, c in moves:
            assert game.board[r][c] == " "


# ── can_flip ──────────────────────────────────────────────────────────────────

class TestCanFlip:
    def test_valid_x_move_can_flip(self, game):
        assert game.can_flip(game.board, 2, 3, "X") is True

    def test_invalid_occupied_cell_cannot_flip(self, game):
        # (3,3) is already "O" — can't place there
        assert game.can_flip(game.board, 3, 3, "X") is False

    def test_corner_cannot_flip_at_start(self, game):
        assert game.can_flip(game.board, 0, 0, "X") is False


# ── make_move & flip_discs ────────────────────────────────────────────────────

class TestMakeMove:
    def test_make_move_places_disc(self, game):
        new_board = game.make_move(game.board, 2, 3, "X")
        assert new_board[2][3] == "X"

    def test_make_move_flips_discs(self, game):
        # X plays (2,3) → (3,3) which was "O" should flip to "X"
        new_board = game.make_move(game.board, 2, 3, "X")
        assert new_board[3][3] == "X"

    def test_make_move_does_not_mutate_original(self, game):
        original = copy.deepcopy(game.board)
        game.make_move(game.board, 2, 3, "X")
        assert game.board == original

    def test_make_move_updates_count(self, game):
        new_board = game.make_move(game.board, 2, 3, "X")
        x_count, o_count = game.count(new_board)
        # X placed 1 new disc and flipped 1 O → X=4, O=1
        assert x_count == 4
        assert o_count == 1

    def test_make_move_o_flips_x(self, game):
        new_board = game.make_move(game.board, 2, 4, "O")
        assert new_board[3][4] == "O"


# ── count ─────────────────────────────────────────────────────────────────────

class TestCount:
    def test_count_initial(self, game):
        x, o = game.count(game.board)
        assert x == 2 and o == 2

    def test_count_empty_board(self, game, empty_board):
        x, o = game.count(empty_board)
        assert x == 0 and o == 0

    def test_count_all_x(self, game, empty_board):
        for r in range(8):
            for c in range(8):
                empty_board[r][c] = "X"
        x, o = game.count(empty_board)
        assert x == 64 and o == 0


# ── terminal ──────────────────────────────────────────────────────────────────

class TestTerminal:
    def test_not_terminal_at_start(self, game):
        assert game.terminal(game.board) is False

    def test_terminal_when_board_full(self, game, empty_board):
        for r in range(8):
            for c in range(8):
                empty_board[r][c] = "X" if (r + c) % 2 == 0 else "O"
        # Full board → neither player can move
        assert game.terminal(empty_board) is True

    def test_terminal_when_one_color_gone(self, game, empty_board):
        # All X, no O → O has no moves, X has no moves (nothing to flip)
        for r in range(8):
            for c in range(8):
                empty_board[r][c] = "X"
        assert game.terminal(empty_board) is True


# ── evaluate ─────────────────────────────────────────────────────────────────

class TestEvaluate:
    def test_evaluate_balanced_at_start(self, game):
        # Equal discs, equal mobility → score should be 0 or near 0
        score = game.evaluate(game.board)
        assert isinstance(score, int)

    def test_evaluate_favors_x_corners(self, game, empty_board):
        # Give X all 4 corners, balanced discs elsewhere
        empty_board[0][0] = "X"
        empty_board[0][7] = "X"
        empty_board[7][0] = "X"
        empty_board[7][7] = "X"
        score = game.evaluate(empty_board)
        assert score > 0  # X should win the evaluation

    def test_evaluate_favors_o_corners(self, game, empty_board):
        empty_board[0][0] = "O"
        empty_board[0][7] = "O"
        empty_board[7][0] = "O"
        empty_board[7][7] = "O"
        score = game.evaluate(empty_board)
        assert score < 0  # O should win the evaluation

    def test_evaluate_returns_int(self, game):
        assert isinstance(game.evaluate(game.board), int)


# ── minimax & best_move ───────────────────────────────────────────────────────

class TestMinimax:
    def test_minimax_returns_numeric(self, game):
        score = game.minimax(
            game.board, depth=2,
            is_maximizing=True,
            alpha=float("-inf"), beta=float("inf"),
        )
        assert isinstance(score, (int, float))

    def test_minimax_depth_0_equals_evaluate(self, game):
        score = game.minimax(
            game.board, depth=0,
            is_maximizing=True,
            alpha=float("-inf"), beta=float("inf"),
        )
        assert score == game.evaluate(game.board)

    def test_best_move_returns_tuple(self, game):
        result = game.best_move(game.board, depth=2)
        assert isinstance(result, tuple)
        new_board, ai_stats = result
        assert isinstance(new_board, list)
        assert isinstance(ai_stats, dict)

    def test_best_move_stats_keys(self, game):
        _, stats = game.best_move(game.board, depth=2)
        assert "nodes" in stats
        assert "depth" in stats
        assert "score" in stats

    def test_best_move_nodes_positive(self, game):
        _, stats = game.best_move(game.board, depth=2)
        assert stats["nodes"] > 0

    def test_best_move_depth_recorded(self, game):
        _, stats = game.best_move(game.board, depth=2)
        assert stats["depth"] == 2

    def test_best_move_changes_board(self, game):
        new_board, _ = game.best_move(game.board, depth=2)
        assert new_board != game.board

    def test_best_move_adds_one_x_disc(self, game):
        x_before, _ = game.count(game.board)
        new_board, _ = game.best_move(game.board, depth=2)
        x_after, _ = game.count(new_board)
        assert x_after > x_before

    def test_best_move_no_moves_returns_unchanged(self, game, empty_board):
        # Board full of O — X has no moves
        for r in range(8):
            for c in range(8):
                empty_board[r][c] = "O"
        new_board, stats = game.best_move(empty_board, depth=2)
        assert new_board == empty_board
        assert stats["nodes"] == 0


# ── nodes counter ─────────────────────────────────────────────────────────────

class TestNodesCounter:
    def test_counter_increments(self, game):
        counter = [0]
        game.minimax(
            game.board, depth=2,
            is_maximizing=True,
            alpha=float("-inf"), beta=float("inf"),
            _counter=counter,
        )
        assert counter[0] > 0

    def test_deeper_search_visits_more_nodes(self, game):
        c1, c2 = [0], [0]
        game.minimax(game.board, 2, True, float("-inf"), float("inf"), _counter=c1)
        game.minimax(game.board, 4, True, float("-inf"), float("inf"), _counter=c2)
        assert c2[0] > c1[0]
