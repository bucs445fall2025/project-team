from fastapi import HTTPException
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
load_dotenv()

"""
get_db_connection()
	database connection and operations for stock predictions and watchlist management

	parameters:
		- None
	returns:
		- database connection object
"""

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

"""
insert_prediction(ticker: str, prediction_data: int)
	Inserts a new stock prediction into the Basic_Stock_Predictions table if no recent prediction exists.
	parameters:
		- ticker: Stock ticker symbol
		- prediction_data: Prediction data as an integer
	returns:
		- message indicating success or reason for skipping insertion
"""
def insert_prediction(ticker: str, prediction_data: int):
	conn = get_db_connection()
	if conn is None:
		raise Exception("Database connection failed")
	try:
		
		date_now = datetime.now().strftime("%Y-%m-%d")

		cursor = conn.cursor(dictionary=True)
		cursor.execute(
			"SELECT Date_DTTM FROM Basic_Stock_Predictions WHERE Stock_Ticker = %s ORDER BY Date_DTTM DESC LIMIT 1",
			(ticker,)
		)
		result = cursor.fetchone()
		if not result or result['Date_DTTM'] < (datetime.now() - timedelta(days=1)).date():
			cursor.execute("INSERT INTO Basic_Stock_Predictions (Date_DTTM, Stock_Ticker, Prediction_Data) VALUES (%s, %s, %s)", (date_now, ticker, prediction_data))
			conn.commit()
			msg = "Insertion successful."
		else:
			msg = "Recent prediction exists, skipping insertion."
		
		cursor.close()
		conn.close()
		return msg
	except Error as e:
		print(f"DB insertion error: {e}")
		raise Exception("Failed to insert prediction")

"""get_prediction(ticker: str)
	Retrieves the latest stock prediction for a given ticker from the Basic_Stock_Predictions
	
	parameters:
		- ticker: Stock ticker symbol
	returns:
		- prediction record as a dictionary
"""
def get_prediction(ticker: str):
	conn = get_db_connection()
	if conn is None:
		raise Exception("Database connection failed")

	try:
		cursor = conn.cursor(buffered=True)
		command = "SELECT * FROM Basic_Stock_Predictions WHERE Stock_Ticker = %s"
		cursor.execute(command, (ticker,))
		result = cursor.fetchone()

		cursor.close()
		conn.close()
		return result
	except Error as e:
		print(f"DB Fetching error: {e}")
		raise Exception("Failed to get row")

"""insert_watchlist(userid: int, ticker: str)
	Adds a stock ticker to the user's watchlist if it is not already present.
	parameters:
		- userid: User ID
		- ticker: Stock ticker symbol
	returns:
		- message indicating success or if the stock is already in the watchlist
"""
def insert_watchlist(userid: int, ticker: str):
	conn = get_db_connection()
	if conn is None:
		raise Exception("Database connection failed")

	try:
		cursor = conn.cursor()

		# Use INSERT IGNORE or handle duplicate key error
		cursor.execute(
			"INSERT INTO watchlist (user_id, ticker) VALUES (%s, %s)", (userid, ticker)
		)
		conn.commit()

		affected_rows = cursor.rowcount
		cursor.close()
		conn.close()

		if affected_rows > 0:
			return {"message": "Stock added to watchlist", "success": True}
		else:
			return {"message": "Stock already in watchlist", "success": False}

	except mysql.connector.IntegrityError as e:
		# Handle duplicate entry (if UNIQUE constraint exists)
		if "Duplicate entry" in str(e):
			return {"message": "Stock already in watchlist", "success": False}
		raise Exception(f"Failed to add to watchlist: {e}")
	except Error as e:
		print(f"DB insertion error: {e}")
		raise Exception("Failed to add to watchlist")

"""
get_watchlist(userid: int)
	Retrieves the watchlist for a given user ID.
	
	parameters:
		- userid: User ID
	
	returns:
		- list of stock tickers in the user's watchlist
"""
def get_watchlist(userid: int):
    conn = get_db_connection()
    if conn is None:
        raise Exception("Database connection failed")

    try:
        cursor = conn.cursor(dictionary=False)
        cursor.execute(
			"SELECT ticker FROM watchlist WHERE user_id = %s ORDER BY added_at DESC",
			(userid,),
		)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        tickers = [ticker[0] for ticker in results]
        return tickers

    except Error as e:
        print(f"DB fetching error: {e}")
        raise Exception("Failed to get watchlist")

"""
remove_from_watchlist(userid: int, ticker: str)
	Removes a stock ticker from the user's watchlist.
	
	parameters:
		- userid: User ID
		- ticker: Stock ticker symbol
	
	returns:
		- message indicating success or if the stock was not found in the watchlist
"""
def remove_from_watchlist(userid: int, ticker: str):
	conn = get_db_connection()
	if conn is None:
		raise Exception("Database connection failed")

	try:
		cursor = conn.cursor()
		cursor.execute(
			"DELETE FROM watchlist WHERE user_id = %s AND ticker = %s", (userid, ticker)
		)
		conn.commit()

		affected_rows = cursor.rowcount
		cursor.close()
		conn.close()

		if affected_rows > 0:
			return {"message": "Stock removed from watchlist", "success": True}
		else:
			return {"message": "Stock not found in watchlist", "success": False}

	except Error as e:
		print(f"DB deletion error: {e}")
		raise Exception("Failed to remove from watchlist")
