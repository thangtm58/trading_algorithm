from flask import Flask, render_template
from waitress import serve
# from news import get_news
from historical_price import plot_historical_price

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


"""
@app.route('/news')
def news():
    return render_template('news.html', news=get_news())
"""

@app.route('/historical_price')
def historical_price():
    return render_template(
        'historical_price.html', 
        historical_graph=plot_historical_price()
    )

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)