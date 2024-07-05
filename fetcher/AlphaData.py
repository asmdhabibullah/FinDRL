import os
import requests
import pandas as pd
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AlphaDataFetcher:

    def get_intraday_data(symbol, interval, month, api_key, outputsize='full'):
        # Construct the API URL

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize={outputsize}&apikey={api_key}"
        # url = "https://www.alphavantage.co/query"
        # params = {
        #     'function': 'TIME_SERIES_INTRADAY',
        #     'symbol': symbol,
        #     'interval': interval,
        #     'month': month,
        #     'apikey': api_key,
        #     'outputsize': outputsize
        # }
        response = requests.get(url)
        data = response.json()
        
        if 'Time Series (' + interval + ')' in data:
            return data['Time Series (' + interval + ')']
        else:
            print(f"Error: {data}")  # Print the raw response for debugging
            raise ValueError("Unexpected response format or no data available")

    def process_data(data, month):
        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        # Filter data by month
        df = df[df.index.to_period('M') == pd.Period(month)]
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        df = df.astype(float)
        return df

    def save_to_csv(provider, df, symbol, interval, timespan, start_month, end_month):
        # Create the 'data' directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            # Create the 'data' directory if it doesn't exist
        
        if not os.path.exists(provider):
            os.makedirs(provider)
            # Create the 'data' directory if it doesn't exist
    
        # Create timespan directories if they don't exist
        timespan_path = os.path.join('data', provider, timespan)
        if not os.path.exists(timespan_path):
            os.makedirs(timespan_path)
        # Define the filename based on the symbol, date range, and interval
        number_only = '1' if ''.join(filter(str.isdigit, interval)) == '60' else ''.join(filter(str.isdigit, interval))
        filename = f"{timespan_path}/{symbol}_{start_month}_to_{end_month}_{number_only}.csv"
        
        # Save the DataFrame to a CSV file
        df.to_csv(filename)
        print(f"Data saved to {filename}")
        
        # Save the DataFrame to a CSV file
        df.to_csv(filename)
        print(f"Data saved to {filename}")


def create_month_range(start_month, end_month):
    # Generate a range of months between start_month and end_month
    month_range = pd.date_range(start=start_month, end=end_month, freq='MS').tolist()
    # Convert each Timestamp to string in 'YYYY-MM' format
    month_range_str = [date.strftime('%Y-%m') for date in month_range]
    return month_range_str

symbol = "SPY"
provider = "ALPHA"
start_month = "2020-01"
end_month = "2024-06"

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

# intervals_timespans =[
#     {'interval': '1min', 'timespan': 'minute'},
#     {'interval': '5min', 'timespan': 'minute'},
#     {'interval': '15min', 'timespan': 'minute'},
#     {'interval': '30min', 'timespan': 'minute'},
#     {'interval': '60min', 'timespan': 'hour'},
# ]

month_range_array = create_month_range(start_month, end_month)

def main():
    try:
        print("month_range_array", month_range_array)

        for  month in month_range_array:
            request_count = 0
            total_requests = len(month_range_array)
            for index, item in enumerate(intervals_timespans):
                interval = item['interval']
                timespan = item['timespan']
                data = get_intraday_data(symbol, interval, month, API_KEY)
                df = process_data(data, month)
                print(f"First few rows of data for {symbol} at {interval} interval for {month}:")
                print(df.head())
                save_to_csv(provider, df, symbol, interval, timespan, start_month=f"{month}-01", end_month=f"{month}-30") # provider, df, symbol, interval, timespan, start_month, end_month

                request_count += 1
                if request_count % 5 == 0 and index < total_requests - 1:
                    print("Waiting for 1/2 minute to avoid API rate limits...")
                    sleep(30)  # Wait for 1/2 minute
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


# import os
# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Define the directory to save data
# data_directory = "data"

# # Ensure the data directory exists
# if not os.path.exists(data_directory):
#     os.makedirs(data_directory)

# alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# def fetch_historical_data(symbol, api_key, interval, outputsize='full'):
#     base_url = 'https://www.alphavantage.co/query'
#     params = {
#         'function': 'TIME_SERIES_INTRADAY',
#         'symbol': symbol,
#         'interval': interval,
#         'apikey': api_key,
#         'outputsize': outputsize
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()
#     if f'Time Series ({interval})' in data:
#         timeseries = data[f'Time Series ({interval})']
#         df = pd.DataFrame.from_dict(timeseries, orient='index')
#         df.columns = ['open', 'high', 'low', 'close', 'volume']
#         df.index = pd.to_datetime(df.index)
#         df.sort_index(inplace=True)
#         return df
#     else:
#         print(f"Error fetching data for {symbol} at interval {interval}")
#         return pd.DataFrame()

# def fetch_data(symbol, start_date, end_date):
#     intervals = ['1min', '5min', '15min', '30min', '60min']

#     try:
#         all_data = []

#         # Calculate the date range
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
#         delta = end_date - start_date

#         for i in range(delta.days + 1):
#             current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
#             print(f"Fetching data for {symbol} on {current_date}...")

#             for interval in intervals:
#                 print(f"Fetching historical data with interval {interval}...")
#                 historical_data = fetch_historical_data(symbol, alpha_vantage_key, interval)
#                 historical_data['interval'] = interval
#                 # Save historical data for the current interval to a CSV file
#                 historical_data.to_csv(os.path.join(data_directory, f"{symbol}_historical_data_{interval}.csv"), mode='a', index=False)
#                 all_data.append(historical_data)

#         print("Data has been saved to CSV files.")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage:
# fetch_data('SPY', '2023-01-01', '2023-01-05')
