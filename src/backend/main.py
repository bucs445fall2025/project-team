from fastapi import FastAPI, HTTPException
import yfinance as yf
from dotenv import load_dotenv
from cachetools import cached, TTLCache
from db import insert_prediction, get_db_connection
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.predictors import run_all_predictions
from routers.auth import router as auth_router
from routers.market import router as market_router
from routers.predict import router as predict_router
from routers import stock_router 
load_dotenv()

db = None

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(stock_router.router, prefix="/api")
app.include_router(market_router, prefix = "/api")
app.include_router(predict_router, prefix ="/api")

origins = [
		"http://localhost:3000"
    ]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],  # Or specify specific methods like ["GET", "POST"]
	allow_headers=["*"],  # Or specify specific headers like ["Authorization", "Content-Type"]
)

_yf_api_cache = TTLCache(maxsize=128, ttl=30)

# Prediction Scheduling
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=15, minute=0)
scheduler.add_job(run_all_predictions, trigger)
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
	yield
	scheduler.shutdown()

@app.get("/")
async def read_root():
	return "Hello World"

@cached(cache=_yf_api_cache)
@app.get("/api/v1/stock/{symbol}")
async def get_stock(symbol: str):
	try:
		dat = yf.Ticker(symbol)
		return dat.info
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Lookup failed: {str(e)}"
		)

@cached(cache=_yf_api_cache)
@app.get("/api/v1/stock/{symbol}/{field}")
async def get_stock_field(symbol: str, field: str):
	try:
		ticker = yf.Ticker(symbol)
		info = ticker.info
		if field in info:
			return info[field]
		else:
			raise HTTPException(
				status_code=404,
				detail=f"Field '{field}' not found for symbol '{symbol}'"
			)
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Lookup failed: {str(e)}"
		)

@cached(cache=_yf_api_cache)
@app.get("/api/v1/company/{company}")
async def get_symbol(company: str):
	try:
		dat = yf.Lookup(company)
		df = dat.get_stock(1)
		if df.empty:
			raise HTTPException(
				status_code=404,
				detail=f"No company found for '{company}"
			)
		symbol = df.index.item()
		return {"symbol":symbol}
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Lookup failed: {str(e)}"
		)

@app.get("/api/v1/database/stockInfo/{symbol}")
async def get_stock_info_from_database(symbol: str):
	db = get_db_connection()

	if not db.is_connected():
		raise HTTPException(status_code=500, detail="Could not connect to database")

	cursor = db.cursor()

	command = f"SELECT * FROM stock WHERE ticker = '{symbol}'"
	result = cursor.execute(command)
	rows = cursor.fetchall()

	return rows

@app.post("/api/v1/database/stockInfo/{symbol}")
async def post_stock_info_to_database(symbol: str):
	db = get_db_connection()

	if not db.is_connected():
		raise HTTPException(status_code=500, detail="Could not connect to database")

	# only do something if stock doesnt exist
	current_rows = await get_stock_info_from_database(symbol)
	if len(current_rows) == 0:
		sector = await get_stock_field(symbol, "sector")
		cursor = db.cursor()

		command = "INSERT INTO stock (ticker, sector) VALUES (%s, %s)"
		print(command)
		values = (symbol, sector)
		print(values)
		cursor.execute(command, values)
		db.commit()
	
	return f"Added {symbol} to the table"


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="localhost", port=8000)
