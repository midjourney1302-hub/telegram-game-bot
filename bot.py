"""
A Telegram games bot. No AI chat, no payments -- just tic-tac-toe, playable
via inline mode: type @your_bot_username in any chat (even a DM with a
friend the bot was never added to) to start a game.

Run:
    python bot.py
"""

import logging
import uuid

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChosenInlineResultHandler,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
)

import config
import game_store
import lang_store
import tictactoe
from translations import LANGUAGES, t

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def _language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(label, callback_data=f"lang:{code}")] for code, label in LANGUAGES]
    )


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if lang_store.has(user_id):
        lang = lang_store.get(user_id)
        await update.message.reply_text(
            t(lang, "welcome", username=context.bot.username), parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            t("en", "choose_language"), reply_markup=_language_keyboard()
        )


async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(t("en", "choose_language"), reply_markup=_language_keyboard())


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data.split(":")[1]
    lang_store.set(query.from_user.id, lang)
    await query.answer()
    await query.edit_message_text(
        t(lang, "welcome", username=context.bot.username), parse_mode="Markdown"
    )


# --------------------------------------------------------------------------- #
# Tic-tac-toe
# --------------------------------------------------------------------------- #

def _ttt_text(game: dict) -> str:
    board = game["board"]
    lang = game["lang"]
    result, _ = tictactoe.winner(board)
    header = f"\u274C {game['x_name']}  vs  \u2B55 {game['o_name'] or '(open)'}"

    if result == "draw":
        body = t(lang, "draw")
    elif result in ("X", "O"):
        champ = game["x_name"] if result == "X" else game["o_name"]
        body = t(lang, "win", name=champ)
    elif game["mode"] == "friend" and game["o_id"] is None:
        body = t(lang, "waiting")
    else:
        mover = game["x_name"] if game["turn"] == "X" else game["o_name"]
        symbol = "\u274C" if game["turn"] == "X" else "\u2B55"
        body = t(lang, "turn", symbol=symbol, name=mover)

    return f"{header}\n{body}"


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.inline_query.from_user.id
    empty_board = [None] * 9
    results = [
        InlineQueryResultArticle(
            id=f"ttt_friend_{uid}_{uuid.uuid4().hex[:6]}",
            title="\U0001F3AE Tic-Tac-Toe \u2014 vs a friend",
            description="Posts a board here; whoever taps second plays O",
            input_message_content=InputTextMessageContent("Setting up a tic-tac-toe game\u2026"),
            reply_markup=tictactoe.render_keyboard(empty_board),
        ),
        InlineQueryResultArticle(
            id=f"ttt_bot_{uid}_{uuid.uuid4().hex[:6]}",
            title="\U0001F916 Tic-Tac-Toe \u2014 vs the bot",
            description="Play solo against an unbeatable AI",
            input_message_content=InputTextMessageContent("Setting up a tic-tac-toe game\u2026"),
            reply_markup=tictactoe.render_keyboard(empty_board),
        ),
    ]
    await update.inline_query.answer(results, cache_time=0)


async def chosen_inline_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chosen_inline_result
    if not result.result_id.startswith("ttt_") or not result.inline_message_id:
        return

    mode = "friend" if result.result_id.startswith("ttt_friend") else "bot"
    lang = lang_store.get(result.from_user.id)
    game = game_store.create(result.inline_message_id, mode, result.from_user, lang=lang)

    await context.bot.edit_message_text(
        inline_message_id=result.inline_message_id,
        text=_ttt_text(game),
        reply_markup=tictactoe.render_keyboard(game["board"]),
    )


async def ttt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    inline_message_id = query.inline_message_id
    user = query.from_user

    game = game_store.get(inline_message_id)
    if not game:
        await query.answer(
            "This game session has expired (probably a bot restart). "
            "Start a new one by typing my username in the chat.",
            show_alert=True,
        )
        return

    if query.data == "ttt:restart":
        if user.id not in (game["x_id"], game["o_id"]):
            await query.answer("Only players in this game can restart.", show_alert=True)
            return
        game_store.reset_for_rematch(game)
        await query.answer("Rematch!")
        await context.bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=_ttt_text(game),
            reply_markup=tictactoe.render_keyboard(game["board"]),
        )
        return

    board = game["board"]
    idx = int(query.data.split(":")[1])

    if tictactoe.winner(board)[0]:
        await query.answer("This game's over \u2014 tap Rematch to play again.", show_alert=True)
        return
    if board[idx] is not None:
        await query.answer("That square's taken.", show_alert=True)
        return

    turn = game["turn"]
    if turn == "X":
        if user.id != game["x_id"]:
            await query.answer("It's not your turn.", show_alert=True)
            return
    else:  # turn == "O"
        if game["mode"] == "bot":
            await query.answer("The bot's move happens automatically \u2014 hang on.", show_alert=True)
            return
        if game["o_id"] is None:
            if user.id == game["x_id"]:
                await query.answer("Waiting for someone else to join as O.", show_alert=True)
                return
            game["o_id"], game["o_name"] = user.id, user.first_name
        elif user.id != game["o_id"]:
            await query.answer("This game already has two players.", show_alert=True)
            return

    board[idx] = turn
    result, _ = tictactoe.winner(board)

    if not result:
        game["turn"] = "O" if turn == "X" else "X"
        if game["mode"] == "bot" and game["turn"] == "O":
            bot_idx = tictactoe.best_move(board, "O")
            board[bot_idx] = "O"
            result, _ = tictactoe.winner(board)
            if not result:
                game["turn"] = "X"

    await query.answer()
    await context.bot.edit_message_text(
        inline_message_id=inline_message_id,
        text=_ttt_text(game),
        reply_markup=tictactoe.render_keyboard(
            board, game_over=bool(result), rematch_label=t(game["lang"], "rematch_button")
        ),
    )


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main():
    if not config.TELEGRAM_BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language_cmd))
    app.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang:"))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(ChosenInlineResultHandler(chosen_inline_result))
    app.add_handler(CallbackQueryHandler(ttt_callback, pattern=r"^ttt:"))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
