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
    today = dt.now().date()

    # Get the next close datetime from the SDK
    next_close = account_client.get_clock().next_close  # Assuming this returns a timezone-aware datetime

    # Convert next_close to local time (Australia)
    next_close_aus = next_close.astimezone(australia_eastern)

    # Get the current time in Australia
    current_time_aus = dt.now(tz=australia_eastern)

    # Loop to keep track of the close time and refresh every hour
    while True:
        # Get the current time in Australia
        current_time_aus = dt.now(tz=australia_eastern)

        # Calculate the time difference
        time_difference = (next_close_aus - current_time_aus).total_seconds()

        # Break the loop if the close time has passed
        if time_difference <= 0:
            break

        # Calculate the delay (for a few minutes after the close time)
        delay_seconds = time_difference + (5 * 60)  # 5 minutes after the close time

        # Ensure delay is positive and avoid missing the next close datetime
        delay_seconds = max(delay_seconds, 0)

        # Wait for the delay period or recheck the time every hour
        time.sleep(min(delay_seconds, 3600))  # Sleep for up to 1 hour to recheck time differences

        # Refresh the next close time and timezone
        next_close = account_client.get_clock().next_close
        next_close_aus = next_close.astimezone(australia_eastern)

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
    time.sleep(3600)