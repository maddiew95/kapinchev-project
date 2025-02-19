from alpaca_sdk import *

logging

# Define timezones
us_eastern = tz.gettz('US/Eastern')
australia_eastern = tz.gettz('Australia/Sydney')
buy_signal = False
symbol = "BNGO"
stock_data(symbol, dt.now().date(), 10)

# Set up logging
logging.basicConfig(filename='market_close_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

while True:
    # Convert next_close to local time (Australia)
    next_close_aus = next_close().astimezone(australia_eastern)

    # Get the current time in Australia
    current_time_aus = dt.now(tz=australia_eastern)

    # Calculate the time difference between the next close time and the current time
    time_diff = (next_close_aus - current_time_aus).total_seconds()

    # check every 15 minutes if time_diff is greater than 15 minutes and 60 minutes of trading time, if not, ready to trade
    if(time_diff > 60 * 15 and time_diff > 60 * 60):
        time.sleep(60 * 15)
        
    else: 
        time.sleep(time_diff + 60 * 2.5)
        logging.info("Market is closing, preparing to start the algorithm")
        # Log the actual close time
        actual_close_time_nyc = dt.now(tz=us_eastern)
        actual_close_time_aus = actual_close_time_nyc.astimezone(australia_eastern)
        logging.info(f"Actual close time in NYC: {actual_close_time_nyc}")
        logging.info(f"Actual close time in Australia Eastern: {actual_close_time_aus}")

        # Algorithm starts here
        logging.info("Algorithm execution started")

        # TODO: will use the list, and money to split each investment money into equal parts
        # symbols = []
        # money = buy_power() // len(symbols)

        # Write the data to a CSV file
        write_data(symbol)



        logging.info("Code execution completed")

        # Sleep for a while before the next iteration (e.g., 1 hour)
        break