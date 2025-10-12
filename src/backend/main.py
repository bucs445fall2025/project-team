from fastapi import FastAPI, HTTPException
import yfinance as yf

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

db = None

app = FastAPI()


def get_db_connection():
	try:
		session = mysql.connector.connect(
			user=os.getenv("DATABASE_USERNAME"),
			password=os.getenv("DATABASE_PASSWORD"),
			host="db.chinny.net",
			database=os.getenv("DATABASE_BASE"),
			port=3306,
		)
		return session
	except Error as e:
		print(e)
		raise HTTPException(status_code=500, detail="Could not connect to database")


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
