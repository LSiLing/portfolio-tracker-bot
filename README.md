# Portfolio Tracker Bot 🤖

A Telegram bot for tracking a personal stock and crypto portfolio with automated price change alerts.

## Features

- Track stocks and crypto (via yfinance)
- Automated price change alerts 3x daily via Telegram
- Add and remove assets through bot commands
- SQLite database for persistent storage
- Alert history logging

## Tech Stack

- `yfinance` — market data
- `python-telegram-bot` — Telegram bot integration
- `APScheduler` — scheduled price checks
- `SQLite` — persistent storage
- `python-dotenv` — secure token management

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root:
   ```
   TELEGRAM_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```
4. Run the bot:
   ```
   python main.py
   ```

## Bot Commands

| Command | Description |
|---|---|
| `/add TICKER NAME CATEGORY` | Add asset to portfolio (category: high/medium/low) |
| `/remove TICKER` | Remove asset from portfolio |
| `/portfolio` | Show current portfolio |

Example: `/add BTC-USD Bitcoin high`

## Alert Thresholds

Alerts are triggered when daily price change exceeds the threshold for the asset's category:

| Category | Threshold |
|---|-----------|
| high | 10%       |
| medium | 6%        |
| low | 5%        |

Checks run at 9:30, 16:00, and 22:00 (Warsaw time).

## Project Structure

```
portfolio_tracker/
├── main.py          # Entry point, scheduler, bot setup
├── models.py        # OOP classes: Stock, Portfolio, DatabaseManager, Alert, Tracker_bot
├── config.py        # Thresholds configuration
├── .env             # Secret tokens (not committed)
├── .gitignore
└── requirements.txt
```

## What I Learned

This was my largest Python project to date, combining multiple new technologies into one working application.

Working with multiple classes simultaneously was the biggest challenge — keeping track of which class is responsible for what, and how objects communicate with each other. OOP separation of concerns became much clearer through practice rather than theory.

New skills acquired: Telegram bot setup and command handling, APScheduler for task scheduling, async/await patterns for network operations, and `.env`/dotenv security patterns for token management. SQL knowledge from previous projects (P7) was also refreshed and applied.

## Future Development

- Timezone-aware alerts (different market hours)
- Asset type differentiation (stocks vs crypto vs ETFs)
- 24/7 deployment on a cloud server 
- Volume-based alerts in addition to price change
- Weekly portfolio summary report