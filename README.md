# Telegram Games Bot

A simple Telegram bot with one job: tic-tac-toe, playable via inline mode
in any chat. No AI, no API costs, no payments.

## How it works

Type `@your_bot_username` in **any** Telegram chat — a group, or even a DM
with a friend the bot was never added to. Two options appear:

- **vs a friend** — posts a board in that chat; whoever taps a square second becomes O
- **vs the bot** — play solo against an unbeatable minimax AI

Taps update the board live via Telegram's inline keyboard callbacks.

## 1. Set up on your Chromebook

Enable Linux if you haven't (Settings → Advanced → Developers → Linux
development environment), then in that terminal:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nano
```

## 2. Get a bot token

1. Message **@BotFather** on Telegram
2. Send `/newbot`, follow the prompts
3. Save the token it gives you (looks like `123456:ABC-DEF...`)

**Turn on inline mode** (required for the game to work at all):
1. Still in @BotFather: send `/setinline` → pick your bot → type any placeholder text
2. Send `/setinlinefeedback` → pick your bot → choose **Enabled**

Skipping `/setinlinefeedback` is the most common reason taps on the board
silently do nothing — it's what lets the bot find out which message was
actually sent so it can track that game.

## 3. Install and configure

```bash
cd telegram-game-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # paste TELEGRAM_BOT_TOKEN=..., then Ctrl+O, Enter, Ctrl+X
```

Note: if the Files app strips the leading dot when you move `.env.example`
onto your Chromebook's Linux filesystem, it'll show up as `env.example`
instead — check with `ls -a`, and just use whichever name you actually see.

## 4. Run it

```bash
source venv/bin/activate   # if not already active
python bot.py
```

Leave that running, then in Telegram type your bot's username in any chat
to start a game.

## Files

- `bot.py` — commands and Telegram handlers (inline query, chosen result, button taps)
- `tictactoe.py` — pure game logic: win detection, unbeatable AI, board rendering
- `game_store.py` — in-memory tracking of active games (resets on restart)

## Adding more games

`tictactoe.py` is a template for the pattern: pure game logic + a
callback-driven inline keyboard. Connect Four, Rock-Paper-Scissors, and
Hangman all fit the same shape.
