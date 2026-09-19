"""
Tracks active inline games in memory, keyed by Telegram's inline_message_id
(the only handle we get back for a message sent via inline mode -- there's
no normal chat_id/message_id for those). Resets if the bot restarts, same
tradeoff as the chat history in bot.py; swap for Redis/DB if that matters.
"""

_games: dict = {}


def create(inline_message_id: str, mode: str, starter, lang: str = "en") -> dict:
    """mode is 'friend' or 'bot'. starter is the Telegram user who invoked it,
    and always plays X. lang is the board text's language for this game's
    whole lifetime (based on whoever started it)."""
    game = {
        "board": [None] * 9,
        "mode": mode,
        "lang": lang,
        "x_id": starter.id,
        "x_name": starter.first_name,
        "o_id": None if mode == "friend" else "BOT",
        "o_name": None if mode == "friend" else "Claude",
        "turn": "X",
    }
    _games[inline_message_id] = game
    return game


def get(inline_message_id: str):
    return _games.get(inline_message_id)


def reset_for_rematch(game: dict):
    """Reset the board in place; in 'friend' mode swap X/O so both players
    get a turn going first."""
    if game["mode"] == "friend":
        game["x_id"], game["o_id"] = game["o_id"], game["x_id"]
        game["x_name"], game["o_name"] = game["o_name"], game["x_name"]
    game["board"] = [None] * 9
    game["turn"] = "X"
