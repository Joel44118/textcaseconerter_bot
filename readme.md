# Telegram Text Case Converter Bot

Send any text, tap a button, get it converted — UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, kebab-case, CONSTANT_CASE, aLtErNaTiNg.

## How it works
1. Send `/start`
2. Send any text message
3. Tap a case button — result appears instantly
4. Keep tapping other buttons on the same result to try different cases for the same text

## Deploy on Render

1. **Get a bot token** from **@BotFather** on Telegram.
2. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Text case converter bot"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
3. **Create the Render Web Service**:
   - New → Web Service → connect the repo (should auto-detect `render.yaml`)
   - If not auto-detected, set manually: Build Command `pip install -r requirements.txt`, Start Command `python bot.py`
4. **Set environment variables in the Render dashboard** (Environment tab — do this manually, `render.yaml` only applies env vars on first creation):
   - `BOT_TOKEN` = your token from BotFather
   - `PYTHON_VERSION` = `3.11.9`
5. Deploy. `RENDER_EXTERNAL_URL` and `PORT` are supplied automatically by Render — the bot uses them to self-register its webhook, no manual setup needed.

Python is pinned to 3.11 because `python-telegram-bot` 21.6 isn't compatible with Python 3.14's stricter asyncio event-loop handling.
