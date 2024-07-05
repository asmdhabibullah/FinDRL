import os
import requests
import pandas as pd
from time import sleep
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_aggregated_data(self, symbol, timespan, interval, from_date, to_date):
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{interval}/{timespan}/{from_date}/{to_date}?adjusted=true&sort=asc&limit=5000&apiKey={self.api_key}"
       
        print(f"Req url: {url}")

        response = requests.get(url)

        data = response.json()
        if 'results' in data:
            return data['results']
        else:
            print(f"Error: {data}")
            raise ValueError("Unexpected response format or no data available")

    def process_data(self, data):
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df.rename(columns={
            'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume', 'n': 'number_of_trades'
        })
        return df

class FileManager:
    def __init__(self, provider):
        self.provider = provider

    def save_to_csv(self, df, symbol, timespan, interval, from_date, to_date):
        if not os.path.exists('data'):
            os.makedirs('data')
        
        provider_path = os.path.join('data', self.provider)
        if not os.path.exists(provider_path):
            os.makedirs(provider_path)

        timespan_path = os.path.join(provider_path, timespan)
        if not os.path.exists(timespan_path):
            os.makedirs(timespan_path)

        filename = f"{timespan_path}/{symbol}_{from_date}_to_{to_date}_{interval}.csv"
        if os.path.exists(filename):
            existing_data = pd.read_csv(filename, index_col=0, parse_dates=True)
            df = pd.concat([existing_data, df])
            df = df[~df.index.duplicated(keep='first')]
        df.to_csv(filename)
        print(f"Data saved to {filename}")
        return timespan_path

class DataAggregator:
    def __init__(self, api_key, symbol, month_array, provider="POLYGON"):
        self.symbol = symbol
        self.api_key = api_key
        self.provider = provider
        self.month_array = month_array
        self.fetcher = DataFetcher(api_key)
        self.file_manager = FileManager(provider)

    def run(self, intervals_timespans):
        request_count = 0

        for interval_timespan in intervals_timespans:
            interval = interval_timespan['interval']
            timespan = interval_timespan['timespan']

            for start_day in self.month_array:
                try:
                    from_date = f"{start_day}-01"
                    to_date = f"{start_day}-30"

                    # print(f"Calling for the day month of: {from_date} to {to_date} ")

                    data = self.fetcher.get_aggregated_data(self.symbol, timespan, interval, from_date, to_date)
                    df = self.fetcher.process_data(data)
                    print(f"For interval {interval} - {timespan}: data downloded successfully!")
                    # print(df.head())
                    main_save_pata = self.file_manager.save_to_csv(df, self.symbol, timespan, interval, from_date, to_date)
                    
                    request_count += 1

                    if len(self.month_array) != 0 and request_count % 4 == 0:
                        print("Waiting for 1 minute to avoid API rate limits...")
                        request_count = 0
                        sleep(61)  # Wait for 1.1 minute
                    print(f"Copy path to analysis data: {main_save_pata}")
                except Exception as e:
                    print(f"An error occurred: {e}")



# import os
# import requests
# import pandas as pd
# from time import sleep
# from datetime import datetime
# from dotenv import load_dotenv
# from utils import total_months_month_array
# # Load environment variables
# load_dotenv()

# def get_aggregated_data(symbol, from_date, to_date, timespan, interval, api_key):
#     url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{timespan}/{interval}/{from_date}/{to_date}"
#     # /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}
#     params = {
#         'sort': 'asc',
#         'adjusted': 'true',
#         'limit': 50000,
#         'apiKey': api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if 'results' in data:
#         return data['results']
#     else:
#         print(f"Error: {data}")  # Print the raw response for debugging
#         raise ValueError("Unexpected response format or no data available")

# def process_data(data):
#     df = pd.DataFrame(data)
#     df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
#     df.set_index('timestamp', inplace=True)
#     df = df.rename(columns={
#         'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume', 'n': 'number_of_trades'
#     })
#     return df

# def save_to_csv(df, provider, symbol, from_date, to_date, interval, timespan):
#     # Create the 'data' directory if it doesn't exist
#     if not os.path.exists('data'):
#         os.makedirs('data')
#         # Create the 'data' directory if it doesn't exist
    
#     if not os.path.exists(provider):
#         os.makedirs(provider)
#         # Create the 'data' directory if it doesn't exist

#     # Create timespan directories if they don't exist
#     timespan_path = os.path.join('data', provider, timespan)
#     if not os.path.exists(timespan_path):
#         os.makedirs(timespan_path)
#     # Define the filename based on the symbol, date range, and interval
#     filename = f"{timespan_path}/{symbol}_{from_date}_to_{to_date}_{interval}.csv"
    
#     # Save the DataFrame to a CSV file
#     df.to_csv(filename)
#     print(f"Data saved to {filename}")


# provider = "POLYGON"
# symbol = "SPY"
# from_date = "2023-01-01"  # Start date
# to_date = "2023-12-30"  # End date

# total_months, month_array = total_months_month_array(from_date, to_date)

