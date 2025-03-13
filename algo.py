from alpaca_sdk import *
from discord import SyncWebhook
load_dotenv()
hook = SyncWebhook.from_url(os.getenv('HOOK'))

def algo(symbol, buy_signal, money):
    # Write the data to a CSV file
    write_data(symbol)

    df = pd.read_csv(f"{symbol}.csv")
    smaLow = df.close.rolling(window=7).mean()
    smaHigh = df.close.rolling(window=21).mean()
    so = StochasticOscillator(df.high, df.low, df.close, window=14).stoch()
    # AverageTrueRange(df.high, df.low, df.close, window=14).average_true_range()
    rsi_value = rsi(df.close, window=14)
    logic_buy = bool(smaLow.iloc[-1] > smaHigh.iloc[-1] and rsi_value.iloc[-1] < 40 and so.iloc[-1] < 30)
    logic_sell = bool(smaLow.iloc[-1] < smaHigh.iloc[-1] and rsi_value.iloc[-1] > 60  and so.iloc[-1] > 70)
    qty = int(money / float(df['close'].iloc[-1]))
    hook.send(f"logic_buy: {logic_buy}, logic_sell: {logic_sell}, buy_signal: {buy_signal}, qty: {qty}")

    if logic_buy and not buy_signal:
        buy_signal = True
        submit_order(symbol, qty, OrderSide.BUY)
        hook.send(f"Buying {qty} shares of {symbol}")
        logging.info(f"Buying {qty} shares of {symbol}")
    elif logic_sell and buy_signal:
        buy_signal = False
        submit_order(symbol, qty, OrderSide.SELL)
        hook.send(f"Selling {qty} shares of {symbol}")
        logging.info(f"Selling {qty} shares of {symbol}")
    
    # write the new buy_signal to the CSV file
    df.iloc[-1, df.columns.get_loc("buy_signal")] =  buy_signal
    df.to_csv(f"{symbol}.csv", index=False) # Update the CSV file with the new buy_signal
