import requests
import time
from vnstock import Vnstock
from datetime import timedelta
import pandas as pd

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

            # If data is too old -> raise error -> will be caught below
            stk['time'] = pd.to_datetime(stk['time'])  # ensure datetime format
            last_time = stk['time'].iloc[-1]
            now = pd.Timestamp.now()

            if (now - last_time) > timedelta(minutes=10):
                raise ValueError("Data is too old (>10 minutes).")

            # If no data or dataframe is empty -> raise error -> will be caught below
            if stk is None or stk.empty:
                raise ValueError("No data available right now.")

            last_buy = stk[stk['match_type'] == 'Buy'].iloc[-1]
            last_sell = stk[stk['match_type'] == 'Sell'].iloc[-1]

            # If no buy or sell transactions -> raise error -> will be caught below
            if last_buy.empty or last_sell.empty:
                raise ValueError("No Buy/Sell data available right now.")

            last_buy_price = float(last_buy['price'].iloc[0])
            last_sell_price = float(last_sell['price'].iloc[0])
            last_buy_vol = float(last_buy['volume'].iloc[0])
            last_sell_vol = float(last_sell['volume'].iloc[0])

            send_telegram_message(
                f"Time: {last_time}:\n{symbol} Buy: {last_buy_price}, Vol: {last_buy_vol}\nSell: {last_sell_price}, Vol: {last_sell_vol}",
                BOT_TOKEN,
                CHAT_ID
            )

        except Exception as e:
            # Any error or missing data -> print error -> sleep 600s -> retry
            print(f"Error or No Data: {e}")

        # Always sleep 600 seconds after each run (success or error), then retry
        time.sleep(600)
if __name__ == "__main__":
    run_bot()