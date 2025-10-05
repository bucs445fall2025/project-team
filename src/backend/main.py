from fastapi import FastAPI, HTTPException
import yfinance as yf


app = FastAPI()

@app.get("/")
async def read_root():
	return "Hello World"

@app.get("/api/v1/stock/{symbol}")
async def get_stock(symbol: str):
<<<<<<< HEAD
	try:
		dat = yf.Ticker(symbol)
		# add caching here for fewer API calls
		return dat.info
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Lookup failed: {str(e)}"
		)
=======
	dat = yf.Ticker(symbol)
	# add caching here for fewer API calls
	return dat.info

@app.get("/api/v1/stock/{symbol}/getCurrentPrice")
async def get_current_price(symbol: str):
	try:
		ticker = yf.Ticker(symbol)
		info = ticker.info

		prev_close = info.get("regularMarketPrice")
		prev_close_percent = round(info.get("regularMarketChangePercent"), ndigits=2)

		if 'postMarketPrice' in info:
			post_price = info.get("postMarketPrice")
			post_price_percent = round(info.get("postMarketChangePercent"), ndigits=2)
			
			return {
				"post_price": post_price,
				"post_price_percent": post_price_percent,
				"last_price": prev_close,
				"last_price_percent": prev_close_percent,
				"source": "after-hours"
			}

		elif "preMarketPrice" in info:

			pre_price = info.get("preMarketPrice")
			pre_price_percent = round(info.get("preMarketChangePercent"), ndigits=2)
			return {
				"pre_price": pre_price,
				"pre_price_percent": pre_price_percent,
				"last_price": prev_close,
				"last_price_percent": prev_close_percent,
				"source": "before-hours"
			}
		else:
			return {
				"last_price": prev_close,
				"last_price_percent": prev_close_percent,
				"source": "during-hours"
			}

	except Exception as e:
		print(e)
		raise HTTPException(status_code=404, detail="Current price not found")
		

>>>>>>> refs/remotes/origin/main

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