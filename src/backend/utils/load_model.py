import torch
import os

def load_model(file_path: str, device: str="cpu"):
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"The file '{file_path} was not found.")
	return torch.load(
		file_path,
		map_location=torch.device(device),
		weights_only=True
	)