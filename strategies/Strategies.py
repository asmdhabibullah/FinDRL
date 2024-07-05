import ta
import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.test import SMA
from backtesting.lib import crossover

class FlatTopBreakout(Strategy):
    indicators = None
    profit_target = 0.1
    stop_loss = 0.05

    def init(self):
        if self.indicators is None:
            raise ValueError("Indicators must be set before running the strategy")

        # Initialize the MomentumIndicators with the current data
        self.indicators = self.indicators(self.data.df)

        # Convert internal data to Pandas Series for rolling calculations
        high_series = pd.Series(self.data.High, index=self.data.index)
        low_series = pd.Series(self.data.Low, index=self.data.index)
        close_series = pd.Series(self.data.Close, index=self.data.index)

        # Calculate necessary indicators for the strategy
        self.high_max = self.I(lambda: high_series.rolling(window=20).max())
        self.low_min = self.I(lambda: low_series.rolling(window=20).min())
        self.higher_lows = self.I(lambda: low_series.rolling(window=20).apply(lambda x: all(np.diff(x) >= 0)))

        # Calculate momentum indicators
        self.rsi = self.I(lambda: self.indicators.rsi(self.data.df))
        self.macd, self.signal_line = self.I(lambda: self.indicators.macd(self.data.df))
        self.so = self.I(lambda: self.indicators.so(self.data.df))
        self.wr = self.I(lambda: self.indicators.wr(self.data.df))

        # Calculate moving averages for crossover
        self.sma_short = self.I(lambda: close_series.rolling(window=10).mean())
        self.sma_long = self.I(lambda: close_series.rolling(window=50).mean())

    def next(self):
        # Define the breakout and indicator conditions for buying
        if (self.higher_lows[-1] and 
            self.data.Close[-1] > self.high_max[-2] * 1.02 and
            self.rsi[-1] < 70 and
            self.macd[-1] > self.signal_line[-1] and
            self.so[-1] < 80 and
            self.wr[-1] > -20 and
            crossover(self.sma_short, self.sma_long)):
            
            self.buy(sl=self.data.Close[-1] * (1 - self.stop_loss), tp=self.data.Close[-1] * (1 + self.profit_target))

        # Define conditions for closing the position
        for trade in self.trades:
            # Close the trade if the stop loss or profit target is hit
            if self.data.Close[-1] <= trade.sl or self.data.Close[-1] >= trade.tp:
                self.position.close()

            # Optional: Additional conditions based on indicators
            # Example: Close if RSI is overbought
            if self.rsi[-1] > 70:
                self.position.close()

class EnhancedFlatTopBreakout(Strategy):
    indicators = None
    profit_target = 0.1
    stop_loss = 0.05

    def init(self):
        if self.indicators is None:
            raise ValueError("Indicators must be set before running the strategy")

        # Initialize the MomentumIndicators with the current data
        self.indicators = self.indicators(self.data.df)

        # Convert internal data to Pandas Series for rolling calculations
        high_series = pd.Series(self.data.High, index=self.data.index)
        low_series = pd.Series(self.data.Low, index=self.data.index)
        close_series = pd.Series(self.data.Close, index=self.data.index)

        # Calculate necessary indicators for the strategy
        self.high_max = self.I(lambda: high_series.rolling(window=20).max())
        self.low_min = self.I(lambda: low_series.rolling(window=20).min())
        self.higher_lows = self.I(lambda: low_series.rolling(window=20).apply(lambda x: all(np.diff(x) >= 0)))

        # Calculate momentum indicators
        self.rsi = self.I(lambda: self.indicators.rsi(self.data.df))
        self.macd, self.signal_line = self.I(lambda: self.indicators.macd(self.data.df))
        self.so = self.I(lambda: self.indicators.so(self.data.df))
        self.wr = self.I(lambda: self.indicators.wr(self.data.df))

        # Calculate moving averages for crossover
        self.sma_short = self.I(lambda: close_series.rolling(window=10).mean())
        self.sma_long = self.I(lambda: close_series.rolling(window=50).mean())

    def next(self):
        # Print the current values of indicators and conditions
        print(f"Close: {self.data.Close[-1]}, High Max: {self.high_max[-2]}, RSI: {self.rsi[-1]}, MACD: {self.macd[-1]}, Signal: {self.signal_line[-1]}, SO: {self.so[-1]}, WR: {self.wr[-1]}")
        print(f"Higher Lows: {self.higher_lows[-1]}, SMA Short: {self.sma_short[-1]}, SMA Long: {self.sma_long[-1]}")

        # Define the breakout and indicator conditions for buying
        if (self.higher_lows[-1] and 
            self.data.Close[-1] > self.high_max[-2] * 1.02 and
            self.rsi[-1] < 70 and
            self.macd[-1] > self.signal_line[-1] and
            self.so[-1] < 80 and
            self.wr[-1] > -20 and
            crossover(self.sma_short, self.sma_long)):
            
            self.buy(sl=self.data.Close[-1] * (1 - self.stop_loss), tp=self.data.Close[-1] * (1 + self.profit_target))

        # Define conditions for closing the position
        for trade in self.trades:
            # Close the trade if the stop loss or profit target is hit
            if self.data.Close[-1] <= trade.sl or self.data.Close[-1] >= trade.tp:
                self.position.close()

            # Optional: Additional conditions based on indicators
            # Example: Close if RSI is overbought
            if self.rsi[-1] > 70:
                self.position.close()

