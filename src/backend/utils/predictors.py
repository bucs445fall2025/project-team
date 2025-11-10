import os
import pandas as pd
import db
from utils.load_model import load_model
from model.linear import create_model
from utils.get_sp500 import get_sp500
import concurrent.futures

DIR = "cached_models/"
MODEL_TYPE = "LINEAR"
TARGET_DATE = (pd.Timestamp.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
FILE_EXT = ".pth"

""" Old run all predictions (sequential) 
def run_all_predictions(file_path: str=DIR, input: str=TARGET_DATE, model_type: str=MODEL_TYPE, device: str="cpu"):
	file_path = os.path.join(file_path, model_type)
	if not os.path.exists(file_path):
		raise FileNotFoundError("Error: Directory not found.")
	for root, _, files in os.walk(file_path):
		for file in files:
			if file.endswith(".pth"):
				run_prediction(os.path.join(root, file), os.path.basename(root), input, device) """


def run_all_predictions(file_path: str=DIR, input: str=TARGET_DATE, model_type: str=MODEL_TYPE, device: str="cpu"):
    file_path = os.path.join(file_path, model_type)
    if not os.path.exists(file_path):
        raise FileNotFoundError("Error: Directory not found.")
    tasks = []
    for root, _, files in os.walk(file_path):
        for file in files:
            if file.endswith(".pth"):
                task_args = (os.path.join(root, file), os.path.basename(root), input, device)
                tasks.append(task_args)
    # If model.predict is heavily CPU-bound (complex calculations), use ProcessPoolExecutor instead.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_prediction = {
            executor.submit(run_prediction, *args): args[1]
            for args in tasks
        }        
        for future in concurrent.futures.as_completed(future_to_prediction):
            ticker = future_to_prediction[future]
            try:
                future.result()
            except Exception as e:
                print(f'Ticker {ticker} generated an exception: {e}')

def run_prediction(file_path: str, ticker: str, input: str=TARGET_DATE, device: str="cpu"):
	model = load_model(file_path, ticker, device)
	print(f"Loaded model for {ticker} from {file_path}")
	prediction = model.predict(input)
	print(f"[{file_path[len(DIR):]}] Prediction for {input}: ${prediction:.2f}")
	try:
		db.insert_prediction(ticker, round(prediction, 2))
	except Exception as e:
		print(f"Error while posting to database: {e}")

def save_sp500(count: int = 500, file_path: str=DIR, model_type: str=MODEL_TYPE):
	sp500_tickers = get_sp500()
	file_name = pd.Timestamp.now().strftime('%Y-%m-%d') + FILE_EXT
	for i, ticker in enumerate(sp500_tickers[:count]):
		model_path = os.path.join(file_path, model_type, ticker, file_name)
		if not os.path.exists(model_path):
			try:
				create_model(ticker)
				print(f"[{i}] Saved model for {ticker} [{pd.Timestamp.now()}]")
			except Exception as e:
				print(e)
		else:
			print(f"Skipping {ticker}, already trained today")