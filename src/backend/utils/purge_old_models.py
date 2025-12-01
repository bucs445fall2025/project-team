import os
import pandas as pd
from pathlib import Path

def purge_old_models(file_path: str, cutoff_date_str: str):
	"""
	Deletes old model files, keeping only one for each ticker (unless after cutoff date)
	Parameters:
		file_path (str): Root directory containing the model types
		cutoff_date_str (str): Date string before which models will be deleted
	"""
	root_path = Path(file_path)
	if not root_path.is_dir():
		print(f"Error: Root directory '{file_path}' does not exist")
		return
	try:
		cutoff_date = pd.to_datetime(cutoff_date_str).date()
	except Exception as e:
		print(f"Error: Could not parse cutoff date '{cutoff_date_str}'")
		return
	print(f"\n--- Starting Model Purge (Cutoff Date: {cutoff_date}) ---")
	for model_type_path in root_path.iterdir():
		if not model_type_path.is_dir(): continue
		for ticker_path in model_type_path.iterdir():
			if not ticker_path.is_dir(): continue
			model_dates = []
			for model_file_path in ticker_path.glob('*.pth'):
				file_name_stem = model_file_path.stem
				try:
					model_date = pd.to_datetime(file_name_stem).date()
					model_dates.append((model_date, model_file_path))
				except Exception as e:
					print(f"Error: {e}, skiping {model_file_path}")
					continue
			if not model_dates:
				continue
			max_date = max(d for d, path in model_dates)
			print(f"\nProcessing Ticker: {ticker_path.name}. Newest model date: {max_date}")
			for model_date, model_file_path in model_dates:
				if model_date < cutoff_date and model_date != max_date:
					print(f"  -> DELETING FILE: {model_file_path} (Date: {model_date})")
					try:
						os.remove(model_file_path)
					except OSError as e:
						print(f"  ERROR deleting file {model_file_path}: {e}")
				else:
					print(f"  -> KEEPING FILE: {model_file_path} (Date: {model_date})")
	print("\n--- Cleaning up empty Ticker directories ---")
	for model_type_path in root_path.iterdir():
		if not model_type_path.is_dir(): continue
		for ticker_path in model_type_path.iterdir():
			if ticker_path.is_dir() and not os.listdir(ticker_path):
				print(f"  -> Removing empty Ticker directory: {ticker_path}")
				try:
					ticker_path.rmdir()
				except OSError as e:
					print(f"  ERROR removing empty directory {ticker_path}: {e}")
	print("\n--- Cleaning up empty Model Type directories ---")
	for model_type_path in root_path.iterdir():
		if model_type_path.is_dir() and not os.listdir(model_type_path):
			print(f"  -> Removing empty Model Type directory: {model_type_path}")
			try:
				model_type_path.rmdir()
			except OSError as e:
				print(f"  ERROR removing empty directory {model_type_path}: {e}")
	print("\n--- Purge Process Complete ---")