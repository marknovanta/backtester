from tester import trade_it
import threading

def get_info(tickers, interval):

    capital = 1000


    info = []

    # SINGLE THREAD WORK
    """ for t in tickers:

        info.append(trade_it(t, capital, interval)) """


    def append_result(t, capital, interval, id):
        result = trade_it(t, capital, interval, id)
        info.append(result)


    threads = []
    id = 0
    for t in tickers:
        thread = threading.Thread(target=append_result, args=(t, capital, interval, id))
        thread.start()
        threads.append(thread)
        id += 1


    for thread in threads:
        thread.join()

    info_s = sorted(info, key=lambda x: x['id'])
    return info_s

