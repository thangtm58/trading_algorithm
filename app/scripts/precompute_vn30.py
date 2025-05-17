from vnstock import Listing
from app.models.info import StockInfo
from app.services.cache_utils import get_cached_result

def precompute():
    vn30_symbols = Listing().symbols_by_group("VN30").to_list()

    for symbol in vn30_symbols:
        print(f"[+] Caching {symbol}...")
        stock = StockInfo(symbol)
        get_cached_result(symbol, 'forecast_garch', stock.forecast_garch)

if __name__ == "__main__":
    precompute()
