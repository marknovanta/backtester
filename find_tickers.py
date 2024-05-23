import requests
import os
from dotenv import load_dotenv
import json

def get_tickers():
    load_dotenv()
    api_key = os.getenv('api_key')
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}'
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        exchs = ['NASDAQ', 'NYSE']
        tickers = []
        filtered_data = []
        for i in data:
            try:
                if (float(i['price']) < 100) and (float(i['price']) >= 10) and (i['type'] == 'stock') and (i['exchangeShortName'] in exchs) and ('.' not in i['symbol']) and (' ' not in i['symbol']) and ('-' not in i['symbol']):
                    tickers.append(i['symbol'])
                    filtered_data.append(i)
            except:
                continue

        with open('found_tickers.txt', 'w') as file:
            for i in filtered_data:
                file.write(json.dumps(i))
                file.write('\n')

        return tickers
    except requests.exceptions.RequestException as e:
        print('Error fetching data:', e)
        return []