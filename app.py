from flask import Flask, render_template
import os
import webbrowser
from threading import Timer
from backtest import get_info
from watchlist import tickers_invest, tickers_swing
from find_tickers import get_tickers
from itertools import islice
import matplotlib.pyplot as plt


def chunked(iterable, chunk_size):
    """Yield successive n-sized chunks from iterable."""
    iterable = iter(iterable)
    while True:
        chunk = list(islice(iterable, chunk_size))
        if not chunk:
            break
        yield chunk

automation = input('AUTO(a) or MANUAL(m)? ')
operativity = input('INVEST(i) or SWING(s)? ')
interval = input('What interval? (1wk, 1mo) ')
balance_plot = False #BALANCE PLOTTING ON/OFF

if operativity == 'i' and automation == 'm':
    info = get_info(tickers_invest, interval)

elif operativity == 's' and automation == 'm':
    info = get_info(tickers_swing, interval)

elif automation == 'a':
    tickers = get_tickers(operativity)
    if len(tickers) > 150:
        chunk_size = 150
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
        c1 = i['cagr'] > 0.03
        c2 = i['period'] >= 10

        if c1 and c2:
            data.append(i)

            # GENERATE PNG OF BALANCE HISTORY
            if i['entry'] == 'entry' and balance_plot:
                t = i['ticker']
                cagr = round(i['cagr']*100,1)
                yld = round(i['yield']*100,1)
                # Create the plot
                plt.plot(i['balance_hist'])
                plt.xlabel('Time')
                plt.ylabel('Balance')
                plt.title(f'{t} {interval} - CAGR:{cagr}% YIELD:{yld}%')

                # Save the plot as PNG
                plt.savefig(f'charts/{t}_{interval}.png', format='png')

                # Close the plot
                plt.close()


    return render_template('index.html', info=data, interval=interval)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=port)