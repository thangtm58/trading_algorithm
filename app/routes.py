from flask import render_template, request, Blueprint
from app.models.info import StockInfo
from vnstock import Listing
from app.services.cache_utils import get_cached_result

# Get all stock symbols
valid_symbols = Listing().all_symbols()['symbol'].tolist()

routes = Blueprint('routes', __name__)

# All routes
@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html')

@routes.route('/info')
def info():
    symbol = request.args.get('symbol').upper()

    # If the symbol is empty, return the index page
    if not bool(symbol.strip()):
        return render_template('index.html', error_message="Please enter a valid symbol.")
    
    # If the symbol is not valid, return the index page
    if symbol not in valid_symbols:
        return render_template('index.html', error_message=f"'{symbol}' is not a valid symbol. Please try again.")

    # Stock info
    stock_info = StockInfo(symbol)

    # Get cached result
    garch_forecast = get_cached_result(symbol, 'forecast_garch', stock_info.forecast_garch)

    return render_template(
        'info.html',
        symbol=symbol,
        company_name=stock_info.company_name,
        forecast=garch_forecast
    )