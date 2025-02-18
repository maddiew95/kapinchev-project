#TODO: make a function to execute
# df1 = pd.read_csv("BNGO.csv")

# smaLow1 = df1.close.rolling(window=7).mean()
# smaHigh1 = df1.close.rolling(window=21).mean()
# so1 = StochasticOscillator(df1.high, df1.low, df1.close, window=14).stoch()
# AverageTrueRange(df.high, df.low, df.close, window=14).average_true_range()
# rsi1 = rsi(df1.close, window=14)
# logic_buy_1 = smaLow1[-1] > smaHigh1[-1] and rsi1[-1] < 40 and so1 < 30
# logic_sell_1 = smaLow1[-1] < smaHigh1[-1] and rsi1[-1] > 60  and so1[-1] > 70
# qty = buy_power() // float(df['close'].iloc[-1])

# if logic_buy_1 and not buy_signal:
#     buy_signal = True
#     submit_order(symbol, qty, OrderSide.BUY)
#     logging.info(f"Buying {qty} shares of {symbol}")
# elif logic_sell_1 and buy_signal:
#     buy_signal = False
#     submit_order(symbol, qty, OrderSide.SELL)
#     logging.info(f"Selling {qty} shares of {symbol}")
