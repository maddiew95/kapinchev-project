from alpaca_sdk import *

logging

# Define timezones
us_eastern = tz.gettz('US/Eastern')
australia_eastern = tz.gettz('Australia/Sydney')
buy_signal = False
stock_data("BNGO", dt.now().date(), 10)

# Set up logging
logging.basicConfig(filename='market_close_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

while True:
    # Convert next_close to local time (Australia)
    next_close_aus = next_close().astimezone(australia_eastern)

    # Get the current time in Australia
    current_time_aus = dt.now(tz=australia_eastern)

    # Calculate the time difference between the next close time and the current time
    time_diff = (next_close_aus - current_time_aus).total_seconds()

    # check every 15 minutes if time_diff is greater than 15 minutes, if not, ready to trade
    if time_diff > 60 * 15 :
        logging.info(f"Time difference between next close and current time: {time_diff} seconds")
        logging.info("Not yet time to trade")
        time.sleep(60 * 15)
        
    else: 
        time.sleep(time_diff + 60 * 3)

        # Log the actual close time
        actual_close_time_nyc = dt.now(tz=us_eastern)
        actual_close_time_aus = actual_close_time_nyc.astimezone(australia_eastern)
        logging.info(f"Actual close time in NYC: {actual_close_time_nyc}")
        logging.info(f"Actual close time in Australia Eastern: {actual_close_time_aus}")

        # Algorithm starts here
        logging.info("Algorithm execution started")

        # TODO: will use the list, and money to split each investment money into equal parts
        symbols = []
        money = buy_power() // len(symbols)

        # Write the data to a CSV file
        with open("bngo.csv", "a") as f:
            f.write(f"{dt.now(tz=ny_eastern)}, ,{new_data('bngo')}, , \n")


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

        logging.info("Code execution completed")

        # Sleep for a while before the next iteration (e.g., 1 hour)
        break