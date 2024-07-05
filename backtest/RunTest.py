from backtest.Backtesting import DynamicBacktest
from indicators.Indicators import MomentumIndicators
from strategies import SmaCross, FlatTopBreakout, EnhancedFlatTopBreakout, BreakoutBuildup, MomentumSRMStrategy

def do_backtesting(data):
    
    print("Backtesting data...")
    print(data.head(5))

    backtester = DynamicBacktest(data)

    # Custom backtest parameters
    custom_params = {
        'cash': 10000,
        'commission': 0.002,
        'exclusive_orders': True,
        'trade_on_close': True
    }

    # Create an instance of the MomentumIndicators class
    # indicators = MomentumIndicators(data)
    # Set the indicators for the strategy
    # EnhancedFlatTopBreakout.indicators = MomentumIndicators

    print(f"Running backtest for {SmaCross.__name__}...")

    output = backtester.run_backtest(SmaCross, custom_params)
    
    print(f"{SmaCross.__name__}: {output}")

    print("Strategies have been run.")







    

    # strategies = [
    #  SmaCross, EnhancedFlatTopBreakout
        #   MomentumStrategy, MovingAverageCrossoverStrategy, BollingerBandsRSIStrategy, MACDStochasticStrategy, TrendFollowingStrategy, MeanReversionStrategy, TripleMACrossoverStrategy, KeltnerRSIStrategy,  ATRTrailingStopStrategy, ChandeMomentumOscillatorStrategy, WilliamsREMA, TrixRSIBollinger, ElderRayIndexStrategy, IchimokuStochasticStrategy, AroonEMAMACDStrategy, KeltnerADXStrategy, MassIndexEMAStrategy, ChoppinessATRStrategy, MACDRSIBollingerStrategy, DMI_ADX_RSIStrategy, PPO_MACD_EMAStrategy, CoppockRSIMACDStrategy, KST_RSIStrategy, ChaikinMACD_RSIStrategy, Donchian_MACD_RSIStrategy, Aroon_MACD_RSIStrategy, WilliamsR_MACD_EMAStrategy, KeltnerRSIMACDStrategy, CCIEMAMACDStrategy, BollingerEMAMACDStrategy, ParabolicSAREMAMACDStrategy, ATREMAMACDStrategy, KSTEMAMACDStrategy, VortexMACDRSIStrategy, TSIEMAMACDStrategy, ChandeMomentumEMABollingerStrategy, MassIndexRSIMACDStrategy, TEMARSIMACDStrategy, PVTEMAMACDStrategy, BOPRSIMACDStrategy, SchaffEMA_MACDStrategy, EaseOfMovementEMAMACDStrategy, VortexEMAMACDStrategy, ChandeMomentumEMAMACDStrategy
    # ]

    # Custom backtest parameters
    # custom_params = {
    #     'return_tickers': True,
    #     'maximize_cash': False,
    #     'stop_loss': 0.05,
    #     'take_profit': 0.10,
    #     'slippage': 0.01,
    #     'cash': 10000,
    #     'commission': 0.002,
    #     'exclusive_orders': True,
    #     'hedging': False,
    #     'trade_on_close': True,
    #     'margin': 0.5,
    #     'max_open_trades': 5,
    #     'fixed_commission': 1.0,
    #     'risk_free_rate': 0.01,
    #     'drawdown': 0.2,
    #     'volatility_target': 0.1,
    #     'position_size': 0.05,
    #     'trade_frequency': 5,
    #     'time_in_market': 0.8,
    #     'max_holding_time': 10,
    #     'min_holding_time': 3,
    #     'reinvest_profits': True,
    #     'initial_leverage': 2.0,
    #     'transaction_cost': 0.0005
    # }

    # sleeper, strategies_len = 0,  len(strategies)
    # results = []

    # for index, strategy in enumerate(strategies):
    #     print(f"Running backtest for {strategy.__name__}...")
    #     output = backtester.run_backtest(strategy, custom_params)
    #     # backtester.run_backtest(strategy, custom_params)
    #     # results.append((strategy.__name__, output, plot_filename))
        
    #     print(f"{strategy.__name__}: {output}")
        
    #     sleeper += 1
    #     if sleeper % 5 == 0:
    #         print("Sleeping for 30 seconds to avoid rate limits...")
    #         sleep(30)
    #         sleeper = 0


    # Create the PDF report
    # pdf_report = PDFReport(results)
    # pdf_report.create_pdf()
