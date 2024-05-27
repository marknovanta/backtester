import requests
import os
from dotenv import load_dotenv

def get_tickers(operativity):
    load_dotenv()
    api_key = os.getenv('api_key')
    url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}'
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        exchs = ['NASDAQ', 'NYSE', 'AMEX']
        tickers = []

        for i in data:
            try:
                if operativity == 's':
                    c1 = float(i['price']) < 100 #max price
                    c2 = float(i['price']) >= 1 #min price

                elif operativity == 'i':
                    c1 = float(i['price']) > 1 #min price
                    c2 = True

                c3 = i['type'] == 'stock'
                c4 = i['exchangeShortName'] in exchs
                c5 = '.' not in i['symbol']
                c6 = ' ' not in i['symbol']
                c7 = '-' not in i['symbol']

                if c1 and c2 and c3 and c4 and c5 and c6 and c7:
                    tickers.append(i['symbol'])
            except:
                continue

        tickers_s = sorted(tickers)
        return tickers_s
    except requests.exceptions.RequestException as e:
        print('Error fetching data:', e)
        return []