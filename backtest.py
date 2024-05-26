from tester import trade_it
import threading
import queue

def get_info(tickers, interval, period):

    capital = 1000


    info = []

    # SINGLE THREAD WORK
    """ for t in tickers:

        info.append(trade_it(t, capital, interval)) """


    """ def append_result(t, capital, interval, id, semaphore):
        result = trade_it(t, capital, interval, id)
        with semaphore:
            info.append(resul10
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
        thread.join() """

    info_q = queue.Queue()
    id = 0
    threads = []
    for t in tickers:
        thread = threading.Thread(target=trade_it, args=(t, capital, interval, id, info_q, period))
        threads.append(thread)
        thread.start()
        id += 1

    for thread in threads:
        thread.join()

    while not info_q.empty():
        i = info_q.get()
        info.append(i)

    info_s = sorted(info, key=lambda x: x['id'])
    return info_s

