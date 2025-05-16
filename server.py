from flask import Flask, render_template
from waitress import serve
# from news import get_news
from historical_price import plot_historical_price
from info import StockInfo
from flask import request  
from vnstock import Listing

app = Flask(__name__)

# Get all stock symbols
valid_symbols = Listing().stock()['ticker'].tolist()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    symbol = request.args.get('symbol').upper()

    # If the symbol is empty, return the index page
    if not bool(symbol.strip()):
        return render_template('index.html', error_message="Please enter a valid symbol.")
    
    # If the symbol is not valid, return the index page
    if symbol not in valid_symbols:
        return render_template('index.html', error_message=f"'{symbol}' is not a valid symbol. Please try again.")
    
    stock_info = StockInfo(symbol)
    return render_template(
        'info.html',
        symbol=symbol,
        forecast=stock_info.forecast_garch()
    )

"""
@app.route('/news')
def news():
    return render_template('news.html', news=get_news()

@app.route('/historical_price')
def historical_price():
    return render_template(
        'historical_price.html', 
        historical_graph=plot_historical_price()
    )
"""

if __name__ == '__main__':
    print("Starting server...")
    serve(app, host='0.0.0.0', port=8000, threads=4)