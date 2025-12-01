import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils.yfinance_api import get_stock_data
from google import genai

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        user=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        host="db.chinny.net",
        database=os.getenv("DATABASE_BASE"),
        port=3306,
    )

class gemini_api:
	def __init__(self, model: str = "gemini-2.5-flash"):
		self.api_key = os.getenv("GEMINI_API_KEY")

		if not self.api_key:
			raise ValueError("GEMINI_API_KEY not found in environment variables.")

		# create gemini client
		self.client = genai.Client(api_key=self.api_key)
		self.model_name = model

	def _query_gemini(self, prompt: str) -> str:
		# call gemini api

		for attempt in range(5):
			try:
				response = self.client.models.generate_content(
					model=self.model_name,
					contents=prompt
				)
				return response.text
			except Exception as e:
				if attempt < 4:
					continue
				else:
					raise RuntimeError(f"Gemini API request failed after 5 attempts: {str(e)}")
		return response.text

	# save analysis to cache
	def save_to_cache(self, ticker: str, analysis: str):
		conn = get_db_connection()
		cursor = conn.cursor()
		expires = (datetime.now() + timedelta(hours=24))
		cursor.execute(
			"INSERT INTO gemini_cache (ticker, analysis, created, expires) VALUES (%s, %s, %s, %s)",
			(ticker, analysis, datetime.now(), expires)
		)
		conn.commit()
		cursor.close()
		conn.close()

	# retrieve cached analysis if exists and not expired
	def get_cached_gemini(self, ticker:str):
		conn = get_db_connection()
		cursor = conn.cursor(dictionary=True)
		cursor.execute(
			"SELECT * FROM gemini_cache WHERE ticker = %s AND expires > %s ORDER BY created DESC LIMIT 1",
			(ticker, datetime.now())
		)
		row = cursor.fetchone()
		cursor.close()
		conn.close()

		if row:
			return row['analysis']
		else:
			return None
	
	def analyze_stock(self, ticker: str) -> str:
		
		# check cache
		cached = self.get_cached_gemini(ticker)
		if cached:
			return cached
		# continue and cache later

		# get stock data for past 5 days and take just the last 3 days
		today = datetime.today().strftime("%Y-%m-%d")
		five_days_ago = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")

		stock_data = get_stock_data(
			ticker,
			start_date=five_days_ago,
			end_date=today,
			interval="1d"
		)

		last_3_days = stock_data.tail(3)

		if last_3_days.empty:
			return f"No trading data found for {ticker} over the last 3 days."

		# format summary string
		stats_summary = f"Ticker: {ticker}\n"
		for _, row in last_3_days.iterrows():
			stats_summary += (
				f"Open: {row[f'Open_{ticker}']}\n"
				f"Close: {row[f'Close_{ticker}']}\n"
				f"High: {row[f'High_{ticker}']}\n"
				f"Low: {row[f'Low_{ticker}']}\n"
				f"Volume: {row[f'Volume_{ticker}']}\n\n"
			)

		# prompt
		prompt = (
			f"You are a financial analyst. Here are the last 3 trading days of stats for {ticker}:\n\n"
			f"{stats_summary}\n"
			f"Now, check the latest financial news about {ticker} and explain in less than 100 words, format nicely for user app:\n"
			f"Why this stock is trending.\n"
			f"What to expect in the near term based on recent news.\n"
			f"Any potential risks or opportunities.\n"
			f"Provide a concise but insightful analysis."
		)
	
		# save to cache
		gemini = self._query_gemini(prompt)
		self.save_to_cache(ticker, gemini)
		return gemini