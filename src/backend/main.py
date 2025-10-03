from fastapi import FastAPI
import yfinance as yf


app = FastAPI()

@app.get("/")
async def read_root():
	return "Hello World"

@app.get("/api/v1/stock/{symbol}")
async def get_stock(symbol: str):
	return {"symbol": symbol, "price": 100.0}



if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="localhost", port=8000)