# API_KEY = os.getenv('POLYGON_API_KEY')
# intervals_timespans =[
#     # For day intervals
#     {'interval': 1, 'timespan': 'day'},
#     # {'interval': 5, 'timespan': 'day'},
#     # {'interval': 10, 'timespan': 'day'},
#     # {'interval': 15, 'timespan': 'day'},
#     # {'interval': 30, 'timespan': 'day'},
#     # For hours intervals
#     {'interval': 1, 'timespan': 'hour'},
#     # {'interval': 5, 'timespan': 'hour'},
#     # {'interval': 10, 'timespan': 'hour'},
#     # {'interval': 15, 'timespan': 'hour'},
#     # {'interval': 30, 'timespan': 'hour'},
#     # For minutes intervals
#     {'interval': 1, 'timespan': 'minute'},
#     # {'interval': 5, 'timespan': 'minute'},
#     # {'interval': 10, 'timespan': 'minute'},
#     {'interval': 15, 'timespan': 'minute'},
#     {'interval': 30, 'timespan': 'minute'},
# ]

# def main():
#     try:
#         request_count = 0
#         total_requests = 5
#         for index, start_day in enumerate(month_array):
#             interval = 1
#             timespan = "minute"
#             data = get_aggregated_data(symbol, from_date=f"{start_day}-1", to_date=f"{start_day}-30", interval=interval, timespan=timespan, api_key=API_KEY)
#             df = process_data(data)
#             print(f"First few rows of data for interval {interval} {timespan}:")
#             print(df.head())
#             save_to_csv(df, symbol, from_date, to_date, interval, timespan)
            
#             request_count += 1
#             total_requests += 1

#             if request_count % 5 == 0:
#                 print("Waiting for 1 minute to avoid API rate limits...")
#                 sleep(60)  # Wait for 1 minute
#                 request_count = 0

#             print("total_requests", total_requests)
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

# import os
# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# def get_aggregated_data(symbol, from_date, to_date, interval, api_key):
#     url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{interval}/{from_date}/{to_date}"
#     params = {
#         'adjusted': 'true',
#         'sort': 'asc',
#         'limit': 50000,
#         'apiKey': api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if 'results' in data:
#         return data['results']
#     else:
#         print(f"Error: {data}")  # Print the raw response for debugging
#         raise ValueError("Unexpected response format or no data available")

# def process_and_resample_data(data):
#     df = pd.DataFrame(data)
#     df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
#     df.set_index('timestamp', inplace=True)
    
#     resampled = df.resample(interval).agg({
#         'o': 'first',
#         'h': 'max',
#         'l': 'min',
#         'c': 'last',
#         'v': 'sum',
#         'n': 'sum'
#     })
    
#     resampled.columns = [
#         'open', 'high', 'low', 'close', 'volume', 'number_of_trades'
#     ]
#     return resampled

# def save_to_csv(df, symbol, from_date, to_date):
#     # Create the 'data' directory if it doesn't exist
#     if not os.path.exists('data'):
#         os.makedirs('data')
    
#     # Define the filename based on the symbol and date range
#     filename = f"data/{symbol}_{from_date}_to_{to_date}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    
#     # Save the DataFrame to a CSV file
#     df.to_csv(filename)
#     print(f"Data saved to {filename}")

# def main():
#     try:
#         data = get_aggregated_data(symbol, from_date, to_date, interval, API_KEY)
#         df = pd.DataFrame(data)
#         df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
#         df.set_index('timestamp', inplace=True)
#         df = df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume', 'n': 'number_of_trades'})
#         print(df.head())
#         save_to_csv(df, symbol, from_date, to_date)
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()


# def main():
#     try:
#         tick_data = get_tick_data(symbol, date, API_KEY)
#         aggregated_df = process_and_resample_data(tick_data, interval)
#         print(aggregated_df.head())
#         save_to_csv(aggregated_df, symbol, date)
#     except Exception as e:
#         print(f"An error occurred: {e}")
# def get_tick_data(symbol, date, api_key):
#     url = f"https://api.polygon.io/v2/ticks/stocks/trades/{symbol}/{date}"
#     params = {
#         'apiKey': api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if 'results' in data:
#         return data['results']
#     else:
#         print(f"Error: {data}")  # Print the raw response for debugging
#         raise ValueError("Unexpected response format or no data available")

# def process_and_resample_data(tick_data, interval):
#     df = pd.DataFrame(tick_data)
#     df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
#     df.set_index('timestamp', inplace=True)
    
#     resampled = df.resample(interval).apply({
#         'p': 'ohlc',
#         's': 'sum',
#         'x': 'first',
#         'c': 'first',
#         'i': 'first',
#         'z': 'first',
#         'trf': 'first',
#         'pt': 'first',
#         'rft': 'first'
#     })
    
#     resampled.columns = [
#         'open', 'high', 'low', 'close', 'volume', 'exchange', 
#         'conditions', 'trade_id', 'sequence', 'trade_report_id',
#         'participant_timestamp', 'reporting_facility_timestamp'
#     ]
#     return resampled

# def save_to_csv(df, symbol, date):
#     # Create the 'data' directory if it doesn't exist
#     if not os.path.exists('data'):
#         os.makedirs('data')
    
