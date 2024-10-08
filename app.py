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

# -------------- INPUTS --------------------------

automation = input('AUTO(a) or MANUAL(m)? ')
operativity = input('INVEST(i) or SWING(s)? ')
interval = input('What interval? (1d, 1wk, 1mo) ')
#period = int(input('Moving Average period? '))
period = 10 #MOVING AVERAGE PERIOD
#charts = input('Plot balances? (y/n) ')
charts = 'n'

# AUTO SWING => price less than $100
# AUTO INVEST => price > $1

# SET MKT CAP BASED ON OPERATIVITY
if automation == 'a':
    if operativity == 'i':
        cap = 60000000000 # market cap filter (top min 60000000000, normal min 800000000)
    elif operativity == 's':
        cap = 800000000

# -------------------------------------------------

if charts == 'y':
    balance_plot = True #BALANCE PLOTTING ON/OFF
elif charts == 'n':
    balance_plot = False

if operativity == 'i' and automation == 'm':
    info = get_info(tickers_invest, interval, period)
    cap = 0

elif operativity == 's' and automation == 'm':
    info = get_info(tickers_swing, interval, period)

# IF LIST TOO LONG, PROCESS IT IN BUNCHES
elif automation == 'a':
    tickers = get_tickers(operativity)
    if len(tickers) > 150:
        chunk_size = 150
        info = []
        for chunk in chunked(tickers, chunk_size):
            i = get_info(chunk, interval, period)
            for x in i:
                info.append(x)
    else:
        info = get_info(tickers, interval, period)
    print(len(info))

app = Flask(__name__)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def index():
    data = []
    for i in info:
        c1 = True
        #c1 = i['cagr'] > 0 # 0.03 to cover inflation
        c2 = i['period'] >= 0
        c3 = i['mkt_cap'] >= cap

        if c1 and c2 and c3:
            data.append(i)

            # GENERATE PNG OF BALANCE HISTORY
            if i['entry'] == 'entry' and balance_plot:
                t = i['ticker']
                cagr = round(i['cagr']*100,1)
                yld = round(i['yield']*100,1)
                # Create the plot
                plt.plot(i['balance_hist'])
                plt.xlabel('Trades')
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