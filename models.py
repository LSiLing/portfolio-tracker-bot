from config import category_threshold_dict
import yfinance as yf
import sqlite3
from dotenv import load_dotenv
import os
from telegram import Bot
load_dotenv()

class Stock:
    def __init__(self, ticker, name, category):
        self.ticker = ticker
        self.name = name
        self.category = category
        self.threshold = self._get_threshold()


    def _get_threshold(self):
        threshold = category_threshold_dict[self.category]
        return threshold

    def _get_price(self):
        stock = yf.Ticker(self.ticker)
        stock_inf = stock.history(period="1d", interval="1h")
        price = stock_inf["Close"]
        return price

class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add(self, stock):
        self.stocks[stock.ticker] = stock
        return self.stocks

    def remove(self, ticker):
        self.stocks.pop(ticker)
        return self.stocks

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("portfolio.db")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        stocks_table = """CREATE TABLE IF NOT EXISTS stocks (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        category TEXT
        )"""
        alerts_table = """CREATE TABLE IF NOT EXISTS alerts_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                date TEXT,
                price_change INTEGER
                )"""
        self.cursor.execute(stocks_table)
        self.cursor.execute(alerts_table)
        self.conn.commit()

    def load_stocks(self):
        query = "SELECT * FROM stocks"
        self.cursor.execute(query)
        stocks = self.cursor.fetchall()
        return stocks

    def remove_stock(self, ticker):
        query = "DELETE FROM stocks WHERE ticker = ?"
        self.cursor.execute(query, (ticker,))
        self.conn.commit()

    def add_stock(self, stock):
        query = "INSERT INTO stocks (ticker, name, category) VALUES (?, ?, ?)"
        self.cursor.execute(query, (stock.ticker, stock.name, stock.category))
        self.conn.commit()

    def save_to_history(self, ticker, date, price_change):
        query = "INSERT INTO alerts_history (ticker, date, price_change) VALUES (?, ?, ?)"
        self.cursor.execute(query, (ticker, date, price_change))
        self.conn.commit()

class Alert:
    def __init__(self, portfolio):
        self.portfolio = portfolio


    def _check_price_change(self):
        change_dict = {}
        for stock in self.portfolio.stocks.values():
            prices = stock._get_price()
            pct_change =(prices.iloc[-1] - prices.iloc[0])/ prices.iloc[0] * 100
            change_dict[stock.ticker] = pct_change
        return change_dict

    async def _compare_price_thres(self):
        p_change_dict = self._check_price_change()
        for ticker in p_change_dict.keys():
            if p_change_dict[ticker] > self.portfolio.stocks[ticker].threshold:
                await self._send_alert(ticker, p_change_dict[ticker])

    async def _send_alert(self, ticker, pct_change):
        token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        text = f"{ticker} price change: {pct_change:.2f}%"
        async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=text)

class Tracker_bot:
    def __init__(self, portfolio, db):
        self.portfolio = portfolio
        self.db = db

    def _add_stock(self, ticker, name, category):
        stock = Stock(ticker, name, category)
        self.portfolio.add(stock)
        self.db.add_stock(stock)

    def _remove_stock(self, ticker):
        self.portfolio.remove(ticker)
        self.db.remove_stock(ticker)

    def _get_portfolio(self):
        stock_list = []
        for ticker in self.portfolio.stocks:
            stock_list.append(self.portfolio.stocks[ticker].name)
        return stock_list

    async def handle_add(self, update, context):
        ticker = context.args[0]
        name = context.args[1]
        category = context.args[2]
        self._add_stock(ticker, name, category)

        await update.message.reply_text("done")

    async def handle_remove(self, update, context):
        ticker = context.args[0]
        self._remove_stock(ticker)
        await update.message.reply_text("done")

    async def handle_portfolio(self, update, context):
        stock_list = self._get_portfolio()
        text = "\n".join(stock_list)
        await update.message.reply_text(text)