class BreakoutBuildup(Strategy):
    atr_period = 14
    consolidation_period = 20
    breakout_threshold = 1.02
    profit_target = 0.1
    stop_loss = 0.05

    def init(self):
        # Calculate ATR for volatility measurement
        self.atr = self.I(pd.Series.rolling, self.data.ATR, self.atr_period)

        # Calculate the highest high and lowest low over the consolidation period
        self.high_max = self.I(pd.Series.rolling, self.data.High, self.consolidation_period).max()
        self.low_min = self.I(pd.Series.rolling, self.data.Low, self.consolidation_period).min()

        # Calculate moving averages for crossover (optional)
        self.sma_short = self.I(pd.Series.rolling, self.data.Close, 10).mean()
        self.sma_long = self.I(pd.Series.rolling, self.data.Close, 50).mean()

    def next(self):
        # Identify the consolidation phase by low ATR
        if self.atr[-1] < np.mean(self.atr[-self.consolidation_period:]):
            # Check for an upward breakout
            if self.data.Close[-1] > self.high_max[-2] * self.breakout_threshold:
                self.buy(sl=self.data.Close[-1] * (1 - self.stop_loss), tp=self.data.Close[-1] * (1 + self.profit_target))
            
            # Check for a downward breakout
            elif self.data.Close[-1] < self.low_min[-2] * (2 - self.breakout_threshold):
                self.sell(sl=self.data.Close[-1] * (1 + self.stop_loss), tp=self.data.Close[-1] * (1 - self.profit_target))

class MomentumSRMStrategy(Strategy):
    def init(self):
        # Calculate Stochastic Oscillator
        self.stoch_k = self.I(ta.momentum.stoch, self.data.High, self.data.Low, self.data.Close, window=14, smooth_window=3)
        self.stoch_d = self.I(ta.momentum.stoch_signal, self.data.High, self.data.Low, self.data.Close, window=14, smooth_window=3)
        
        # Calculate RSI
        self.rsi = self.I(ta.momentum.rsi, self.data.Close, window=14)
        
        # Calculate MACD
        macd = ta.trend.MACD(self.data.Close, window_slow=26, window_fast=12, window_sign=9)
        self.macd = self.I(lambda: macd.macd())
        self.macd_signal = self.I(lambda: macd.macd_signal())
        
    def next(self):
        # Define buy signal conditions
        stoch_oversold = self.stoch_k[-1] < 20 and self.stoch_d[-1] < 20
        rsi_uptrend = self.rsi[-1] > 50
        macd_bullish = self.macd[-1] > self.macd_signal[-1]
        stoch_not_overbought = self.stoch_k[-1] < 80 and self.stoch_d[-1] < 80
        
        if stoch_oversold and rsi_uptrend and macd_bullish and stoch_not_overbought:
            self.buy()

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


# import numpy as np
# import pandas as pd
# from backtesting import Strategy
# from backtesting.lib import crossover

# class EnhancedFlatTopBreakout(Strategy):
#     indicators = None
#     profit_target = 0.1
#     stop_loss = 0.05

#     def init(self):
#         if self.indicators is None:
#             raise ValueError("Indicators must be set before running the strategy")

#         # Initialize the MomentumIndicators with the current data
#         self.indicators = self.indicators(self.data.df)

#         # Convert internal data to Pandas Series for rolling calculations
#         high_series = pd.Series(self.data.High, index=self.data.index)
#         low_series = pd.Series(self.data.Low, index=self.data.index)
#         close_series = pd.Series(self.data.Close, index=self.data.index)

#         # Calculate necessary indicators for the strategy
#         self.high_max = self.I(lambda: high_series.rolling(window=20).max())
#         self.low_min = self.I(lambda: low_series.rolling(window=20).min())
#         self.higher_lows = self.I(lambda: low_series.rolling(window=20).apply(lambda x: all(np.diff(x) >= 0)))

#         # Calculate momentum indicators
#         self.rsi = self.I(lambda: self.indicators.rsi(self.data.df))
#         self.macd, self.signal_line = self.I(lambda: self.indicators.macd(self.data.df))
#         self.so = self.I(lambda: self.indicators.so(self.data.df))
#         self.wr = self.I(lambda: self.indicators.wr(self.data.df))

#     def next(self):
#         # Define the breakout and indicator conditions for buying
#         if (self.higher_lows[-1] and 
#             self.data.Close[-1] > self.high_max[-2] * 1.02 and
#             self.rsi[-1] < 70 and
#             self.macd[-1] > self.signal_line[-1] and
#             self.so[-1] < 80 and
#             self.wr[-1] > -20):
            
#             self.buy(sl=self.data.Close[-1] * (1 - self.stop_loss), tp=self.data.Close[-1] * (1 + self.profit_target))

#         # Define conditions for closing the position
#         for trade in self.trades:
#             # Close the trade if the stop loss or profit target is hit
#             if self.data.Close[-1] <= trade.sl or self.data.Close[-1] >= trade.tp:
#                 self.position.close()

#             # Optional: Additional conditions based on indicators
#             # Example: Close if RSI is overbought
#             if self.rsi[-1] > 70:
#                 self.position.close()



# import numpy as np
# import pandas as pd
# from backtesting import Strategy

# class EnhancedFlatTopBreakout(Strategy):
#     indicators = None
#     profit_target = 0.1
#     stop_loss = 0.05

#     def init(self):
#         if self.indicators is None:
#             raise ValueError("Indicators must be set before running the strategy")

#         # Initialize the MomentumIndicators with the current data
#         self.indicators = self.indicators(self.data.df)

#         # Calculate necessary indicators for the strategy
#         self.high_max = self.I(pd.Series.rolling, self.data.High, window=20).max()
#         self.low_min = self.I(pd.Series.rolling, self.data.Low, window=20).min()
#         self.higher_lows = self.I(lambda x: x.rolling(window=20).apply(lambda y: all(np.diff(y) >= 0)), self.data.Low)
        
#         # Calculate momentum indicators
#         self.rsi = self.I(self.indicators.rsi)
#         self.macd, self.signal_line = self.I(self.indicators.macd)
#         self.so = self.I(self.indicators.so)
#         self.wr = self.I(self.indicators.wr)

#     def next(self):
#         # Define the breakout and indicator conditions for buying
#         if (self.higher_lows[-1] and 
#             self.data.Close[-1] > self.high_max[-2] * 1.02 and
#             self.rsi[-1] < 70 and
#             self.macd[-1] > self.signal_line[-1] and
#             self.so[-1] < 80 and
#             self.wr[-1] > -20):
            
#             self.buy(sl=self.data.Close[-1] * (1 - self.stop_loss), tp=self.data.Close[-1] * (1 + self.profit_target))

