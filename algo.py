from alpaca_sdk import *

def algo(symbol, buy_signal, money):
    df = pd.read_csv(f"{symbol}.csv")
    smaLow = df.close.rolling(window=7).mean()
    smaHigh = df.close.rolling(window=21).mean()
    so = StochasticOscillator(df.high, df.low, df.close, window=14).stoch()
    # AverageTrueRange(df.high, df.low, df.close, window=14).average_true_range()
    rsi = rsi(df.close, window=14)
    logic_buy = smaLow[-1] > smaHigh[-1] and rsi[-1] < 40 and so < 30
    logic_sell = smaLow[-1] < smaHigh[-1] and rsi[-1] > 60  and so[-1] > 70
    qty = int(money / float(df['close'].iloc[-1]))

    if logic_buy and not buy_signal:
        buy_signal = True
        submit_order(symbol, qty, OrderSide.BUY)
        logging.info(f"Buying {qty} shares of {symbol}")
    elif logic_sell and buy_signal:
        buy_signal = False
        submit_order(symbol, qty, OrderSide.SELL)
        logging.info(f"Selling {qty} shares of {symbol}")
    
    # write the new buy_signal to the CSV file
    df["buy_signal"].iloc[-1] = buy_signal
