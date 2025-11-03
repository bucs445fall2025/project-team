import os
import pandas as pd
import db
from utils.load_model import load_model

DIR = "cached_models/"
MODEL_TYPE = "LINEAR"
TARGET_DATE = (pd.Timestamp.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

def run_all_predictions(file_path: str=DIR, input: str=TARGET_DATE, model_type: str=MODEL_TYPE, device: str="cpu"):
	file_path = os.path.join(file_path, model_type)
	if not os.path.exists(file_path):
		raise FileNotFoundError("Error: Directory not found.")
	for root, _, files in os.walk(file_path):
		for file in files:
			if file.endswith(".pth"):
				run_prediction(os.path.join(root, file), os.path.basename(root), input, device)


def run_prediction(file_path: str, ticker: str, input: str=TARGET_DATE, device: str="cpu"):
	model = load_model(file_path, ticker, device)
	prediction = model.predict(input)
	print(f"[{file_path[len(DIR):]}] Prediction for {input}: ${prediction:.2f}")
	try:
		db.insert_prediction(ticker, prediction)
	except Exception as e:
		print(f"Error while posting to database: {e}")