#         # Define conditions for closing the position
#         for trade in self.trades:
#             # Close the trade if the stop loss or profit target is hit
#             if self.data.Close[-1] <= trade.sl or self.data.Close[-1] >= trade.tp:
#                 self.position.close()

#             # Optional: Additional conditions based on indicators
#             # Example: Close if RSI is overbought
#             if self.rsi[-1] > 70:
#                 self.position.close()

# class EnhancedFlatTopBreakout(Strategy):
#     indicators = None  # This should be set externally before running the strategy
#     profit_target = 0.1
#     stop_loss = 0.05

#     def init(self, indicators, profit_target=0.1, stop_loss=0.05):
#         # Initialize the MomentumIndicators with the current data
#         self.indicators = indicators

#         # Calculate necessary indicators for the strategy
#         self.high_max = self.I(pd.Series.rolling, self.data.High, window=20).max()
#         self.low_min = self.I(pd.Series.rolling, self.data.Low, window=20).min()
#         self.higher_lows = self.I(lambda x: x.rolling(window=20).apply(lambda y: all(np.diff(y) >= 0)), self.data.Low)
        
#         # Calculate momentum indicators
#         self.rsi = self.I(self.indicators.rsi)
#         self.macd, self.signal_line = self.I(self.indicators.macd)
#         self.so = self.I(self.indicators.so)
#         self.wr = self.I(self.indicators.wr)

#         # Store the profit target and stop loss
#         self.profit_target = profit_target
#         self.stop_loss = stop_loss

#     def next(self):
#         # Define the breakout and indicator conditions for buying
#         if (self.higher_lows[-1] and 
#             self.data.Close[-1] > self.high_max[-2] * 1.02 and
#             self.rsi[-1] < 70 and
#             self.macd[-1] > self.signal_line[-1] and
#             self.so[-1] < 80 and
#             self.wr[-1] > -20):
            
#             self.buy(sl=self.data.Close[-1] * (1 - self.stop_loss), tp=self.data.Close[-1] * (1 + self.profit_target))

#         # Define conditions for closing the position
#         for trade in self.trades:
#             # Close the trade if the stop loss or profit target is hit
#             if self.data.Close[-1] <= trade.sl or self.data.Close[-1] >= trade.tp:
#                 self.position.close()

#             # Optional: Additional conditions based on indicators
#             # Example: Close if RSI is overbought
#             if self.rsi[-1] > 70:
#                 self.position.close()


# class EnhancedFlatTopBreakout(Strategy):
#     def init(self, indicators):
#         # Initialize the MomentumIndicators with the current data
#         self.indicators = indicators

#         # Calculate necessary indicators for the strategy
#         self.high_max = self.I(pd.Series.rolling, self.data.High, window=20).max()
#         self.low_min = self.I(pd.Series.rolling, self.data.Low, window=20).min()
#         self.higher_lows = self.I(lambda x: x.rolling(window=20).apply(lambda y: all(np.diff(y) >= 0)), self.data.Low)
        
#         # Calculate momentum indicators
#         self.rsi = self.I(self.indicators.rsi)
#         self.macd, self.signal_line = self.I(self.indicators.macd)
#         self.so = self.I(self.indicators.so)
#         self.wr = self.I(self.indicators.wr)

#     def next(self):
#         # Define the breakout and indicator conditions for buying
#         if (self.higher_lows[-1] and 
#             self.data.Close[-1] > self.high_max[-2] * 1.02 and
#             self.rsi[-1] < 70 and
#             self.macd[-1] > self.signal_line[-1] and
#             self.so[-1] < 80 and
#             self.wr[-1] > -20):
            
#             self.buy(sl=self.low_min[-2], tp=self.data.Close[-1] + (self.data.Close[-1] - self.low_min[-2]))


# from indicators.Indicators import SMA, RSI, MACD, BollingerBands


# class FlatTopBreakout(Strategy):
#     def init(self):
#         self.high_max = self.I(pd.Series.rolling, self.data.High, window=20).max()
#         self.low_min = self.I(pd.Series.rolling, self.data.Low, window=20).min()
#         self.higher_lows = self.I(lambda x: x.rolling(window=20).apply(lambda y: all(np.diff(y) >= 0)), self.data.Low)

#     def next(self):
#         if self.higher_lows[-1] and self.data.Close[-1] > self.high_max[-2] * 1.02:
#             self.buy(sl=self.low_min[-2], tp=self.data.Close[-1] + (self.data.Close[-1] - self.low_min[-2]))



# class SmaCross(Strategy):
#     def init(self):
#         self.sma1 = self.I(SMA, self.data.Close, 10)
#         self.sma2 = self.I(SMA, self.data.Close, 20)

#     def next(self):
#         if crossover(self.sma1, self.sma2):
#             self.buy()
#         elif crossover(self.sma2, self.sma1):
#             self.sell()


# # Strategy 1: Momentum-Based Strategy
# # Indicators: RSI, MACD, Bollinger Bands

# class MomentumStrategy(Strategy):
#     def init(self):
#         self.rsi = self.I(RSI, self.data.Close, window=14)
#         self.macd, self.signal = self.I(MACD, self.data.Close)
#         self.upper_band, self.lower_band = self.I(BollingerBands, self.data.Close, window=20, no_of_std=2)

#     def next(self): 
#         if self.rsi[-1] < 35 and crossover(self.macd, self.signal) and self.data.Close[-1] < self.lower_band[-1]:
#             self.buy()
#         elif self.rsi[-1] > 65 and crossover(self.signal, self.macd) and self.data.Close[-1] > self.upper_band[-1]:
#             self.sell()


# # Strategy 2: Moving Average Crossover Strategy
# # Indicators: Short-term EMA, Long-term EMA, Volume

# class MovingAverageCrossoverStrategy(Strategy):
#     def init(self):
#         self.short_ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=12)
#         self.long_ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=26)
#         self.volume = self.data.Volume

#     def next(self):
#         if crossover(self.short_ema, self.long_ema) and self.volume[-1] > self.volume.mean():
#             self.buy()
#         elif crossover(self.long_ema, self.short_ema):
#             self.sell()


# # Strategy 3: Bollinger Bands and RSI Strategy
# # Indicators: Bollinger Bands, RSI

