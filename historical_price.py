from vnstock import Vnstock
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt


def get_historical_price(symbol="VCB"):
    stock = Vnstock().stock(symbol=symbol, source='VCI')
    stk = stock.quote.history(
        start='2025-01-01', 
        end=datetime.today().strftime("%Y-%m-%d"), 
        to_df=True
        )
    return stk

def plot_historical_price(symbol="VCB"):
    df = get_historical_price(symbol)

    df['date'] = pd.to_datetime(df['time'])  # Giữ nguyên datetime64[ns]
    df.sort_values(by='date', inplace=True)
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['close'],
        mode='lines'
        # , name='Close'
    ))
    fig.update_layout(
        title=f"{symbol} Historical Price",
        xaxis_title="Date",
        yaxis_title="Close",
        template="plotly_white",
        margin=dict(l=40, r=20, t=40, b=40)
    )

    # Ensure datetime is serialized properly
    graphJSON = plotly.io.to_json(fig)
    return graphJSON
    """

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['date'], df['close'], label='Close')
    ax.set_title(f"{symbol} Historical Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close")
    ax.legend()
    fig.tight_layout()
    return fig


if __name__ == '__main__':
    print(get_historical_price().head(20))

    """ Test 
    df = get_historical_price()
    df['date'] = df['time'].dt.date
    df.sort_values(by='date', inplace=True)
    print(df.head(20))
    print(df.tail(20))
    print(df['close'].dtypes)
    print(df['date'].dtypes)
    """