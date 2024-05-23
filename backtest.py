from tester import trade_it
#import concurrent.futures
import threading
import collections

def get_info(tickers, interval):

    capital = 1000


    info = collections.deque()

    # SINGLE THREAD WORK
    """ info = []
    for t in tickers:

        info.append(trade_it(t, capital, interval)) """


    def append_result(t, capital, interval, event):
        result = trade_it(t, capital, interval)
        info.append(result)
        event.set()


    events = [threading.Event() for t in tickers]

    for t, event in zip(tickers, events):
        thread = threading.Thread(target=append_result, args=(t, capital, interval, event))
        thread.start()


    for event in events:
        event.wait()

    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

    return info

