from cachetools import cached, LRUCache
import pandas as pd
import yfinance as yf

_util_cache = LRUCache(maxsize=256)

@cached(cache=_util_cache)
def get_moving_average(ticker: str, interval: int=50):
	data = yf.download(ticker, period="2y", progress=False, auto_adjust=True)
	if data.empty:
		raise Exception(f"Could not find data for ticker {ticker}")
	data[f'{interval}-Day SMA'] = data['Close'].rolling(window=interval).mean()
	return data[['Close', f'{interval}-Day SMA']].dropna()

#print(get_moving_average("AAPL"))