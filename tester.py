from data_cleaner import clean_data
from period_extract import extract_years
import math

def trade_it(ticker, data_raw, capital):
    # provide data for cleaning
    data = clean_data(data_raw)

    # set trading variables
    starting_balance = capital
    balance = starting_balance
    trades = 0
    size = 0
    position_open = False
    entry_price = None
    exit_price = None
    result = None
    starting_investment = 0

    # trade
    period_counter = 1
    for key, value in data.items():
        if period_counter < 10:
            period_counter += 1
            continue

        #print(f'CLOSE: {key}, MA: {value}')
        if position_open is True and float(key) < float(value):
            exit_price = float(key)
            result = (exit_price - entry_price)*size
            balance += result
            position_open = False

        if position_open is False and float(key) > float(value):
            entry_price = float(key)
            size = math.floor(balance/entry_price)
            if trades == 0:
                starting_investment = size * entry_price
            trades += 1
            position_open = True

        period_counter +=1

    strategy_yield = (balance - starting_investment) / starting_investment

    periods = extract_years(data_raw)
    cagr = ((balance/starting_investment)**(1/periods))-1


    resulting_data = {
        'ticker': ticker,
        'initial investment': starting_investment,
        'final balance': balance,
        'yield': strategy_yield,
        'cagr': cagr,
        'period': periods,
        'trades': trades
    }
    return resulting_data