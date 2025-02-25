import os, pandas as pd, time, logging, numpy as np, requests as req, bs4 as soup, re
from ta.volatility import AverageTrueRange
from ta.momentum import StochasticOscillator, rsi
from dateutil import tz
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt, timedelta
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
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

# Set paper to True if you want to use the paper trading account
account_client = TradingClient(key, secret, paper=False)

# To get the current buying power of the account
def buy_power():
    account = account_client.get_account()
    return float(account.buying_power)

def new_data(symbol):
    c = "whitespace-nowrap px-0.5 py-[1px] text-left text-smaller font-semibold tiny:text-base xs:px-1 sm:py-2 sm:text-right sm:text-small"
    url = f"https://stockanalysis.com/stocks/{symbol}/"
    close = re.findall("\d+\.\d{2}", soup.BeautifulSoup(req.get(url).text, 'html.parser').find_all('div')[0].text)[0]
    low, high = tuple(soup.BeautifulSoup(req.get(url).text, 'html.parser').findAll('td', class_=c)[12].text.split(' - '))
    return f" , {high}, {low}, {close}"

# To get historical data from a certain number of years ago (e.g. 5 years ago) NOTE: Alpaca only allows 8 years of data
def stock_data(symbol, today, years_ago):
    params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=(today - relativedelta(years=years_ago)).strftime('%Y-%m-%d'),
        end=today.strftime('%Y-%m-%d')
        )
    bars =  stock_client.get_stock_bars(params)
    raw = pd.DataFrame(bars.model_dump()["data"][symbol]).drop(columns=["symbol"])
    raw["buy_signal"] = False
    raw.to_csv(f"{symbol}.csv", index=False)

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

def write_data(symbol):
    with open(f"{symbol}.csv", "a") as f:
        f.write(f"{dt.now(tz=ny_eastern)}, {new_data(symbol)}, , , \n")

