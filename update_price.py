import requests
import time
from vnstock import Vnstock

# Set symbol
symbol = 'VCB'
stock = Vnstock().stock(symbol=symbol, source='VCI')

TOKEN = '8092343811:AAFMv0H6H6W0B1q2vwvoI5BNmCdMyC3rrHkK'
CHAT_ID = '817649025'
BOT_TOKEN = TOKEN

def send_telegram_message(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=payload)
    return response

def run_bot():
    while True:
        try:
            # Try to fetch intraday data
            stk = stock.quote.intraday(symbol=symbol, to_df=True)

            # If no data or dataframe is empty -> raise error -> will be caught below
            if stk is None or stk.empty:
                raise ValueError("No data available right now.")

            last_buy = stk[stk['match_type'] == 'Buy'].tail(1)
            last_sell = stk[stk['match_type'] == 'Sell'].tail(1)

            # If no buy or sell transactions -> raise error -> will be caught below
            if last_buy.empty or last_sell.empty:
                raise ValueError("No Buy/Sell data available right now.")

            last_buy_price = float(last_buy['price'].iloc[0])
            last_sell_price = float(last_sell['price'].iloc[0])

            send_telegram_message(
                f"{symbol} Buy: {last_buy_price} Sell: {last_sell_price}",
                BOT_TOKEN,
                CHAT_ID
            )

        except Exception as e:
            # Any error or missing data -> print error -> sleep 600s -> retry
            print(f"Error or No Data: {e}")

        # Always sleep 600 seconds after each run (success or error), then retry

if __name__ == "__main__":
    run_bot()