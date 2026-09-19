"""
Pure game logic for tic-tac-toe: win detection, an unbeatable minimax AI,
and rendering the board as a Telegram inline keyboard. No Telegram API calls
live here on purpose -- keeps it easy to test and reuse.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]

SYMBOLS = {"X": "\u274C", "O": "\u2B55", None: "\u00B7"}  # ❌ ⭕ ·


def winner(board: list) -> tuple:
    """Returns ('X'|'O', winning_line) or ('draw', None) or (None, None)."""
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    if all(cell is not None for cell in board):
        return "draw", None
    return None, None


def _minimax(board: list, player: str, ai: str, human: str, depth: int = 0):
    result, _ = winner(board)
    # Score wins/losses adjusted by depth so the AI prefers the *fastest* win
    # and the *slowest* loss, instead of any old optimal-but-sluggish line.
    if result == ai:
        return 10 - depth, None
    if result == human:
        return depth - 10, None
    if result == "draw":
        return 0, None

    scored = []
    for i in range(9):
        if board[i] is None:
            board[i] = player
            score, _ = _minimax(board, human if player == ai else ai, ai, human, depth + 1)
            board[i] = None
            scored.append((score, i))

    if player == ai:
        return max(scored, key=lambda s: s[0])
    return min(scored, key=lambda s: s[0])


def best_move(board: list, ai_symbol: str) -> int:
    """Optimal move for ai_symbol. Plays perfectly -- best a human can do is draw."""
    human = "O" if ai_symbol == "X" else "X"
    _, move = _minimax(list(board), ai_symbol, ai_symbol, human)
    return move


def render_keyboard(board: list, game_over: bool = False, rematch_label: str = "\U0001F504 Rematch") -> InlineKeyboardMarkup:
    rows = []
    for r in range(3):
        row = []
        for c in range(3):
            i = r * 3 + c
            row.append(InlineKeyboardButton(SYMBOLS[board[i]], callback_data=f"ttt:{i}"))
        rows.append(row)
    if game_over:
        rows.append([InlineKeyboardButton(rematch_label, callback_data="ttt:restart")])
    return InlineKeyboardMarkup(rows)
