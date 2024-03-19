from tester import trade_it

def get_info(tickers):

    capital = 1000

    info = []


    for t in tickers:

        info.append(trade_it(t, capital))

    return info