#     # Define the filename based on the symbol and current date and time
#     filename = f"data/{symbol}_{date}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    
#     # Save the DataFrame to a CSV file
#     df.to_csv(filename)
#     print(f"Data saved to {filename}")

# def main():
#     try:
#         tick_data = get_tick_data(symbol, date, API_KEY)
#         aggregated_df = process_and_resample_data(tick_data, interval)
#         print(aggregated_df.head())
#         save_to_csv(aggregated_df, symbol, date)
#     except Exception as e:
#         print(f"An error occurred: {e}")


# def get_tick_data(symbol, date, api_key):
#     url = f"https://api.polygon.io/v2/ticks/stocks/trades/{symbol}/{date}"
#     params = {
#         'apiKey': api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if 'results' in data:
#         return data['results']
#     else:
#         raise ValueError("Unexpected response format or no data available")

# def process_and_resample_data(tick_data, interval):
#     df = pd.DataFrame(tick_data)
#     df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
#     df.set_index('timestamp', inplace=True)
    
#     resampled = df.resample(interval).apply({
#         'p': 'ohlc',
#         's': 'sum',
#         'x': 'first',
#         'c': 'first',
#         'i': 'first',
#         'z': 'first',
#         'trf': 'first',
#         'pt': 'first',
#         'rft': 'first'
#     })
    
#     resampled.columns = [
#         'open', 'high', 'low', 'close', 'volume', 'exchange', 
#         'conditions', 'trade_id', 'sequence', 'trade_report_id',
#         'participant_timestamp', 'reporting_facility_timestamp'
#     ]
#     return resampled

# def save_to_csv(df, symbol, date):
#     # Create the 'data' directory if it doesn't exist
#     if not os.path.exists('data'):
#         os.makedirs('data')
    
#     # Define the filename based on the symbol and current date and time
#     filename = f"data/{symbol}_{date}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    
#     # Save the DataFrame to a CSV file
#     df.to_csv(filename)
#     print(f"Data saved to {filename}")



# def main():
#     data = get_tick_data(symbol, interval, API_KEY)
#     df = process_and_resample_data(data, interval)
#     print(df.head())
#     save_to_csv(df, symbol, date)

# def fetch_tick_data(symbol, api_key, date):
#     url = f"https://api.polygon.io/v2/ticks/stocks/trades/{symbol}/{date}?apiKey={api_key}"
#     response = requests.get(url)
#     data = response.json()

#     if 'results' in data:
#         return pd.DataFrame(data['results'])
#     else:
#         print(f"Error fetching tick data: {data}")
#         return pd.DataFrame()

# def analyze_trade_data(tick_data, intervals):
#     tick_data['timestamp'] = pd.to_datetime(tick_data['t'], unit='ms')
#     tick_data.set_index('timestamp', inplace=True)

#     summary_data = []

#     for interval in intervals:
#         resampled = tick_data.resample(interval).apply({
#             'p': 'ohlc',
#             's': 'sum',
#             'x': 'first',
#             'c': 'first',
#             'i': 'first',
#             'z': 'first',
#             'trf': 'first',
#             'pt': 'first',
#             'rft': 'first'
#         })
#         resampled.columns = [
#             'open', 'high', 'low', 'close', 'volume', 'exchange', 
#             'conditions', 'trade_id', 'sequence', 'trade_report_id',
#             'participant_timestamp', 'reporting_facility_timestamp'
#         ]
#         summary_data.append(resampled)

#     return pd.concat(summary_data)

# def fetch_data(symbol, start_date, end_date):
#     polygon_key = os.getenv('POLYGON_API_KEY')
#     intervals = ['1s', '15s', '30s', '1min', '5min', '15min']

#     try:
#         all_summary_data = []
#         all_trade_details = []

#         # Calculate the date range
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
#         delta = end_date - start_date

#         for i in range(delta.days + 1):
#             current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
#             print(f"Fetching tick data for {symbol} on {current_date}...")

#             tick_data = fetch_tick_data(symbol, polygon_key, current_date)
#             if not tick_data.empty:
#                 tick_data.to_csv(f"./data/{symbol}_tick_data_{current_date}.csv", index=False)
#                 all_trade_details.append(tick_data)

#                 print(f"Analyzing trade data for {symbol} on {current_date}...")
#                 summary_data = analyze_trade_data(tick_data, intervals)
#                 summary_data.to_csv(f"./data/{symbol}_trade_summary_{current_date}.csv", index=True)
#                 all_summary_data.append(summary_data)

#         if all_summary_data:
#             combined_summary_data = pd.concat(all_summary_data)
#             combined_summary_data.to_csv(f"./data/{symbol}_trade_summary_{start_date}_to_{end_date}.csv", index=True)

#         if all_trade_details:
#             combined_trade_details = pd.concat(all_trade_details)
#             combined_trade_details.to_csv(f"./data/{symbol}_tick_data_{start_date}_to_{end_date}.csv", index=False)

#         print("Data has been saved to CSV files.")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage:
# fetch_data('SPY', '2023-01-01', '2023-01-05') #SPX, $SPX
