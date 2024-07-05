import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

def total_months_month_array(from_date, to_date):
    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    total_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    month_array = []
    current_date = start_date

    while current_date <= end_date:
        month_array.append(current_date.strftime("%Y-%m"))
        current_date += relativedelta(months=1)

    return total_months, month_array

def combine_csv_files_data(input_directory, output_file):

    all_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.endswith('.csv')]
    all_data = []

    for file in all_files:
        df = pd.read_csv(file, parse_dates=['timestamp'])
        all_data.append(df)

    combined_df = pd.concat(all_data)
    combined_df = combined_df.sort_values(by='timestamp')
    combined_df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file} and started analyzation...")
    print(f"For backtese use this data file: {output_file}")

def custom_plot(results, trades, data, resample=None):
    df = data
    equity_curve = results['_equity_curve']
    
    if resample:
        df = df.resample(resample).agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        equity_curve.index = pd.to_datetime(equity_curve.index)
        equity_curve = equity_curve.resample(resample).last().dropna()
        trades['EntryTime'] = pd.to_datetime(trades['EntryTime'])
        trades['ExitTime'] = pd.to_datetime(trades['ExitTime'])
        trades = trades.resample(resample, on='ExitTime').last().dropna()

    fig, ax1 = plt.subplots()

    df['Close'].plot(ax=ax1, label='Close', color='black', lw=0.8)
    
    # Plot buy/sell trades
    if not trades.empty:
        buy_trades = trades[trades['Size'] > 0]
        sell_trades = trades[trades['Size'] < 0]

        ax1.scatter(buy_trades['ExitTime'], df['Close'].reindex(buy_trades['ExitTime']), color='green', marker='^', alpha=0.8)
        ax1.scatter(sell_trades['ExitTime'], df['Close'].reindex(sell_trades['ExitTime']), color='red', marker='v', alpha=0.8)
    
    ax2 = ax1.twinx()
    equity_curve.plot(ax=ax2, label='Equity', color='blue', lw=0.8)
    
    plt.title(f"Backtest result for {results['_strategy']}")
    plt.legend()
    plt.show()
    
    return fig, ax1, ax2

def correct_columns_name(self, data):
    columns = data.columns
    corrected_columns = [col[0].upper() + col[1:] for col in columns]
    data.columns = corrected_columns
    return data

def convert_to_minutes(interval):
    if interval.endswith("min"):
        return int(interval[:-3])
    elif interval.endswith("h"):
        return int(interval[:-1]) * 60
    elif interval.endswith("d"):
        return int(interval[:-1]) * 24 * 60
    else:
        raise ValueError("Unsupported interval format")


# interval_minutes = convert_to_minutes(interval)
# if interval_minutes <= 30:
#     file_path = resalmple_data.process(interval)
# else:
#     file_path = resalmple_data.find_csv_file(data_directory, file_number)


# if __name__ == "__main__":
#     input_directory = "./data/POLYGON/minute"  # Change this to your actual input directory
#     output_file = "data/POLYGON/minute/combined_data.csv"  # Change this to your desired output file path

#     combine_csv_files_data(input_directory, output_file)

# def create_date_range(start_date, end_date):
#     # Generate a range of dates between start_date and end_date
#     date_range = pd.date_range(start=start_date, end=end_date).tolist()
#     # Convert each Timestamp to string
#     date_range_str = [date.strftime('%Y-%m-%d') for date in date_range]
#     return date_range_str

# def create_month_range(start_month, end_month):
#     # Generate a range of months between start_month and end_month
#     month_range = pd.date_range(start=start_month, end=end_month, freq='MS').tolist()
#     # Convert each Timestamp to string in 'YYYY-MM' format
#     month_range_str = [date.strftime('%Y-%m-%d') for date in month_range]
#     return month_range_str

import yfinance as yf

def down():

    msft = yf.download("MSFT")

    # get all stock info
    msft.info

    # get historical market data
    hist = msft.history(period="1mo")
