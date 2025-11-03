from fastapi import APIRouter, Query, HTTPException
from utils.yfinance_api import get_stock_data
from typing import Optional

router = APIRouter()

@router.get("/stock/data")
def fetch_stock_data(
    ticker: str = Query(..., description="stock ticker symbol"),
    start_date: Optional[str] = Query(None, description="start date in 'YYYY-MM-DD'"),
    end_date: Optional[str] = Query(None, description="end date in 'YYYY-MM-DD'"),
    interval: str = Query("1d", description="data interval (1d, 1wk, 1mo)")
):

    try:
        data = get_stock_data(ticker, start_date, end_date, interval)
        data.reset_index(inplace=True) # Reset index to make 'Date' a column
        if data.empty:
            raise HTTPException(status_code=404, detail="no data found for the given parameters")
        print("Returning data:", data.reset_index().to_dict(orient="records")[:2])
        return {"data": data.to_dict(orient="records")}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))