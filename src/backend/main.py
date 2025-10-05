from fastapi import FastAPI, HTTPException
import yfinance as yf


app = FastAPI()

@app.get("/")
async def read_root():
	return "Hello World"

@app.get("/api/v1/stock/{symbol}")
async def get_stock(symbol: str):
	try:
		dat = yf.Ticker(symbol)
		# add caching here for fewer API calls
		return dat.info
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Lookup failed: {str(e)}"
		)

@app.get("/api/v1/company/{company}")
async def get_symbol(company: str):
	try:
		dat = yf.Lookup(company)
		df = dat.get_stock(1)
		if df.empty:
			raise HTTPException(
				status_code=404,
				detail=f"No comapny found for '{company}"
			)
		symbol = df.index.item()
		return {"symbol":symbol}
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Lookup failed: {str(e)}"
		)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="localhost", port=8000)