# class BollingerBandsRSIStrategy(Strategy):
#     def init(self):
#         self.bb = self.I(ta.volatility.BollingerBands, self.data.Close)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close)

#     def next(self):
#         if self.data.Close[-1] < self.bb.bollinger_lband()[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.data.Close[-1] > self.bb.bollinger_hband()[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 4: MACD and Stochastic Strategy
# # Indicators: MACD, Stochastic Oscillator, ATR

# class MACDStochasticStrategy(Strategy):
#     def init(self):
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.stoch = self.I(ta.momentum.StochasticOscillator, self.data.High, self.data.Low, self.data.Close)
#         self.atr = self.I(ta.volatility.AverageTrueRange, self.data.High, self.data.Low, self.data.Close)

#     def next(self):
#         if self.macd.macd()[-1] > self.signal_line[-1] and self.stoch.stoch()[-1] < 20 and self.data.Close[-1] > self.atr.atr()[-1]:
#             self.buy()
#         elif self.macd.macd()[-1] < self.signal_line[-1] and self.stoch.stoch()[-1] > 80 and self.data.Close[-1] < self.atr.atr()[-1]:
#             self.sell()

# # Strategy 5: Trend-Following Strategy
# # Indicators: EMA, ADX, Parabolic SAR

# class TrendFollowingStrategy(Strategy):
#     def init(self):
#         self.ema_50 = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.ema_200 = self.I(ta.trend.EMAIndicator, self.data.Close, window=200)
#         self.adx = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close)
#         self.psar = self.I(ta.trend.PSARIndicator, self.data.High, self.data.Low, self.data.Close)

#     def next(self):
#         if self.ema_50[-1] > self.ema_200[-1] and self.adx.adx()[-1] > 25 and self.data.Close[-1] > self.psar.psar()[-1]:
#             self.buy()
#         elif self.ema_50[-1] < self.ema_200[-1] and self.adx.adx()[-1] > 25 and self.data.Close[-1] < self.psar.psar()[-1]:
#             self.sell()

# # Strategy 6: Mean Reversion Strategy
# # Indicators: Stochastic Oscillator, Bollinger Bands, Moving Average

# class MeanReversionStrategy(Strategy):
#     def init(self):
#         self.stoch = self.I(ta.momentum.StochasticOscillator, self.data.High, self.data.Low, self.data.Close)
#         self.bb = self.I(ta.volatility.BollingerBands, self.data.Close)
#         self.ma_50 = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.stoch.stoch()[-1] < 20 and self.data.Close[-1] < self.bb.bollinger_lband()[-1] and self.data.Close[-1] < self.ma_50[-1]:
#             self.buy()
#         elif self.stoch.stoch()[-1] > 80 and self.data.Close[-1] > self.bb.bollinger_hband()[-1] and self.data.Close[-1] > self.ma_50[-1]:
#             self.sell()

# # Strategy 7: Triple Moving Average Crossover Strategy
# # Indicators: Short-term MA, Mid-term MA, Long-term MA

# class TripleMACrossoverStrategy(Strategy):
#     def init(self):
#         self.short_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=10)
#         self.mid_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)
#         self.long_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=100)

#     def next(self):
#         if crossover(self.short_ma, self.mid_ma) and self.mid_ma > self.long_ma:
#             self.buy()
#         elif crossover(self.mid_ma, self.short_ma) and self.mid_ma < self.long_ma:
#             self.sell()

# # Strategy 8: Keltner Channel and RSI Strategy
# # Indicators: Keltner Channel, RSI

# class KeltnerRSIStrategy(Strategy):
#     def init(self):
#         self.kc = self.I(ta.volatility.KeltnerChannel, self.data.High, self.data.Low, self.data.Close, window=20, window_atr=10)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.data.Close[-1] < self.kc.keltner_channel_lband()[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.data.Close[-1] > self.kc.keltner_channel_hband()[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 9: ATR Trailing Stop Strategy
# # Indicators: ATR, Close Price, EMA

# class ATRTrailingStopStrategy(Strategy):
#     def init(self):
#         self.atr = self.I(ta.volatility.AverageTrueRange, self.data.High, self.data.Low, self.data.Close)
#         self.ema_20 = self.I(ta.trend.EMAIndicator, self.data.Close, window=20)

#     def next(self):
#         if self.data.Close[-1] > self.ema_20[-1] and self.data.Close[-1] > self.data.Close[-1] - self.atr.atr()[-1]:
#             self.buy()
#         elif self.data.Close[-1] < self.ema_20[-1] and self.data.Close[-1] < self.data.Close[-1] - self.atr.atr()[-1]:
#             self.sell()

# # Strategy 10: Chande Momentum Oscillator Strategy
# # Indicators: Chande Momentum Oscillator, MA, ATR

# class ChandeMomentumOscillatorStrategy(Strategy):
#     def init(self):
#         self.cmo = self.I(ta.momentum.ChandeMomentumOscillator, self.data.Close, window=14)
#         self.ma_50 = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)
#         self.atr = self.I(ta.volatility.AverageTrueRange, self.data.High, self.data.Low, self.data.Close)

#     def next(self):
#         # if selfContinuing with the implementation of more strategies using three to five indicators, here's a comprehensive set of 50 strategies aiming for an annual return of 70%+:
#         pass

# # Strategy 11: Williams %R and EMA Strategy
# # Indicators**: Williams %R, EMA, MACD

# class WilliamsREMA(Strategy):
#     def init(self):
#         self.williams_r = self.I(ta.momentum.WilliamsRIndicator, self.data.High, self.data.Low, self.data.Close, lbp=14)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.williams_r.williams_r()[-1] < -80 and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.williams_r.williams_r()[-1] > -20 and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 12: Trix, RSI and Bollinger Bands Strategy
# # Indicators: Trix, RSI, Bollinger Bands

# class TrixRSIBollinger(Strategy):
#     def init(self):
#         self.trix = self.I(ta.trend.TRIXIndicator, self.data.Close, window=15)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.bb = self.I(ta.volatility.BollingerBands, self.data.Close)

