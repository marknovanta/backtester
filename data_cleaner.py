import csv
import yfinance as yf

def clean_data(ticker):

    print(f'Processing {ticker} ...')
    ticker = yf.Ticker(ticker)

    #data = {}
    data = ticker.history(period='max', interval='1mo', prepost=True, auto_adjust=False, actions=False)
    data_closing = []
    for d in data['Close']:
        data_closing.append(d)

    '''
    # open CSV
    with open(file, mode='r') as f:
        reader = csv.reader(f)
        next(reader, None)

        # store data from CSV in a dictionary of dictionaries
        for row in reader:
            data[row[0]] = {
                'open':row[1],
                'high': row[2],
                'low': row[3],
                'close': row[4],
                'adj_close': row[5],
                'volume': row[6],
                'MA': 0
                }
            data_closing.append(row[4])
    '''

    # popping out the last data because month not yet closed
    #data_closing.pop()
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

    return data_clean


