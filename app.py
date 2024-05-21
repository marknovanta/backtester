from flask import Flask, render_template
import os
import webbrowser
from threading import Timer
from backtest import get_info
from watchlist import tickers_invest, tickers_swing

answer = input('Invest(i) or swing(s)? ')
if answer == 'i':
    info = get_info(tickers_invest)
elif answer == 's':
    info = get_info(tickers_swing)

app = Flask(__name__)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def index():
    return render_template('index.html', info=info)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=port)