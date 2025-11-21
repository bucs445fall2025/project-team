import pandas as pd
import requests
from cachetools import LRUCache, cached
from io import StringIO

_sp500_cache = LRUCache(4)

@cached(_sp500_cache)
def get_sp500():
	url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'  # Default user-agent fails.
	response = requests.get(url, headers={'User-Agent': user_agent})
	if response.status_code == 200:
		tables = pd.read_html(StringIO(response.text))
		sp500_table = tables[0]
		tickers = sp500_table['Symbol'].tolist()
		return tickers
	else:
		raise IOError(f"Failed to fetch S&P 500 data from {url}. Status Code: {response.status_code}")