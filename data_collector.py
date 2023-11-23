import pandas as pd
import requests
from datetime import datetime

def collect_historical_data(crypto_id, api_key, start_date, end_date):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    params = {
        'fsym': crypto_id,
        'tsym': 'USD',
        'limit': 2000,  # Adjust as necessary
        'toTs': int(end_date.timestamp()),
        'api_key': '3b311037957c48cff5cf685396cfff76952c1afd5c6fa18ba5cc124b0b4c5095'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df['price'] = df['close']  # Closing price as 'price'
        df['open'] = df['open']
        df['high'] = df['high']
        df['low'] = df['low']
        df['volume'] = df['volumeto']
        # Additional fields like market cap can be added if available from the API
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

def append_data_to_csv(new_data, file_name):
    try:
        existing_data = pd.read_csv(file_name)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
        updated_data.to_csv(file_name, index=False)
    except FileNotFoundError:
        new_data.to_csv(file_name, index=False)

if __name__ == "__main__":
    API_KEY = 'your_api_key_here'
    crypto_id = 'BTC'
    start_date = datetime(2012, 1, 1)  # Adjust the start date as needed
    end_date = datetime.now()  # Current date as the end date

    new_data = collect_historical_data(crypto_id, API_KEY, start_date, end_date)
    append_data_to_csv(new_data, 'Data.csv')
