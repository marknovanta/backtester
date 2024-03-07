from tester import trade_it

def get_info(tickers):

    capital = 1000

    info = []


    for t in tickers:
        data = './data/' + t + '.csv'
        info.append(trade_it(t, data, capital))

    return info

