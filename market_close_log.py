from alpaca_sdk import *

logging

# Define timezones
us_eastern = tz.gettz('US/Eastern')
australia_eastern = tz.gettz('Australia/Sydney')

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

    # Check for daylight savings adjustments and update time_difference
    if us_eastern.utcoffset(current_time_aus) != us_eastern.dst(current_time_aus):
        # US daylight savings change
        logging.info("Daylight savings change detected in US timezone")
        # Recalculate next_close_aus with daylight savings adjustment
        next_close_aus = next_close.astimezone(australia_eastern)
        
    if australia_eastern.utcoffset(current_time_aus) != australia_eastern.dst(current_time_aus):
        # Australia daylight savings change
        logging.info("Daylight savings change detected in Australia timezone")
        # Recalculate next_close_aus with daylight savings adjustment
        next_close_aus = next_close.astimezone(australia_eastern)

    # Calculate the time difference
    time_difference = (next_close_aus - current_time_aus).total_seconds()

    # Calculate the delay (for a few minutes after the close time)
    delay_seconds = time_difference + (5 * 60)  # 5 minutes after the close time

    # # Log the values
    # logging.info(f"Next close time in NYC: {next_close}")
    # logging.info(f"Next close time in Australia Eastern: {next_close_aus}")
    # logging.info(f"Current time in Australia Eastern: {current_time_aus}")
    # logging.info(f"Delay seconds: {delay_seconds}")

    # Ensure delay is positive and avoid missing the next close datetime
    while time_difference > 0:
        # Recalculate current time and time difference
        current_time_aus = dt.now(tz=australia_eastern)
        time_difference = (next_close_aus - current_time_aus).total_seconds()

        # Calculate the delay (for a few minutes after the close time)
        delay_seconds = time_difference + (5 * 60)  # 5 minutes after the close time

        # # Log the values
        # logging.info(f"Next close time in NYC: {next_close}")
        # logging.info(f"Next close time in Australia Eastern: {next_close_aus}")
        # logging.info(f"Current time in Australia Eastern: {current_time_aus}")
        # logging.info(f"Delay seconds: {delay_seconds}")

        # Wait for the delay period
        if delay_seconds > 0:
            time.sleep(min(delay_seconds, 60))  # Sleep for up to 60 seconds to recheck time differences
        else:
            break

    # Log the actual close time
    actual_close_time_nyc = dt.now(tz=us_eastern)
    actual_close_time_aus = actual_close_time_nyc.astimezone(australia_eastern)
    # logging.info(f"Actual close time in NYC: {actual_close_time_nyc}")
    # logging.info(f"Actual close time in Australia Eastern: {actual_close_time_aus}")

    # Execute your code 5 minutes after the market close
    logging.info(f"Executing code a few minutes after the close time @ {dt.now(tz=australia_eastern)} Aussie time, or {dt.now(tz=us_eastern)} NYC time")
    # Add your code here
    # symbol = "AAPL"
    # stock = stock_data(symbol, today, 10)
    # print(stock.iloc[-1])
    # logic_buy = stock['smaLow'].iloc[-1] > stock['smaHigh'].iloc[-1] and stock['rsi'].iloc[-1] < 40 and stock['so'].iloc[-1] < 30
    # logic_sell = stock['smaLow'].iloc[-1] < stock['smaHigh'].iloc[-1] and stock['rsi'].iloc[-1] > 60  and stock['so'].iloc[-1] > 70
    # print(f"Buy: {logic_buy}, Sell: {logic_sell}")
    # qty = buy_power() // stock['close'].iloc[-1]
    # if logic_buy:
    #     submit_order(symbol, qty, OrderSide.BUY)
    #     logging.info(f"Buying {qty} shares of {symbol}")
    # elif logic_sell:
    #     submit_order(symbol, qty, OrderSide.SELL)
    #     logging.info(f"Selling {qty} shares of {symbol}")
    
    logging.info("Code execution completed")

    # Sleep for a while before the next iteration (e.g., 1 hour)
    time.sleep(3600)