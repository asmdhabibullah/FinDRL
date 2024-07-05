import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.data = {}

    def fetch_data(self, interval):
        print(f"Fetching data for interval: {interval}")
        data = self.fetch_interval_data(interval)
        if data is not None:
            self.data[interval] = data
            self.save_data_to_file(data, interval)

    # def fetch_interval_data(self, interval):
    #     data_frames = []
    #     current_start = self.start_date

    #     print("current_start", current_start.strftime('%Y-%m-%d'))

    #     while current_start < self.end_date:
    #         current_end = min(current_start + timedelta(days=1), self.end_date)

    #         print("current_end", current_end.strftime('%Y-%m-%d'))

    #         data = yf.download(tickers=self.symbol, start=current_start.strftime('%Y-%m-%d'), end=current_end.strftime('%Y-%m-%d'), period="1d", interval=interval)

    #         if not data.empty:
    #             data_frames.append(data)
    #         current_start = current_end

    #     if data_frames:
    #         return pd.concat(data_frames)
    #     else:
    #         print(f"No data fetched for interval: {interval}")
    #         return None
        
    def fetch_interval_data(self,interval='1m'):
        data_frames = []
        current_start = self.start_date

        while current_start < self.end_date:
            current_end = min(current_start + timedelta(days=7), self.end_date)  # Fetch in 7-day chunks

            try:
                data = yf.download(
                    tickers=self.symbol,
                    start=current_start.strftime('%Y-%m-%d'),
                    end=current_end.strftime('%Y-%m-%d'),
                    interval=interval
                )

                if not data.empty:
                    data_frames.append(data)
                    print(f"Fetched data from {current_start} to {current_end}")

            except Exception as e:
                print(f"Failed to fetch data from {current_start} to {current_end}: {e}")

            current_start = current_end

        if data_frames:
            self.df = pd.concat(data_frames)
            return self.df
        else:
            print(f"No data fetched for interval: {interval}")
            return None


    def save_data_to_file(self, data, interval):
        directory = './data/YAHOO'
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{directory}/{self.symbol}_{self.start_date.strftime('%Y-%m-%d')}_{self.end_date.strftime('%Y-%m-%d')}_{interval}.csv"

        if os.path.exists(filename):
            existing_data = pd.read_csv(filename, index_col=0, parse_dates=True)
            data = pd.concat([existing_data, data])
            data = data[~data.index.duplicated(keep='first')]
        data.to_csv(filename)
        print(f"Data saved to {filename}")
