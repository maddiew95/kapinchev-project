import os, pandas as pd, time, logging, numpy as np
from ta.volatility import AverageTrueRange
from ta.momentum import StochasticOscillator, rsi
from dateutil import tz
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt, timedelta
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient
from alpaca.data import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


load_dotenv()

key = os.getenv('API_KEY')
secret = os.getenv('API_SECRET')
ny_eastern = tz.gettz('US/Eastern')
stock_client = StockHistoricalDataClient(key, secret)

account_client = TradingClient(key, secret)

# To get the current buying power of the account
def buy_power():
    account = account_client.get_account()
    return account.buying_power

# To get historical data up till whenever "today" is from a certain number of years ago (e.g. 5 years ago) NOTE: Alpaca only allows 8 years of data
def stock_data(symbol, today, years_ago):
    params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=(today - relativedelta(years=years_ago)).strftime('%Y-%m-%d'),
        end=today.strftime('%Y-%m-%d')
        )
    bars =  stock_client.get_stock_bars(params)
    raw = pd.DataFrame(bars.model_dump()["data"][symbol]).drop(columns=["symbol"])
    raw["smaLow"] = raw.close.rolling(window=7).mean()
    raw["smaHigh"] = raw.close.rolling(window=21).mean()
    raw["so"] = StochasticOscillator(raw.high, raw.low, raw.close, window=14).stoch()
    raw["atr"] = AverageTrueRange(raw.high, raw.low, raw.close, window=14).average_true_range()
    raw["rsi"] = rsi(raw.close, window=14)
    return raw

# To get the closing price of the stock for the next trading day
def next_close():
    return account_client.get_clock().next_close

# Use this function to submit an order (buy and sell)
def submit_order(symbol, qty, order_type):
    order_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=order_type,
                        time_in_force=TimeInForce.DAY
                        )
    # Market order
    account_client.submit_order(order_data=order_data)