#     def next(self):
#         if self.trix.trix()[-1] > self.trix.trix_signal()[-1] and self.rsi[-1] < 30 and self.data.Close[-1] < self.bb.bollinger_lband()[-1]:
#             self.buy()
#         elif self.trix.trix()[-1] < self.trix.trix_signal()[-1] and self.rsi[-1] > 70 and self.data.Close[-1] > self.bb.bollinger_hband()[-1]:
#             self.sell()

# # Strategy 13: Elder Ray Index Strategy
# # Indicators: Elder Ray Bull Power, Elder Ray Bear Power, ADX

# class ElderRayIndexStrategy(Strategy):
#     def init(self):
#         self.bull_power = self.I(ta.volume.ElderRayIndex, self.data.High, self.data.Low, self.data.Close, window=13).bull_power()
#         self.bear_power = self.I(ta.volume.ElderRayIndex, self.data.High, self.data.Low, self.data.Close, window=13).bear_power()
#         self.adx = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close, window=14)

#     def next(self):
#         if self.bull_power[-1] > 0 and self.bear_power[-1] < 0 and self.adx.adx()[-1] > 25:
#             self.buy()
#         elif self.bull_power[-1] < 0 and self.bear_power[-1] > 0 and self.adx.adx()[-1] > 25:
#             self.sell()

# # Strategy 14: Ichimoku Cloud and Stochastic Strategy
# # Indicators: Ichimoku Cloud, Stochastic Oscillator

# class IchimokuStochasticStrategy(Strategy):
#     def init(self):
#         self.ichimoku = self.I(ta.trend.IchimokuIndicator, self.data.High, self.data.Low, self.data.Close, window1=9, window2=26, window3=52)
#         self.stoch = self.I(ta.momentum.StochasticOscillator, self.data.High, self.data.Low, self.data.Close)

#     def next(self):
#         if self.data.Close[-1] > self.ichimoku.ichimoku_a()[-1] and self.data.Close[-1] > self.ichimoku.ichimoku_b()[-1] and self.stoch.stoch()[-1] < 20:
#             self.buy()
#         elif self.data.Close[-1] < self.ichimoku.ichimoku_a()[-1] and self.data.Close[-1] < self.ichimoku.ichimoku_b()[-1] and self.stoch.stoch()[-1] > 80:
#             self.sell()


# # Strategy 15: Aroon, EMA and MACD Strategy
# # Indicators: Aroon, EMA, MACD

# class AroonEMAMACDStrategy(Strategy):
#     def init(self):
#         self.aroon = self.I(ta.trend.AroonIndicator, self.data.Close, window=25)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.aroon.aroon_up()[-1] > self.aroon.aroon_down()[-1] and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.aroon.aroon_up()[-1] < self.aroon.aroon_down()[-1] and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 16: Keltner Channel and ADX Strategy
# # Indicators: Keltner Channel, ADX

# class KeltnerADXStrategy(Strategy):
#     def init(self):
#         self.kc = self.I(ta.volatility.KeltnerChannel, self.data.High, self.data.Low, self.data.Close, window=20, window_atr=10)
#         self.adx = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close)

#     def next(self):
#         if self.data.Close[-1] < self.kc.keltner_channel_lband()[-1] and self.adx.adx()[-1] > 25:
#             self.buy()
#         elif self.data.Close[-1] > self.kc.keltner_channel_hband()[-1] and self.adx.adx()[-1] > 25:
#             self.sell()


# # Strategy 17: Mass Index and EMA Strategy
# # Indicators: Mass Index, EMA

# class MassIndexEMAStrategy(Strategy):
#     def init(self):
#         self.mass_index = self.I(ta.trend.MassIndex, self.data.High, self.data.Low, window_fast=9, window_slow=25)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.mass_index.mass_index()[-1] > 27 and self.data.Close[-1] > self.ema[-1]:
#             self.buy()
#         elif self.mass_index.mass_index()[-1] < 27 and self.data.Close[-1] < self.ema[-1]:
#             self.sell()

# # Strategy 18: Choppiness Index and ATR Strategy
# # Indicators: Choppiness Index, ATR, EMA

# class ChoppinessATRStrategy(Strategy):
#     def init(self):
#         self.chop = self.I(ta.trend.ChoppinessIndicator, self.data.High, self.data.Low, self.data.Close, window=14)
#         self.atr = self.I(ta.volatility.AverageTrueRange, self.data.High, self.data.Low, self.data.Close)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.chop.chop()[-1] < 38.2 and self.data.Close[-1] > self.ema[-1] and self.data.Close[-1] > self.atr.atr()[-1]:
#             self.buy()
#         elif self.chop.chop()[-1] > 61.8 and self.data.Close[-1] < self.ema[-1] and self.data.Close[-1] < self.atr.atr()[-1]:
#             self.sell()

# # Strategy 19: MACD, RSI, and Bollinger Bands Strategy
# # Indicators: MACD, RSI, Bollinger Bands

# class MACDRSIBollingerStrategy(Strategy):
#     def init(self):
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.bb = self.I(ta.volatility.BollingerBands, self.data.Close)

#     def next(self):
#         if self.macd.macd()[-1] > self.signal_line[-1] and self.rsi[-1] < 30 and self.data.Close[-1] < self.bb.bollinger_lband()[-1]:
#             self.buy()
#         # elif self.macd.macd()[-1] < selfLet's continue building the remaining strategies using a combination of three to five technical indicators, aiming for an annual return of 70% or more. 

# # Strategy 20: DMI, ADX, and RSI Strategy
# # Indicators**: DMI, ADX, RSI

