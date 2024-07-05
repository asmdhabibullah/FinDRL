import ta

class MomentumIndicators:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def rsi(data, column='Close', period=14):
        return ta.momentum.rsi(data[column], window=period)

    @staticmethod
    def macd(data, column='Close', short=12, long=26, signal=9):
        macd_line = ta.trend.macd(data[column], window_slow=long, window_fast=short)
        signal_line = ta.trend.macd_signal(data[column], window_slow=long, window_fast=short, window_sign=signal)
        return macd_line, signal_line

    @staticmethod
    def so(data, high='High', low='Low', close='Close', period=14):
        return ta.momentum.stoch(data[high], data[low], data[close], window=period, smooth_window=3)

    @staticmethod
    def wr(data, high='High', low='Low', close='Close', period=14):
        return ta.momentum.williams_r(data[high], data[low], data[close], lbp=period)

# import ta

# class MomentumIndicators:
#     def __init__(self, data):
#         self.data = data

#     @staticmethod
#     def rsi(data, column='Close', period=14):
#         return ta.momentum.rsi(data[column], window=period)

#     @staticmethod
#     def macd(data, column='Close', short=12, long=26, signal=9):
#         macd_line = ta.trend.macd(data[column], window_slow=long, window_fast=short)
#         signal_line = ta.trend.macd_signal(data[column], window_slow=long, window_fast=short, window_sign=signal)
#         return macd_line, signal_line

#     @staticmethod
#     def so(data, high='High', low='Low', close='Close', period=14):
#         return ta.momentum.stoch(data[high], data[low], data[close], window=period, smooth_window=3)

#     @staticmethod
#     def wr(data, high='High', low='Low', close='Close', period=14):
#         return ta.momentum.williams_r(data[high], data[low], data[close], lbp=period)


# class MomentumIndicators:
#     def __init__(self, data):
#         self.data = data

#     @staticmethod
#     def rsi(data, column='Close', period=14):
#         series = data[column]
#         delta = series.diff()
#         gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
#         loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
#         rs = gain / loss
#         return 100 - (100 / (1 + rs))

#     @staticmethod
#     def macd(data, column='Close', short=12, long=26, signal=9):
#         series = data[column]
#         short_ema = series.ewm(span=short, adjust=False).mean()
#         long_ema = series.ewm(span=long, adjust=False).mean()
#         macd = short_ema - long_ema
#         signal_line = macd.ewm(span=signal, adjust=False).mean()
#         return macd, signal_line

#     @staticmethod
#     def so(data, high='High', low='Low', close='Close', period=14):
#         lowest_low = data[low].rolling(window=period).min()
#         highest_high = data[high].rolling(window=period).max()
#         k_percent = 100 * (data[close] - lowest_low) / (highest_high - lowest_low)
#         return k_percent

#     @staticmethod
#     def wr(data, high='High', low='Low', close='Close', period=14):
#         highest_high = data[high].rolling(window=period).max()
#         lowest_low = data[low].rolling(window=period).min()
#         return -100 * (highest_high - data[close]) / (highest_high - lowest_low)

# import pandas as pd

# class MomentumIndicators:
#     def __init__(self, data):
#         self.data = data

#     @staticmethod
#     def rsi(data, column='Close', period=14):
#         series = data[column]
#         delta = series.diff()
#         gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
#         loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
#         rs = gain / loss
#         return 100 - (100 / (1 + rs))

#     @staticmethod
#     def macd(data, column='Close', short=12, long=26, signal=9):
#         series = data[column]
#         short_ema = series.ewm(span=short, adjust=False).mean()
#         long_ema = series.ewm(span=long, adjust=False).mean()
#         macd = short_ema - long_ema
#         signal_line = macd.ewm(span=signal, adjust=False).mean()
#         return macd, signal_line

#     @staticmethod
#     def so(data, high='High', low='Low', close='Close', period=14):
#         lowest_low = data[low].rolling(window=period).min()
#         highest_high = data[high].rolling(window=period).max()
#         k_percent = 100 * (data[close] - lowest_low) / (highest_high - lowest_low)
#         return k_percent

#     @staticmethod
#     def wr(data, high='High', low='Low', close='Close', period=14):
#         highest_high = data[high].rolling(window=period).max()
#         lowest_low = data[low].rolling(window=period).min()
#         return -100 * (highest_high - data[close]) / (highest_high - lowest_low)


# # Sample usage
# if __name__ == "__main__":
#     # Load your data here
#     # For example, using a CSV file
#     data = pd.read_csv('your_stock_data.csv')
    
#     # Initialize the MomentumIndicators class with the data
#     mi = MomentumIndicators(data)
    
#     # Calculate all indicators
#     mi.calculate_all_indicators()
    
#     # Display the first few rows with the new indicators
#     print(mi.data.head())

# import pandas as pd

# # Custom RSI implementation
# def RSI(data, window=14):
#     data = pd.Series(data)  # Ensure the data is a pandas Series
#     delta = data.diff()
#     gain = (delta.where(delta > 0, 0)).fillna(0)
#     loss = (-delta.where(delta < 0, 0)).fillna(0)
#     avg_gain = gain.rolling(window=window).mean()
#     avg_loss = loss.rolling(window=window).mean()
#     rs = avg_gain / avg_loss
#     rsi = 100 - (100 / (1 + rs))
#     return rsi

