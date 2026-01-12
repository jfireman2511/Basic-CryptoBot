import requests
import pandas as pd
import numpy as np
import time

# Define your CoinAPI.io API key
API_KEY = 

# Define the CoinAPI.io base URL for historical data
BASE_URL = 'https://rest.coinapi.io/v1/ohlcv'

# Define your trading parameters
symbols = ['BTC-USD', 'ETH-USD']
timeframe = '1HRS'
lookback_period = 50
buy_trigger_percentage = 0.02
sell_trigger_percentage = -0.01

# Function to fetch historical data from CoinAPI.io
def get_historical_data(symbol, interval, limit):
    url = f"{BASE_URL}/{symbol}/history?period_id={interval}&time_start=2020-01-01T00:00:00"
    headers = {'X-CoinAPI-Key': API_KEY}
    params = {'limit': limit}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code == 200:
        df = pd.DataFrame(data)
        df['time_period_start'] = pd.to_datetime(df['time_period_start'])
        df.set_index('time_period_start', inplace=True)
        return df
    else:
        print("Error fetching data:", data)
        return None

# Function to implement the swing trading strategy
def swing_trading_strategy(data, symbol):
    data['Returns'] = data['price_close'].pct_change()
    data['Buy Trigger'] = buy_trigger_percentage
    data['Sell Trigger'] = sell_trigger_percentage
    data['Signal'] = 0

    for i in range(lookback_period, len(data)):
        if data['price_close'][i] > data['price_close'][i - lookback_period] * (1 + buy_trigger_percentage):
            data['Signal'][i] = 1  # Buy signal
        elif data['price_close'][i] < data['price_close'][i - lookback_period] * (1 + sell_trigger_percentage):
            data['Signal'][i] = -1  # Sell signal

    return data

# Create dictionaries to store file handlers for buy and sell signals for each symbol
buy_file_handlers = {symbol: open(f"{symbol}_buy_orders.txt", "a") for symbol in symbols}
sell_file_handlers = {symbol: open(f"{symbol}_sell_orders.txt", "a") for symbol in symbols}

# Main trading loop
while True:
    for symbol in symbols:
        historical_data = get_historical_data(symbol, timeframe, lookback_period)
        
        if historical_data is None:
            continue
        
        signals = swing_trading_strategy(historical_data, symbol)
        
        latest_signal = signals['Signal'].iloc[-1]
        
        if latest_signal == 1:
            print(f"Buy {symbol}")
            # Write the buy signal to the buy text file
            buy_file_handlers[symbol].write(f"Buy {symbol}\n")
        elif latest_signal == -1:
            print(f"Sell {symbol}")
            # Write the sell signal to the sell text file
            sell_file_handlers[symbol].write(f"Sell {symbol}\n")
    
    # Sleep for a while before the next iteration
    time.sleep(3600)  # Sleep for 1 hour before checking again
