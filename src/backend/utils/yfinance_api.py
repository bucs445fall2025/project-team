import yfinance as yf
from typing import Optional

from yfinance import data
"""
    get stock data using custom date range.

    args: ticker (str): stock ticker symbol
          start_date (str): start date in 'YYYY-MM-DD' format
          end_date (str): end date in 'YYYY-MM-DD' format
          interval (str): data interval (1d, 1wk, 1mo)

"""
def get_stock_data(ticker: str, start_date: Optional[str], end_date: Optional[str], interval: str = "1d"):
    if start_date is not None and end_date is not None:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period="1mo", interval=interval)

    # reset index to flatten date column
    data.reset_index(inplace=True)  
    flattened_columns = [] 

    # flatten multi index columns if any
    for col in data.columns:
        if isinstance(col, tuple):
            flattened = "_".join(col).strip()
            flattened_columns.append(flattened)
        else:
            flattened_columns.append(col)

    data.columns = flattened_columns   
    return data