# # Custom MACD implementation
# def MACD(data, short_window=12, long_window=26, signal_window=9):
#     data = pd.Series(data)  # Ensure the data is a pandas Series
#     short_ema = data.ewm(span=short_window, adjust=False).mean()
#     long_ema = data.ewm(span=long_window, adjust=False).mean()
#     macd = short_ema - long_ema
#     signal = macd.ewm(span=signal_window, adjust=False).mean()
#     return macd, signal

# # Custom Bollinger Bands implementation
# def BollingerBands(data, window=20, no_of_std=2):
#     data = pd.Series(data)  # Ensure the data is a pandas Series
#     rolling_mean = data.rolling(window=window).mean()
#     rolling_std = data.rolling(window=window).std()
#     upper_band = rolling_mean + (rolling_std * no_of_std)
#     lower_band = rolling_mean - (rolling_std * no_of_std)
#     return upper_band, lower_band

# # Custom SMA implementation
# def SMA(data, window):
#     data = pd.Series(data)  # Ensure the data is a pandas Series
#     return data.rolling(window=window).mean()

    # def calculate_rsi(self, window=14):
    #     delta = self.data['Close'].diff()
    #     gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    #     loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    #     rs = gain / loss
    #     self.data['RSI'] = 100 - (100 / (1 + rs))

    # def calculate_macd(self, short_window=12, long_window=26, signal_window=9):
    #     short_ema = self.data['Close'].ewm(span=short_window, adjust=False).mean()
    #     long_ema = self.data['Close'].ewm(span=long_window, adjust=False).mean()
    #     macd = short_ema - long_ema
    #     signal = macd.ewm(span=signal_window, adjust=False).mean()
    #     self.data['MACD'] = macd
    #     self.data['MACD_Signal'] = signal
    #     self.data['MACD_Histogram'] = macd - signal

    # def calculate_stochastic_oscillator(self, window=14):
    #     low_min = self.data['Low'].rolling(window=window).min()
    #     high_max = self.data['High'].rolling(window=window).max()
    #     stoch_k = 100 * ((self.data['Close'] - low_min) / (high_max - low_min))
    #     stoch_d = stoch_k.rolling(window=3).mean()
    #     self.data['Stoch_K'] = stoch_k
    #     self.data['Stoch_D'] = stoch_d

    # def calculate_cci(self, window=20):
    #     typical_price = (self.data['High'] + self.data['Low'] + self.data['Close']) / 3
    #     sma_typical_price = typical_price.rolling(window=window).mean()
    #     mean_deviation = typical_price.rolling(window=window).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    #     cci = (typical_price - sma_typical_price) / (0.015 * mean_deviation)
    #     self.data['CCI'] = cci

    # def calculate_roc(self, window=12):
    #     roc = self.data['Close'].diff(window) / self.data['Close'].shift(window) * 100
    #     self.data['ROC'] = roc

    # def calculate_adx(self, window=14):
    #     plus_dm = self.data['High'].diff()
    #     minus_dm = self.data['Low'].diff()
    #     plus_dm[plus_dm < 0] = 0
    #     minus_dm[minus_dm > 0] = 0
    #     atr = (self.data['High'] - self.data['Low']).rolling(window=window).mean()
    #     plus_di = 100 * (plus_dm / atr).rolling(window=window).mean()
    #     minus_di = 100 * (minus_dm.abs() / atr).rolling(window=window).mean()
    #     dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di)).rolling(window=window).mean()
    #     self.data['ADX'] = dx.rolling(window=window).mean()

    # def calculate_williams_r(self, window=14):
    #     highest_high = self.data['High'].rolling(window=window).max()
    #     lowest_low = self.data['Low'].rolling(window=window).min()
    #     williams_r = (highest_high - self.data['Close']) / (highest_high - lowest_low) * -100
    #     self.data['Williams_R'] = williams_r

    # def calculate_momentum(self, window=10):
    #     momentum = self.data['Close'].diff(window)
    #     self.data['Momentum'] = momentum

    # def calculate_chaikin_oscillator(self, short_window=3, long_window=10):
    #     adl = ((self.data['Close'] - self.data['Low']) - (self.data['High'] - self.data['Close'])) / (self.data['High'] - self.data['Low']) * self.data['Volume']
    #     chaikin_oscillator = adl.ewm(span=short_window, adjust=False).mean() - adl.ewm(span=long_window, adjust=False).mean()
    #     self.data['Chaikin'] = chaikin_oscillator

    # def calculate_emv(self, window=14):
    #     distance_moved = ((self.data['High'] + self.data['Low']) / 2).diff()
    #     box_ratio = (self.data['Volume'] / 1e8) / (self.data['High'] - self.data['Low'])
    #     emv = distance_moved / box_ratio
    #     self.data['EMV'] = emv.rolling(window=window).mean()

    # def calculate_all_indicators(self):
    #     self.calculate_rsi()
    #     self.calculate_macd()
    #     self.calculate_stochastic_oscillator()
    #     self.calculate_cci()
    #     self.calculate_roc()
    #     self.calculate_adx()
    #     self.calculate_williams_r()
    #     self.calculate_momentum()
    #     self.calculate_chaikin_oscillator()
    #     self.calculate_emv()
