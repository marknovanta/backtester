from flask import Flask, render_template
import os
import webbrowser
from threading import Timer
from backtest import get_info
from watchlist import tickers_invest, tickers_swing
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('api_key')



operativity = input('Invest(i) or swing(s)? ')
interval = input('What interval? (1wk, 1mo) ')
# interval = '1mo'
if operativity == 'i':
    info = get_info(tickers_invest, interval)
elif operativity == 's':
    info = get_info(tickers_swing, interval)

app = Flask(__name__)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def index():
    data = []
    for i in info:
        if i['cagr'] > 0.03 and i['period'] >= 10:
            data.append(i)
    return render_template('index.html', info=data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=port)