import csv
import yfinance as yf

def clean_data(ticker, interval):

    # INTERVALS: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    # interval = '1mo'

    print(f'Processing {ticker} ...')
    ticker = yf.Ticker(ticker)
    info = ticker.info
    name = info['longName']
    try:
        sector = info['sector']
    except:
        sector = ''

    try:
        divYield = info['dividendYield']
    except:
        divYield = 0

    try:
        payout = info['payoutRatio']
    except:
        payout = 0

    try:
        pe = info['trailingPE']
    except:
        pe = 0

    try:
        current_ratio = info['currentRatio']
    except:
        current_ratio = 0

    try:
        debt_equity = info['debtToEquity']
    except:
        debt_equity = 0

    try:
        current_price = info['currentPrice']
    except:
        current_price = 0

    try:
        book_value = info['bookValue']
    except:
        book_value = 0

    data = ticker.history(period='max', interval=interval, prepost=True, auto_adjust=False, actions=False)
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
        data_clean[i] = ma[idx - (period-1)]

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

    data_clean['name'] = name
    data_clean['sector'] = sector

    data_clean['divYield'] = divYield
    data_clean['payout'] = payout
    data_clean['pe'] = pe
    data_clean['current_ratio'] = current_ratio
    data_clean['debt_equity'] = debt_equity
    data_clean['current_price'] = current_price
    data_clean['book_value'] = book_value

    return data_clean


