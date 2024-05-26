from data_cleaner import clean_data
import math

def trade_it(ticker, capital, interval, id, info_q, period):
    # provide data for cleaning
    #period = 10 #MOVING AVERAGE PERIOD
    data = clean_data(ticker, interval, period)
    periods = data['years']
    entry = data['entry']
    name = data['name']
    sector = data['sector']

    divYield = data['divYield']
    payout = data['payout']
    pe = data['pe']
    current_ratio = data['current_ratio']
    debt_equity = data['debt_equity']
    current_price = data['current_price']
    book_value = data['book_value']

    data.pop('divYield')
    data.pop('payout')
    data.pop('pe')
    data.pop('current_ratio')
    data.pop('debt_equity')
    data.pop('current_price')
    data.pop('book_value')

    data.pop('name')
    data.pop('sector')
    data.pop('years')
    data.pop('entry')

    # set trading variables
    starting_balance = capital
    balance = starting_balance
    trades = 0
    wins = 0
    losses = 0
    size = 0
    position_open = False
    entry_price = None
    exit_price = None
    result = None
    starting_investment = 0
    balance_hist = [balance]

    # trade
    period_counter = 1
    for key, value in data.items():
        if period_counter < period:
            period_counter += 1
            continue

        #print(f'CLOSE: {key}, MA: {value}')
        if position_open is True and float(key) < float(value):
            exit_price = float(key)
            result = (exit_price - entry_price)*size
            if result > 0:
                wins += 1
            elif result < 0:
                losses += 1
            balance += result
            balance_hist.append(balance)
            position_open = False

        if position_open is False and float(key) > float(value):
            entry_price = float(key)
            size = math.floor(balance/entry_price)
            if trades == 0:
                starting_investment = size * entry_price
            trades += 1
            position_open = True

        period_counter +=1

    try:
        strategy_yield = (balance - starting_investment) / starting_investment
    except ZeroDivisionError:
        strategy_yield = 0

    try:
        cagr = ((balance/starting_investment)**(1/periods))-1
    except ZeroDivisionError:
        cagr = 0

    try:
        pb = current_price / book_value
    except:
        pb = ''

    try:
        win_rate = wins / (wins + losses)
    except:
        win_rate = 0

    resulting_data = {
        'id': id,
        'ticker': ticker,
        'initial investment': starting_investment,
        'final balance': balance,
        'yield': strategy_yield,
        'cagr': cagr,
        'period': periods,
        'trades': trades,
        'win_rate': win_rate,
        'entry': entry,
        'name': name,
        'sector': sector,
        'divYield' : divYield,
        'payout' : payout,
        'pe' : pe,
        'current_ratio' : current_ratio,
        'debt_equity' : debt_equity,
        'current_price' : current_price,
        'book_value' : book_value,
        'pb': pb,
        'balance_hist': balance_hist
    }

    info_q.put(resulting_data)
    return resulting_data