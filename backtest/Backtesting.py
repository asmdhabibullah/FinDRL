from backtesting import Backtest
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show, output_file

class DynamicBacktest:
    def __init__(self, data):
        self.data = data

    # def backtest(data):
    #     return {"result": "success", "data_summary": data.describe()}

    # def plot_data(data):
    #     p = figure(x_axis_type="datetime", title="Stock Prices")
    #     p.line(data.index, data['Close'], legend_label='Close Price', line_width=2)
        
    #     # Configure the DatetimeTickFormatter
    #     p.xaxis.formatter = DatetimeTickFormatter(
    #         days="%d %b",
    #         months="%b %Y",
    #         years="%Y"
    #     )
        
    #     output_file("stock_prices.html")
    #     show(p)
            # Generate the plot
        # plot = bt.plot(plot_volume=False, resample=True)

        # # # Customize the plot using Bokeh
        # plot.xaxis.formatter = DatetimeTickFormatter(days="%d %b", months="%d %b %Y", years="%d %b %Y")
        # show(plot)

    def run_backtest(self, strategy_class, custom_params):
        bt = Backtest(self.data, strategy_class, **custom_params)
        output = bt.run()
        bt.plot()
        return output
