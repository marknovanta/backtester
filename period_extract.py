import yfinance as yf

def extract_years(ticker):
    '''
    dates = []

    with open(file, mode='r') as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                dates.append(row[0])

    start = dates[0][:4]
    end = dates[-1][:4]

    years = int(end) - int(start)
    '''

    ticker = yf.Ticker(ticker)

    data = ticker.history(period='max', interval='1mo', prepost=True, auto_adjust=False, actions=False)

    data.reset_index(inplace=True)
    dates = []
    for d in data['Date']:
        dates.append(d)

    start = dates[0]
    end = dates[-1]

    years = end.year - start.year

    return years