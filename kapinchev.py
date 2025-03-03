from alpaca_sdk import *
from algo import *

logging

# Define timezones
us_eastern = tz.gettz('US/Eastern')
australia_eastern = tz.gettz('Australia/Sydney')
symbol = "BNGO"

stock_data(symbol, dt.now(tz=us_eastern).date(), 10)

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
        logging.info("Trading time approaching within 1 hour")
        time.sleep(time_diff + 60 * 2.5)
        
        # Log the actual close time
        actual_close_time_nyc = dt.now(tz=us_eastern)
        actual_close_time_aus = actual_close_time_nyc.astimezone(australia_eastern)
        logging.info(f"Actual close time in NYC: {actual_close_time_nyc}")
        logging.info(f"Actual close time in Australia Eastern: {actual_close_time_aus}")

        # Algorithm starts here
        logging.info("Algorithm execution started")

        money = round(float(buy_power() / 4), 2)
        buy_signal = bool(pd.read_csv(f"{symbol}.csv")['buy_signal'].iloc[-1])
        # run algo
        algo(symbol, buy_signal, money)

       



        logging.info("Code execution completed")
        
    