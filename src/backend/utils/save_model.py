import torch
import os

def save_model(model, path: str):
    """
    Save a model to a desired file path
    Parameters:
        model (any): Model instance
        path (str): Exact file path for the model to be saved to
    """
    if model.X_mean is None or model.X_std is None:
        print("Model must be populated before saving")
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'X_mean': model.X_mean,
        'X_std': model.X_std,
        'y_mean': model.y_mean,
        'y_std': model.y_std,
        'reference_date': str(model.reference_date) if model.reference_date is not None else None,
        'datenum': model.datenum,
    }
    torch.save(checkpoint, path)
    print("Model saved to: " + path)
    return True