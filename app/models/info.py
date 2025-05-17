from dotenv import load_dotenv
from pprint import pprint
from vnstock import Vnstock, Listing
from datetime import datetime
from arch import arch_model
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd

load_dotenv()

# Get the company name for each symbol
df = Listing().all_symbols()
symbol_to_name = dict(zip(df['symbol'], df['organ_name']))

class StockInfo:
    def __init__(self, symbol):
        self.symbol = symbol
        self.company_name = symbol_to_name[symbol]
        self.historical_price = Vnstock().stock(symbol=symbol, source='VCI').quote.history(
            start='2019-01-01', 
            end=datetime.today().strftime("%Y-%m-%d"), 
            to_df=True
        )
        self.historical_price['date'] = pd.to_datetime(self.historical_price['time'])
        self.historical_price = self.historical_price.sort_values(by='date', ascending=True)

    def plot_historical_price(self):

        trace = go.Scatter(
            x=self.historical_price['date'],
            y=self.historical_price['close'],
            mode='lines',
            name=self.symbol
        )

        layout = go.Layout(
            title=f"Price Chart for {self.symbol}",
            xaxis=dict(title='Date'),
            yaxis=dict(title='Close Price (VND)'),
            template='plotly_white'
        )

        fig = go.Figure(data=[trace], layout=layout)
        
        # Return HTML div string
        return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    def forecast_garch(self, steps=20):
        # Calculate log returns from price and rescale by 100
        log_returns = np.log(self.historical_price['close'] / self.historical_price['close'].shift(1)).dropna() * 100

        # Fit the GARCH(1,1) model to rescaled log returns
        model = arch_model(log_returns, vol='Garch', p=1, q=1)
        garch_fit = model.fit(disp='off')

        # Forecast the next steps
        forecast_horizon = steps
        garch_forecast = garch_fit.forecast(horizon=forecast_horizon)

        # Get the forecasted mean and variance (volatility), and rescale back
        mean_forecast = garch_forecast.mean.iloc[-1].values / 100
        variance_forecast = garch_forecast.variance.iloc[-1].values / (100**2)
        vol_forecast = np.sqrt(variance_forecast)

        # Simulate possible log return paths (using mean and volatility)
        simulated_log_returns = np.random.normal(loc=mean_forecast, scale=vol_forecast, size=forecast_horizon)
        # simulated_log_returns = mean_forecast


        # Convert forecasted log returns to price path
        last_price = self.historical_price['close'].iloc[-1]
        forecasted_prices = [last_price]
        for r in simulated_log_returns:
            forecasted_prices.append(forecasted_prices[-1] * np.exp(r))
        forecasted_prices = forecasted_prices[1:]  # Remove the initial last_price

        return forecasted_prices
    
if __name__ == "__main__":
    stock_info = StockInfo("VCB")
    print(stock_info.forecast_garch())