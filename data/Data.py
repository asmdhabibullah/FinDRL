import pandas as pd
from os import listdir, path, makedirs

class DataResampler:
    def __init__(self, folder_path, file_number=0):
        self.df = None
        self.file_number = file_number
        self.folder_path = folder_path

    def correct_columns_name(self, data):
        columns = data.columns
        corrected_columns = [col[0].upper() + col[1:] if len(col) > 1 else col.upper() for col in columns]
        data.columns = corrected_columns
        return data

    def find_csv_file(self, folder_path, file_number):
        """Find a CSV file in the specified folder based on the provided file number."""
        csv_files = [file for file in listdir(folder_path) if file.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV files found in the specified folder.")

        if file_number >= len(csv_files):
            raise ValueError(f"Requested file number ({file_number}) is out of range. Available files: {len(csv_files)}")
        
        selected_file = csv_files[file_number]
        return path.join(self.folder_path, selected_file), selected_file
    
    # def load_data(self, folder_path, file_number=0):
    #     """Load the 1-minute data from the specified CSV file."""
    #     file_path, selected_file = self.find_csv_file(folder_path, file_number)
    #     self.df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
    #     print("Data loaded successfully.")
    #     return selected_file
    def load_data(self, folder_path, file_number=0):
        """Load the 1-minute data from the specified CSV file."""
        file_path, selected_file = self.find_csv_file(folder_path, file_number)
        self.df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
        # self.df = self.correct_columns_name(self.df)
        print("Data loaded successfully.")
        return selected_file

    def resample_data(self, interval):
        """Resample the data to the specified interval."""
        if self.df is None:
            raise ValueError("Data not loaded. Please load the data first.")
        
        # Ensure the index is a DateTimeIndex
        if not isinstance(self.df.index, pd.DatetimeIndex):
            raise ValueError("Index is not a DateTimeIndex")

        # Fill missing columns with appropriate values
        self.df.fillna({
            'volume': 0,
            'vw': 0,
            'open': self.df['close'].shift(),
            'close': self.df['open'].shift(-1),
            'high': self.df[['open', 'close']].max(axis=1),
            'low': self.df[['open', 'close']].min(axis=1),
            'number_of_trades': 0
        }, inplace=True)

        # Ensure open prices are carried forward correctly for resampling
        self.df['open'] = self.df['open'].ffill()

        # Handle case where 'open' may still have NaN at the start
        if pd.isnull(self.df['open'].iloc[0]):
            self.df['open'].iloc[0] = self.df['close'].iloc[0]
        
        resampled_df = self.df.resample(interval).agg({
            'volume': 'sum',  # Sum the volume
            'vw': 'mean',     # Average the volume-weighted price
            'open': 'first',  # Take the first open price
            'close': 'last',  # Take the last close price
            'high': 'max',    # Take the highest price
            'low': 'min',     # Take the lowest price
            'number_of_trades': 'sum'  # Sum the number of trades
        })
        
        # Drop rows with any missing values
        resampled_df.dropna(inplace=True)

        # Reset index to convert timestamp back to a column
        resampled_df = resampled_df.reset_index()
        resampled_df.rename(columns={'timestamp': 'Date', 'volume': 'Volume', 'vw': 'VW', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'number_of_trades': 'Number_of_trades'}, inplace=True)
        
        # # Split the DateTime index into Date and Time columns
        # resampled_df['Date'] = resampled_df.index.Date.astype(str)
        
        # # Set the Date column as the index
        # resampled_df.set_index('Date', inplace=True)

        return resampled_df
    
    def process(self, interval="15min"):
        """Orchestrate the data loading, resampling, and saving process, and return the new file's absolute path."""
        selected_file = self.load_data(self.folder_path, self.file_number)

        resampled_df = self.resample_data(interval)

        # print("resampled_df DF")
        # print(resampled_df.head(5))

        # self.df = self.correct_columns_name(resampled_df)
        
        # Create the analysis directory if it doesn't exist
        analysis_dir = path.join(self.folder_path, 'analysis')
        if not path.exists(analysis_dir):
            makedirs(analysis_dir)

        output_file = path.join(analysis_dir, f"{interval}_{selected_file}")

        # Save the resampled data to a CSV file, replacing the file if it already exists
        resampled_df.to_csv(output_file, index=False)

        print(f"Resampled data saved to {output_file}")

        print("Processed data...")
        print(self.df.head(5))

        return path.abspath(output_file)

class DataLoder:
    
    def __init__(self, folder_path, file_number):
        self.folder_path = folder_path
        self.file_number = file_number

    def load(self):
        """Find a CSV file in the specified folder based on the provided file number."""
        csv_files = [file for file in listdir(self.folder_path) if file.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV files found in the specified folder.")

        if self.file_number >= len(csv_files):
            raise ValueError(f"Requested file number ({self.file_number}) is out of range. Available files: {len(csv_files)}")
        
        selected_file = csv_files[self.file_number]
        data_path = path.join(self.folder_path, selected_file)
        df = pd.read_csv(data_path)
        # df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime
        # df.set_index('Date', inplace=True)  # Set 'Date' column as index

        return df

# import pandas as pd
# from os import listdir, path, makedirs

# class DataResampler:
#     def __init__(self, folder_path, file_number=0):
#         self.df = None
#         self.file_number = file_number
#         self.folder_path = folder_path

#     def find_csv_file(self, folder_path, file_number):
#         """Find a CSV file in the specified folder based on the provided file number."""
#         csv_files = [file for file in listdir(folder_path) if file.endswith('.csv')]
#         if not csv_files:
#             raise FileNotFoundError("No CSV files found in the specified folder.")

#         if file_number >= len(csv_files):
#             raise ValueError(f"Requested file number ({file_number}) is out of range. Available files: {len(csv_files)}")
        
#         selected_file = csv_files[file_number]
#         return path.join(self.folder_path, selected_file), selected_file
    
#     def load_data(self, folder_path, file_number=0):
#         """Load the 1-minute data from the specified CSV file."""
#         file_path, selected_file = self.find_csv_file(folder_path, file_number)
#         self.df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
#         print("Data loaded successfully.")
#         return selected_file
    
#     def resample_data(self, interval):
#         """Resample the data to the specified interval."""
#         if self.df is None:
#             raise ValueError("Data not loaded. Please load the data first.")
        
#         # Fill missing columns with appropriate values
#         self.df.fillna({
#             'volume': 0,
#             'vw': 0,
#             'open': self.df['close'].shift(),
#             'close': self.df['open'].shift(-1),
#             'high': self.df[['open', 'close']].max(axis=1),
#             'low': self.df[['open', 'close']].min(axis=1),
#             'number_of_trades': 0
#         }, inplace=True)

#         # Ensure open prices are carried forward correctly for resampling
#         self.df['open'] = self.df['open'].ffill()

#         # Handle case where 'open' may still have NaN at the start
#         if pd.isnull(self.df['open'].iloc[0]):
#             self.df['open'].iloc[0] = self.df['close'].iloc[0]
        
#         resampled_df = self.df.resample(interval).agg({
#             'volume': 'sum',  # Sum the volume
#             'vw': 'mean',     # Average the volume-weighted price
#             'open': 'first',  # Take the first open price
#             'close': 'last',  # Take the last close price
#             'high': 'max',    # Take the highest price
#             'low': 'min',     # Take the lowest price
#             'number_of_trades': 'sum'  # Sum the number of trades
#         })
        
#         # Drop rows with any missing values
#         resampled_df.dropna(inplace=True)

#         # Reset index to convert timestamp back to a column
#         resampled_df = resampled_df.reset_index()
#         resampled_df.rename(columns={'timestamp': 'Date', 'volume': 'Volume', 'vw': 'VW', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'number_of_trades': 'Number_of_trades'}, inplace=True)
        
#         return resampled_df
    
#     def process(self, interval="15min"):
#         """Orchestrate the data loading, resampling, and saving process, and return the new file's absolute path."""
#         selected_file = self.load_data(self.folder_path, self.file_number)
#         resampled_df = self.resample_data(interval)
        
#         # Create the analysis directory if it doesn't exist
#         analysis_dir = path.join(self.folder_path, 'analysis')
#         if not path.exists(analysis_dir):
#             makedirs(analysis_dir)

        # output_file = path.join(analysis_dir, f"{interval}_{selected_file}")

        # # Save the resampled data to a CSV file, replacing the file if it already exists
        # resampled_df.to_csv(output_file, index=False)
        # print(f"Resampled data saved to {output_file}.")

        # return path.abspath(output_file)

# import pandas as pd
# from os import listdir, path, makedirs

# class DataResampler:
#     def __init__(self, folder_path, file_number=0):
#         self.df = None
#         self.file_number = file_number
#         self.folder_path = folder_path

#     def find_csv_file(self, folder_path, file_number):
#         """Find a CSV file in the specified folder based on the provided file number."""
#         csv_files = [file for file in listdir(folder_path) if file.endswith('.csv')]
#         if not csv_files:
#             raise FileNotFoundError("No CSV files found in the specified folder.")

#         if file_number >= len(csv_files):
#             raise ValueError(f"Requested file number ({file_number}) is out of range. Available files: {len(csv_files)}")
        
#         selected_file = csv_files[file_number]
#         return path.join(self.folder_path, selected_file), selected_file
    
#     def load_data(self, folder_path, file_number=0):
#         """Load the 1-minute data from the specified CSV file."""
#         file_path, selected_file = self.find_csv_file(folder_path, file_number)
#         self.df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
#         print("Data loaded successfully.")
#         return selected_file
    
#     def resample_data(self, interval):
#         """Resample the data to the specified interval."""
#         if self.df is None:
#             raise ValueError("Data not loaded. Please load the data first.")
        
#         # Fill missing columns with appropriate values
#         self.df.fillna({
#             'volume': 0,
#             'vw': 0,
#             'open': self.df['close'].shift(),
#             'close': 0,
#             'high': 0,
#             'low': 0,
#             'number_of_trades': 0
#         }, inplace=True)

#         # Ensure open prices are carried forward correctly for resampling
#         # self.df['open'].fillna(method='ffill', inplace=True)
#         self.df['open'] = self.df['open'].ffill()

#         # Handle case where 'open' may still have NaN at the start
#         if pd.isnull(self.df['open'].iloc[0]):
#             self.df['open'].iloc[0] = self.df['close'].iloc[0]

#         resampled_df = self.df.resample(interval).agg({
#             'volume': 'sum',  # Sum the volume
#             'vw': 'mean',     # Average the volume-weighted price
#             'open': 'first',  # Take the first open price
#             'close': 'last',  # Take the last close price
#             'high': 'max',    # Take the highest price
#             'low': 'min',     # Take the lowest price
#             'number_of_trades': 'sum'  # Sum the number of trades
#         })
        
#         # Reset index to convert timestamp back to a column
#         resampled_df = resampled_df.reset_index()
#         resampled_df.rename(columns={'timestamp': 'Date', 'volume': 'Volume', 'vw': 'VW', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'number_of_trades': 'Number_of_trades'}, inplace=True)
        
#         return resampled_df
    
#     def process(self, interval="15min"):
#         """Orchestrate the data loading, resampling, and saving process, and return the new file's absolute path."""
#         selected_file = self.load_data(self.folder_path, self.file_number)
#         resampled_df = self.resample_data(interval)
        
#         # Create the analysis directory if it doesn't exist
#         analysis_dir = path.join(self.folder_path, 'analysis')
#         if not path.exists(analysis_dir):
#             makedirs(analysis_dir)

#         output_file = path.join(analysis_dir, selected_file)

#         # Save the resampled data to a CSV file
#         resampled_df.to_csv(output_file, index=False)
#         print(f"Resampled data saved to {output_file}.")

#         return path.abspath(output_file)



# import pandas as pd
# from os import listdir, path, mkdir

# class DataResampler:
#     def __init__(self, folder_path, file_number=0):
#         self.df = None
#         self.file_number = file_number
#         self.folder_path = folder_path

#     def find_csv_file(self, folder_path, file_number):
#         """Find a CSV file in the specified folder based on the provided file number."""
#         csv_files = [file for file in listdir(folder_path) if file.endswith('.csv')]
#         if not csv_files:
#             raise FileNotFoundError("No CSV files found in the specified folder.")

#         if file_number >= len(csv_files):
#             raise ValueError(f"Requested file number ({file_number}) is out of range. Available files: {len(csv_files)}")
        
#         selected_file = csv_files[file_number]
#         return path.join(self.folder_path, selected_file), selected_file
    
#     def load_data(self, folder_path, file_number=0):
#         """Load the 1-minute data from the first CSV file found in the folder."""
#         file_path, selected_file = self.find_csv_file(folder_path, file_number)
#         self.df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
#         print("Data loaded successfully.")
#         return selected_file
    
#     def resample_data(self, interval):
#         """Resample the data to the specified interval."""
#         if self.df is None:
#             raise ValueError("Data not loaded. Please load the data first.")
        
#         resampled_df = self.df.resample(interval).agg({
#             'volume': 'sum',  # Sum the volume
#             'vw': 'mean',     # Average the volume-weighted price
#             'open': 'first',  # Take the first open price
#             'close': 'last',  # Take the last close price
#             'high': 'max',    # Take the highest price
#             'low': 'min',     # Take the lowest price
#             'number_of_trades': 'sum'  # Sum the number of trades
#         })
        
#         # Reset index to convert timestamp back to a column
#         resampled_df = resampled_df.reset_index()
#         resampled_df.rename(columns={'timestamp': 'Date', 'volume': 'Volume', 'vw': 'VW', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'number_of_trades': 'Number_of_trades'}, inplace=True)
        
#         resampled_df = resampled_df[resampled_df['Volume'] > 0]

#         return resampled_df
    
#     def process(self, interval="15T"):
#         """Orchestrate the data loading, resampling, and saving process, and return the new file's absolute path."""
#         selected_file = self.load_data(self.folder_path, self.file_number)
#         resampled_df = self.resample_data(interval)
        
#         # Ensure the 'analysis' directory exists
#         analysis_dir = path.join(self.folder_path, 'analysis')
#         if not path.exists(analysis_dir):
#             mkdir(analysis_dir)

#         # Save the resampled data to a CSV file
#         output_file = path.join(analysis_dir, f"{interval}_{selected_file}")
#         resampled_df.to_csv(output_file, index=False)
#         print(f"Resampled data saved to {output_file}.")

#         return output_file


# import pandas as pd
# from os import listdir, path, mkdir

# class DataResampler:
#     def __init__(self, folder_path, file_number=0):
#         self.df = None
#         self.file_number = file_number
#         self.folder_path = folder_path

#     def find_csv_file(self, folder_path, file_number):
#         """Find a CSV file in the specified folder based on the provided file number."""
#         csv_files = [file for file in listdir(folder_path) if file.endswith('.csv')]
#         if not csv_files:
#             raise FileNotFoundError("No CSV files found in the specified folder.")

#         if file_number >= len(csv_files):
#             raise ValueError(f"Requested file number ({file_number}) is out of range. Available files: {len(csv_files)}")
        
#         selected_file = csv_files[file_number]
#         return path.join(self.folder_path, selected_file), selected_file
    
#     def load_data(self, folder_path, file_number=0):
#         """Load the 1-minute data from the first CSV file found in the folder."""
#         file_path, selected_file = self.find_csv_file(folder_path, file_number)
#         """Load the 1-minute data from a CSV file."""
#         self.df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
#         print("Data loaded successfully.")

#         return selected_file
    
#     def resample_data(self, interval):
#         """Resample the data to the specified interval."""
#         if self.df is None:
#             raise ValueError("Data not loaded. Please load the data first.")
        
#         resampled_df = self.df.resample(interval).agg({
#             'volume': 'sum',  # Sum the volume
#             'vw': 'mean',     # Average the volume-weighted price
#             'open': 'first',  # Take the first open price
#             'close': 'last',  # Take the last close price
#             'high': 'max',    # Take the highest price
#             'low': 'min',     # Take the lowest price
#             'number_of_trades': 'sum'  # Sum the number of trades
#         })
        
#         # Reset index to convert timestamp back to a column
#         resampled_df = resampled_df.reset_index()
#         resampled_df.rename(columns={'timestamp': 'Date', 'volume': 'Volume', 'vw': 'VW', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'number_of_trades': 'Number_of_trades'}, inplace=True)
        
#         return resampled_df
    
#     def process(self, interval="15T"):
#         """Orchestrate the data loading, resampling, and saving process, and return the new file's absolute path."""
#         selected_file =self.load_data(self.folder_path, self.file_number)
#         resampled_df = self.resample_data(interval)
#         file = f"{self.folder_path}/analysis"
    
#         if not path.exists(file):
#             mkdir(file)

#         output_file=f"{file}/{selected_file}"

#         """Save the resampled data to a CSV file."""
#         resampled_df.to_csv(output_file)
#         print(f"Resampled data saved to {output_file}.")

#         return output_file

# Usage
# if __name__ == "__main__":
#     file_path = 'data.csv'  # Replace with the path to your CSV file
#     resampler = DataResampler(file_path)
    
#     # Load data
#     resampler.load_data()
    
#     # Resample to 30-minute intervals
#     df_30min = resampler.resample_data('30T')
#     print("30-minute dataframe:")
#     print(df_30min.head())
#     resampler.save_data(df_30min, 'data_30min.csv')
    
#     # Resample to 1-hour intervals
#     df_1h = resampler.resample_data('1H')
#     print("1-hour dataframe:")
#     print(df_1h.head())
#     resampler.save_data(df_1h, 'data_1h.csv')



# import pandas as pd

# class DataResampler:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.df = None

#     def load_data(self):
#         """Load the 1-minute data from a CSV file."""
#         self.df = pd.read_csv(self.file_path, parse_dates=['date'], index_col='date')
#         print("Data loaded successfully.")
    
#     def resample_data(self, interval):
#         """Resample the data to the specified interval."""
#         if self.df is None:
#             raise ValueError("Data not loaded. Please load the data first.")
        
#         return self.df.resample(interval).mean()
    
#     def save_data(self, resampled_df, output_file):
#         """Save the resampled data to a CSV file."""
#         resampled_df.to_csv(output_file)
#         print(f"Resampled data saved to {output_file}.")

# # Usage
# if __name__ == "__main__":
#     file_path = 'data.csv'  # Replace with the path to your CSV file
#     resampler = DataResampler(file_path)
    
#     # Load data
#     resampler.load_data()
    
#     # Resample to 30-minute intervals
#     df_30min = resampler.resample_data('30T')
#     print("30-minute dataframe:")
#     print(df_30min.head())
#     resampler.save_data(df_30min, 'data_30min.csv')
    
#     # Resample to 1-hour intervals
#     df_1h = resampler.resample_data('1H')
#     print("1-hour dataframe:")
#     print(df_1h.head())
#     resampler.save_data(df_1h, 'data_1h.csv')
