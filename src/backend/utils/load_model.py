import torch
import os
import pandas as pd
from cachetools import cached, LRUCache
from model.linear import LinearRegression

_model_cache = LRUCache(maxsize=256)

@cached(_model_cache)
def load_model(file_path: str, ticker: str, device: str="cpu"):
    """
    Loads a model from a file
    Parameters:
        file_path (str): Desired model file path to load
        ticker (str): Ticker of the company
        device (str): Device to run the model on
    Returns:
        LinearRegression: Trained model instance
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    checkpoint = torch.load(
        file_path,
        map_location=torch.device(device),
        weights_only=True
    )
    model = LinearRegression(ticker=ticker).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.X_mean = checkpoint['X_mean']
    model.X_std = checkpoint['X_std']
    model.y_mean = checkpoint['y_mean']
    model.y_std = checkpoint['y_std']
    model.reference_date = pd.Timestamp(checkpoint['reference_date'])
    model.datenum = checkpoint['datenum']
    model.eval()
    return model