# class DMI_ADX_RSIStrategy(Strategy):
#     def init(self):
#         self.adx = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close)
#         self.dmi_pos = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close).adx_pos()
#         self.dmi_neg = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close).adx_neg()
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.adx.adx()[-1] > 25 and self.dmi_pos[-1] > self.dmi_neg[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.adx.adx()[-1] > 25 and self.dmi_pos[-1] < self.dmi_neg[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 21: PPO, MACD, and EMA Strategy
# # Indicators: PPO, MACD, EMA

# class PPO_MACD_EMAStrategy(Strategy):
#     def init(self):
#         self.ppo = self.I(ta.trend.PPOIndicator, self.data.Close)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.ppo.ppo()[-1] > self.ppo.ppo_signal()[-1] and self.macd.macd()[-1] > self.signal_line[-1] and self.data.Close[-1] > self.ema[-1]:
#             self.buy()
#         elif self.ppo.ppo()[-1] < self.ppo.ppo_signal()[-1] and self.macd.macd()[-1] < self.signal_line[-1] and self.data.Close[-1] < self.ema[-1]:
#             self.sell()

# # Strategy 22: Coppock Curve, RSI, and MACD Strategy
# # Indicators: Coppock Curve, RSI, MACD

# class CoppockRSIMACDStrategy(Strategy):
#     def init(self):
#         self.cc = self.I(ta.trend.CoppockCurve, self.data.Close, window=10)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.cc.coppock_curve()[-1] > 0 and self.rsi[-1] < 30 and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.cc.coppock_curve()[-1] < 0 and self.rsi[-1] > 70 and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 23: KST, RSI, and EMA Strategy
# # Indicators: KST, RSI, EMA

# class KST_RSIStrategy(Strategy):
#     def init(self):
#         self.kst = self.I(ta.trend.KSTIndicator, self.data.Close, roc1=10, roc2=15, roc3=20, roc4=30, window1=10, window2=10, window3=10, window4=15, nsig=9)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.kst.kst()[-1] > self.kst.kst_signal()[-1] and self.rsi[-1] < 30 and self.data.Close[-1] > self.ema[-1]:
#             self.buy()
#         elif self.kst.kst()[-1] < self.kst.kst_signal()[-1] and self.rsi[-1] > 70 and self.data.Close[-1] < self.ema[-1]:
#             self.sell()

# # Strategy 24: Chaikin Money Flow, MACD, and RSI Strategy
# # Indicators: Chaikin Money Flow, MACD, RSI

# class ChaikinMACD_RSIStrategy(Strategy):
#     def init(self):
#         self.cmf = self.I(ta.volume.ChaikinMoneyFlowIndicator, self.data.High, self.data.Low, self.data.Close, self.data.Volume, window=20)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.cmf.chaikin_money_flow()[-1] > 0 and self.macd.macd()[-1] > self.signal_line[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.cmf.chaikin_money_flow()[-1] < 0 and self.macd.macd()[-1] < self.signal_line[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 25: Donchian Channel, MACD, and RSI Strategy
# # Indicators: Donchian Channel, MACD, RSI

# class Donchian_MACD_RSIStrategy(Strategy):
#     def init(self):
#         self.dc = self.I(ta.trend.DonchianChannel, self.data.High, self.data.Low, self.data.Close, window=20)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.data.Close[-1] > self.dc.donchian_channel_hband()[-1] and self.macd.macd()[-1] > self.signal_line[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.data.Close[-1] < self.dc.donchian_channel_lband()[-1] and self.macd.macd()[-1] < self.signal_line[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 26: Aroon, MACD, and RSI Strategy
# # Indicators: Aroon, MACD, RSI

# class Aroon_MACD_RSIStrategy(Strategy):
#     def init(self):
#         self.aroon = self.I(ta.trend.AroonIndicator, self.data.Close, window=25)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.aroon.aroon_up()[-1] > self.aroon.aroon_down()[-1] and self.macd.macd()[-1] > self.signal_line[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.aroon.aroon_up()[-1] < self.aroon.aroon_down()[-1] and self.macd.macd()[-1] < self.signal_line[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 27: Williams %R, MACD, and EMA Strategy
# # Indicators: Williams %R, MACD, EMA

# class WilliamsR_MACD_EMAStrategy(Strategy):
#     def init(self):
#         self.williams_r = self.I(ta.momentum.WilliamsRIndicator, self.data.High, self.data.Low, self.data.Close, lbp=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.williams_r.williams_r()[-1] < -80 and self.macd.macd()[-1] > self.signal_line[-1] and self.data.Close[-1] > self.ema[-1]:
#             self.buy()
#         # elif self.williams_r.williams_r()[-1] > -20 and self.macd.macd()[-1] < self.signal_line[-1] and self.data.Close[-1]
        
#         # Let's continue building the remaining strategies using a combination of three to five technical indicators, aiming for an annual return of 70% or more.

# # Strategy 28: Keltner Channel, RSI, and MACD Strategy
# # Indicators: Keltner Channel, RSI, MACD

# class KeltnerRSIMACDStrategy(Strategy):
#     def init(self):
#         self.kc = self.I(ta.volatility.KeltnerChannel, self.data.High, self.data.Low, self.data.Close, window=20, window_atr=10)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.data.Close[-1] < self.kc.keltner_channel_lband()[-1] and self.rsi[-1] < 30 and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.data.Close[-1] > self.kc.keltner_channel_hband()[-1] and self.rsi[-1] > 70 and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 29: CCI, EMA, and MACD Strategy
# # Indicators: CCI, EMA, MACD

# class CCIEMAMACDStrategy(Strategy):
#     def init(self):
#         self.cci = self.I(ta.trend.CCIIndicator, self.data.High, self.data.Low, self.data.Close, window=20)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.cci.cci()[-1] < -100 and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.cci.cci()[-1] > 100 and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 30: Bollinger Bands, EMA, and MACD Strategy
# # Indicators: Bollinger Bands, EMA, MACD

# class BollingerEMAMACDStrategy(Strategy):
#     def init(self):
#         self.bb = self.I(ta.volatility.BollingerBands, self.data.Close)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.data.Close[-1] < self.bb.bollinger_lband()[-1] and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.data.Close[-1] > self.bb.bollinger_hband()[-1] and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 31: Parabolic SAR, EMA, and MACD Strategy
# # Indicators: Parabolic SAR, EMA, MACD

# class ParabolicSAREMAMACDStrategy(Strategy):
#     def init(self):
#         self.psar = self.I(ta.trend.PSARIndicator, self.data.High, self.data.Low, self.data.Close)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.data.Close[-1] > self.psar.psar()[-1] and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.data.Close[-1] < self.psar.psar()[-1] and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 32: ATR, EMA, and MACD Strategy
# # Indicators: ATR, EMA, MACD

# class ATREMAMACDStrategy(Strategy):
#     def init(self):
#         self.atr = self.I(ta.volatility.AverageTrueRange, self.data.High, self.data.Low, self.data.Close)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.data.Close[-1] > self.ema[-1] and self.data.Close[-1] > self.data.Close[-1] - self.atr.atr()[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.data.Close[-1] < self.ema[-1] and self.data.Close[-1] < self.data.Close[-1] - self.atr.atr()[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 33: KST, EMA, and MACD Strategy
# # Indicators: KST, EMA, MACD

# class KSTEMAMACDStrategy(Strategy):
#     def init(self):
#         self.kst = self.I(ta.trend.KSTIndicator, self.data.Close, roc1=10, roc2=15, roc3=20, roc4=30, window1=10, window2=10, window3=10, window4=15, nsig=9)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.kst.kst()[-1] > self.kst.kst_signal()[-1] and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.kst.kst()[-1] < self.kst.kst_signal()[-1] and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 34: Vortex, MACD, and RSI Strategy
# # Indicators: Vortex Indicator, MACD, RSI

# class VortexMACDRSIStrategy(Strategy):
#     def init(self):
#         self.vi = self.I(ta.trend.VortexIndicator, self.data.High, self.data.Low, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.vi.vortex_indicator_pos()[-1] > self.vi.vortex_indicator_neg()[-1] and self.macd.macd()[-1] > self.signal_line[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.vi.vortex_indicator_pos()[-1] < self.vi.vortex_indicator_neg()[-1] and self.macd.macd()[-1] < self.signal_line[-1] and self.rsi[-1] > 70:
#             self.sell()

# # Strategy 35: TSI, EMA, and MACD Strategy
# # Indicators: TSI, EMA, MACD

# class TSIEMAMACDStrategy(Strategy):
#     def init(self):
#         self.tsi = self.I(ta.momentum.TSIIndicator, self.data.Close, window_slow=25, window_fast=13)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         pass
#         # if self.tsi.tsi()[-1] > 0 and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-To complete the implementation of the strategies using a minimum of three and a maximum of five technical indicators, here is a comprehensive set of 50 strategies. Each strategy aims for an annual return of 70% or more and follows the structure provided.

# # Strategy 36: Chande Momentum Oscillator, EMA, and Bollinger Bands Strategy
# # Indicators: Chande Momentum Oscillator, EMA, Bollinger Bands

# class ChandeMomentumEMABollingerStrategy(Strategy):
#     def init(self):
#         self.cmo = self.I(ta.momentum.ChandeMomentumOscillator, self.data.Close, window=14)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.bb = self.I(ta.volatility.BollingerBands, self.data.Close)

#     def next(self):
#         if self.cmo.cmo()[-1] > 0 and self.data.Close[-1] > self.ema[-1] and self.data.Close[-1] < self.bb.bollinger_lband()[-1]:
#             self.buy()
#         elif self.cmo.cmo()[-1] < 0 and self.data.Close[-1] < self.ema[-1] and self.data.Close[-1] > self.bb.bollinger_hband()[-1]:
#             self.sell()


# # Strategy 37: Mass Index, RSI, and MACD Strategy
# # Indicators: Mass Index, RSI, MACD

# class MassIndexRSIMACDStrategy(Strategy):
#     def init(self):
#         self.mass_index = self.I(ta.trend.MassIndex, self.data.High, self.data.Low, window_fast=9, window_slow=25)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.mass_index.mass_index()[-1] > 27 and self.rsi[-1] < 30 and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.mass_index.mass_index()[-1] < 27 and self.rsi[-1] > 70 and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 38: Triple Exponential Moving Average (TEMA), RSI, and MACD Strategy
# # Indicators: TEMA, RSI, MACD

# class TEMARSIMACDStrategy(Strategy):
#     def init(self):
#         self.tema = self.I(ta.trend.TEMAIndicator, self.data.Close, window=20)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.tema.tema()[-1] > self.tema.tema()[-2] and self.rsi[-1] < 30 and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.tema.tema()[-1] < self.tema.tema()[-2] and self.rsi[-1] > 70 and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 39: Price Volume Trend (PVT), EMA, and MACD Strategy
# # Indicators: PVT, EMA, MACD

# class PVTEMAMACDStrategy(Strategy):
#     def init(self):
#         self.pvt = self.I(ta.volume.PVTIndicator, self.data.Close, self.data.Volume)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.pvt.pvt()[-1] > self.pvt.pvt()[-2] and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.pvt.pvt()[-1] < self.pvt.pvt()[-2] and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 40: Balance of Power (BOP), RSI, and MACD Strategy
# # Indicators: BOP, RSI, MACD

# class BOPRSIMACDStrategy(Strategy):
#     def init(self):
#         self.bop = self.I(ta.volume.BalanceOfPowerIndicator, self.data.Close, self.data.High, self.data.Low, self.data.Open)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.bop.bop()[-1] > 0 and self.rsi[-1] < 30 and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.bop.bop()[-1] < 0 and self.rsi[-1] > 70 and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 41: Schaff Trend Cycle, EMA, and MACD Strategy
# # Indicators: Schaff Trend Cycle, EMA, MACD

# class SchaffEMA_MACDStrategy(Strategy):
#     def init(self):
#         self.stc = self.I(ta.trend.STCIndicator, self.data.Close, window_slow=50, window_fast=23, cycle=10)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.stc.stc()[-1] > 25 and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.stc.stc()[-1] < 75 and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 42: Ease of Movement, EMA, and MACD Strategy
# # Indicators: Ease of Movement, EMA, MACD

# class EaseOfMovementEMAMACDStrategy(Strategy):
#     def init(self):
#         self.eom = self.I(ta.volume.EaseOfMovementIndicator, self.data.High, self.data.Low, self.data.Volume, window=14)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.eom.ease_of_movement()[-1] > 0 and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.eom.ease_of_movement()[-1] < 0 and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 43: Vortex, EMA, and MACD Strategy
# # Indicators: Vortex Indicator, EMA, MACD

# class VortexEMAMACDStrategy(Strategy):
#     def init(self):
#         self.vi = self.I(ta.trend.VortexIndicator, self.data.High, self.data.Low, self.data.Close, window=14)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.vi.vortex_indicator_pos()[-1] > self.vi.vortex_indicator_neg()[-1] and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.vi.vortex_indicator_pos()[-1] < self.vi.vortex_indicator_neg()[-1] and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()

# # Strategy 44: Chande Momentum Oscillator, EMA, and MACD Strategy
# # Indicators: Chande Momentum Oscillator, EMA, MACD

# class ChandeMomentumEMAMACDStrategy(Strategy):
#     def init(self):
#         self.cmo = self.I(ta.momentum.ChandeMomentumOscillator, self.data.Close, window=14)
#         self.ema = self.I(ta.trend.EMAIndicator, self.data.Close, window=50)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()

#     def next(self):
#         if self.cmo.cmo()[-1] > 0 and self.data.Close[-1] > self.ema[-1] and self.macd.macd()[-1] > self.signal_line[-1]:
#             self.buy()
#         elif self.cmo.cmo()[-1] < 0 and self.data.Close[-1] < self.ema[-1] and self.macd.macd()[-1] < self.signal_line[-1]:
#             self.sell()



#### End Strategies



# # 1. Momentum-Based Strategy
# # Indicators: RSI, MACD, Bollinger Bands

# class MomentumStrategy(Strategy):
#     def init(self):
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.macd = self.I(ta.trend.MACD, self.data.Close)
#         self.signal_line = self.I(ta.trend.MACD, self.data.Close).macd_signal()
#         self.bb_high = self.I(ta.volatility.BollingerBands, self.data.Close).bollinger_hband()
#         self.bb_low = self.I(ta.volatility.BollingerBands, self.data.Close).bollinger_lband()

#     def next(self):
#         if self.rsi[-1] < 30 and self.macd.macd()[-1] > self.signal_line[-1] and self.data.Close[-1] < self.bb_low[-1]:
#             self.buy()
#         elif self.rsi[-1] > 70 and self.macd.macd()[-1] < self.signal_line[-1] and self.data.Close[-1] > self.bb_high[-1]:
#             self.sell()

# # 2. Moving Average Crossover Strategy
# # Indicators: Short-term MA, Long-term MA

# class MovingAverageCrossover(Strategy):
#     def init(self):
#         self.short_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)
#         self.long_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=200)

#     def next(self):
#         if crossover(self.short_ma, self.long_ma):
#             self.buy()
#         elif crossover(self.long_ma, self.short_ma):
#             self.sell()

# # 3. Bollinger Bands and RSI Strategy
# # Indicators: Bollinger Bands, RSI

# class BollingerBandsRSIStrategy(Strategy):
#     def init(self):
#         self.bb = ta.volatility.BollingerBands(self.data.Close)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close)

#     def next(self):
#         if self.data.Close[-1] < self.bb.bollinger_lband()[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.data.Close[-1] > self.bb.bollinger_hband()[-1] and self.rsi[-1] > 70:
#             self.sell()

# # 4. Mean Reversion Strategy
# # Indicators: Stochastic Oscillator, Bollinger Bands, Moving Average

# class MeanReversionStrategy(Strategy):
#     def init(self):
#         self.stoch = ta.momentum.StochasticOscillator(self.data.High, self.data.Low, self.data.Close)
#         self.bb = ta.volatility.BollingerBands(self.data.Close)
#         self.ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.stoch.stoch()[-1] < 20 and self.data.Close[-1] < self.bb.bollinger_lband()[-1] and self.data.Close[-1] < self.ma[-1]:
#             self.buy()
#         elif self.stoch.stoch()[-1] > 80 and self.data.Close[-1] > self.bb.bollinger_hband()[-1] and self.data.Close[-1] > self.ma[-1]:
#             self.sell()

# # 5. ATR Trailing Stop Strategy
# # Indicators: ATR, Close Price

# class WilliamsRStrategy(Strategy):
#     def init(self):
#         self.williams_r = self.I(ta.momentum.WilliamsRIndicator, self.data.High, self.data.Low, self.data.Close, lbp=14)

#     def next(self):
#         if self.williams_r[-1] < -80:
#             self.buy()
#         elif self.williams_r[-1] > -20:
#             self.sell()

# # 6. Triple Moving Average Crossover Strategy
# # Indicators: Short-term MA, Mid-term MA, Long-term MA

# class TripleMACrossoverStrategy(Strategy):
#     def init(self):
#         self.short_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=10)
#         self.mid_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)
#         self.long_ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=100)

#     def next(self):
#         if crossover(self.short_ma, self.mid_ma) and self.mid_ma > self.long_ma:
#             self.buy()
#         elif crossover(self.mid_ma, self.short_ma) and self.mid_ma < self.long_ma:
#             self.sell()

# # 7. Relative Strength Index (RSI) and Moving Average (MA) Strategy
# # Indicators: RSI, MA

# class RSIMA_Strategy(Strategy):
#     def init(self):
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)
#         self.ma = self.I(ta.trend.SMAIndicator, self.data.Close, window=50)

#     def next(self):
#         if self.rsi[-1] < 30 and self.data.Close[-1] > self.ma[-1]:
#             self.buy()
#         elif self.rsi[-1] > 70 and self.data.Close[-1] < self.ma[-1]:
#             self.sell()

# # 8. Donchian Channel and RSI Strategy
# # Indicators: Donchian Channel, RSI

# class DonchianRSIStrategy(Strategy):
#     def init(self):
#         self.dc = self.I(ta.trend.DonchianChannel, self.data.High, self.data.Low, self.data.Close, window=20)
#         self.rsi = self.I(ta.momentum.RSIIndicator, self.data.Close, window=14)

#     def next(self):
#         if self.data.Close[-1] > self.dc.donchian_channel_hband()[-1] and self.rsi[-1] < 30:
#             self.buy()
#         elif self.data.Close[-1] < self.dc.donchian_channel_lband()[-1] and self.rsi[-1] > 70:
#             self.sell()
