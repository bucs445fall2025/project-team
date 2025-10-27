import torch
import os

def save_model(model_state, path: str):
	if model_state.X_mean is None or model_state.X_std is None:
		print("Model must be populated before making predictions")
		return False
	os.makedirs(os.path.dirname(path), exist_ok=True)
	torch.save(model_state.state_dict(), path)
	print("Model saved to: " + path)
	return True
