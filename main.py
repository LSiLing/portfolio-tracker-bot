from models import Stock, Portfolio, DatabaseManager, Alert, Tracker_bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()
db = DatabaseManager()
portfolio = Portfolio()

stocks_tuples = db.load_stocks()

for i in stocks_tuples:
    ticker = i[0]
    name = i[1]
    category = i[2]
    stock = Stock(ticker, name, category)
    portfolio.add(stock)

bot = Tracker_bot(portfolio, db)
alert = Alert(portfolio)

function = alert._compare_price_thres

scheduler = AsyncIOScheduler()
scheduler.add_job(function, 'cron', hour=9, minute=30)
scheduler.add_job(function, 'cron', hour=16, minute=00)
scheduler.add_job(function, 'cron', hour=22, minute=00)

token = os.getenv("TELEGRAM_TOKEN")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("add", bot.handle_add))
app.add_handler(CommandHandler("remove", bot.handle_remove))
app.add_handler(CommandHandler("portfolio", bot.handle_portfolio))
async def on_startup(app):
    scheduler.start()

app.post_init = on_startup

app.run_polling()


