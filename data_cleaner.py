import csv
import yfinance as yf

def clean_data(ticker):

    print(f'Processing {ticker} ...')
    ticker = yf.Ticker(ticker)

    data = ticker.history(period='max', interval='1mo', prepost=True, auto_adjust=False, actions=False)
    data_closing = []
    for d in data['Close']:
        data_closing.append(d)

    data_closing.pop()

    # calculate moving average

    period = 10

    ma = []
    for idx, d in enumerate(data_closing):
        if idx < period-1:
            continue
        avg = (float(data_closing[idx]) + float(data_closing[idx - 1]) + float(data_closing[idx - 2]) + float(data_closing[idx - 3]) + float(data_closing[idx - 4]) + float(data_closing[idx - 5]) + float(data_closing[idx - 6]) + float(data_closing[idx - 7]) + float(data_closing[idx - 8]) + float(data_closing[idx - 9])) / period
        ma.append(avg)

    # building the cleaned dictionary
    data_clean = {}
    for idx, i in enumerate(data_closing):
        if idx < period-1:
            data_clean[i] = 0
            continue
        data_clean[i] = ma[idx - 9]

    data.reset_index(inplace=True)
    dates = []
    for d in data['Date']:
        dates.append(d)

    start = dates[0]
    end = dates[-1]

    data_clean['years'] = end.year - start.year
    if data_closing[-1] > ma[-1] and data_closing[-2] < ma[-2]:
        data_clean['entry'] = 'entry'
    elif data_closing[-1] < ma[-1] and data_closing[-2] > ma[-2]:
        data_clean['entry'] = 'exit'
    else:
        data_clean['entry'] = ''

    return data_clean


