from tester import trade_it
import threading

def get_info(tickers, interval):

    capital = 1000


    info = []

    # SINGLE THREAD WORK
    """ for t in tickers:

        info.append(trade_it(t, capital, interval)) """


    def append_result(t, capital, interval, id, semaphore):
        result = trade_it(t, capital, interval, id)
        with semaphore:
            info.append(result)

    max_threads = 112
    semaphore = threading.Semaphore(max_threads)

    threads = []
    id = 0
    for t in tickers:
        thread = threading.Thread(target=append_result, args=(t, capital, interval, id, semaphore))
        thread.start()
        threads.append(thread)
        id += 1


    for thread in threads:
        thread.join()

    info_s = sorted(info, key=lambda x: x['id'])
    return info_s

