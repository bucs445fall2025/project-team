from fastapi import HTTPException
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
load_dotenv()


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


def insert_prediction (ticker: str, prediction_data: int):
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

if __name__ == "__main__":
    # simple test
    msg = insert_prediction("blah", 100000)
    print(msg)
