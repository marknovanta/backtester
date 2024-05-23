from flask import Flask, render_template
import os
import webbrowser
from threading import Timer
from backtest import get_info
from watchlist import tickers_invest, tickers_swing
from find_tickers import get_tickers
from itertools import islice


def chunked(iterable, chunk_size):
    """Yield successive n-sized chunks from iterable."""
    iterable = iter(iterable)
    while True:
        chunk = list(islice(iterable, chunk_size))
        if not chunk:
            break
        yield chunk


operativity = input('Invest(i) or swing(s)? ')
interval = input('What interval? (1wk, 1mo) ')
# interval = '1mo'
if operativity == 'i':
    info = get_info(tickers_invest, interval)
elif operativity == 's':
    #info = get_info(tickers_swing, interval)
    tickers = get_tickers()
    if len(tickers) > 150:
        chunk_size = 121
        info = []
        for chunk in chunked(tickers, chunk_size):
            i = get_info(chunk, interval)
            for x in i:
                info.append(x)
    else:
        info = get_info(tickers, interval)
    print(len(info))

app = Flask(__name__)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def index():
    data = []
    for i in info:
        if i['cagr'] > 0.03 and i['period'] >= 10:
            data.append(i)
    return render_template('index.html', info=data, interval=interval)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=port)