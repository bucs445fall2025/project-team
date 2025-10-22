import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
load_dotenv()

def get_db_connection():
    try:
        port = int(os.getenv("DATABASE_PORT", "3306"))
        conn = mysql.connector.connect(
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST", "localhost"),
            database=os.getenv("DATABASE_NAME") or os.getenv("DATABASE_BASE"),
            port=port,
        )
        if conn.is_connected():
            return conn
        else: 
            print("Failed to connect to database")
            return None
    except Error as e:
        print(f"DB connection error: {e}")
        return None
    
def insert_prediction (ticker: str, prediction_data: int):
    conn = get_db_connection()
    if conn is None:
        raise Exception("Database connection failed")
        return False
    try:

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT Date_DTTM FROM Basic_Stock_Predictions WHERE Stock_Ticker = %s ORDER BY Date_DTTM DESC LIMIT 1",
            (ticker,)
        )
        result = cursor.fetchone()
        if not result or result['Date_DTTM'] < datetime.now() - timedelta(days=1):
            cursor.execute("INSERT INTO Basic_Stock_Predictions (Stock_Ticker, Prediction_Data) VALUES (%s, %s)", (ticker, prediction_data))
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
    # Simple test
    msg = insert_prediction("NVDA", 100000)
    print(msg)
