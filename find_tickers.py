import requests
import os
from dotenv import load_dotenv

def get_tickers():
    load_dotenv()
    api_key = os.getenv('api_key')
    url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}'
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        exchs = ['NASDAQ', 'NYSE']
        tickers = []
        for i in data:
            try:
                if (float(i['price']) < 100) and (float(i['price']) >= 0.01) and (i['type'] == 'stock') and (i['exchangeShortName'] in exchs) and ('.' not in i['symbol']) and (' ' not in i['symbol']) and ('-' not in i['symbol']):
                    tickers.append(i['symbol'])
            except:
                continue

        tickers_s = sorted(tickers)
        return tickers_s
    except requests.exceptions.RequestException as e:
        print('Error fetching data:', e)
        return []