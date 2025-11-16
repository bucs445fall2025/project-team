import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import requests
from utils.moving_average import get_moving_average
from utils.save_model import save_model

MAX_ITER = 10000
LR = 0.001
BATCH_SIZE = 32
TICKER = "AAPL"
INTERVAL = 50
SAMPLE_COUNT = 1000
TRAIN_RATIO = 0.8
PATIENCE = 100
GPU_TRAIN = False
MOMENTUM = 0.9
API_BASE_URL = "http://localhost:8000"
DIR = "cached_models/"
FILE_EXT = ".pth"
MODEL_TYPE = "LINEAR"
REFERENCE_DATE = '2025-11-01'

device = torch.device("cpu")
if __name__ == "__main__":
    if GPU_TRAIN:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("CUDA available:", torch.cuda.is_available())
        print("Device:", device)
        print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU only")
    else:
        print("GPU training disabled, using CPU only")


class LinearRegression(nn.Module):
    def __init__(self, ticker=TICKER, api_base_url=API_BASE_URL):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(3, 1)
        self.X_mean = None
        self.X_std = None
        self.y_mean = None
        self.y_std = None
        self.api_base_url = api_base_url
        self.reference_date = None
        self.ticker = ticker
        self.datenum = None
        self.model_type = MODEL_TYPE

    def get_dir(self) -> str:
        return DIR + MODEL_TYPE + "/" + self.ticker + "/" + self.get_date() + FILE_EXT

    def get_date(self) -> str:
        return pd.Timestamp.now().strftime('%Y-%m-%d')

    def forward(self, x):
        return self.linear(x)
    
    def _normalize_features(self, X_tensor):
        if self.X_mean is None or self.X_std is None:
            self.X_mean = X_tensor.mean(dim=0, keepdim=True)
            self.X_std = X_tensor.std(dim=0, keepdim=True)
        return (X_tensor - self.X_mean) / self.X_std
    
    def _normalize_targets(self, y_train):
        self.y_mean = y_train.mean(dim=0, keepdim=True)
        self.y_std = y_train.std(dim=0, keepdim=True)
        return (y_train - self.y_mean) / self.y_std
    
    def _denormalize_prediction(self, pred_normalized):
        if self.y_mean is not None and self.y_std is not None:
            return pred_normalized * self.y_std + self.y_mean
        return pred_normalized
    
    def _fetch_close_price_from_api(self):
        response = requests.get(f"{self.api_base_url}/api/v1/stock/{self.ticker}")
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch stock data: {response.text}")
        stock_info = response.json()
        close_price_response = requests.get(
            f"{self.api_base_url}/api/v1/stock/{self.ticker}/currentPrice"
        )
        if close_price_response.status_code == 200:
            return close_price_response.json()
        close_price = (stock_info.get("currentPrice") or 
                      stock_info.get("regularMarketPrice") or 
                      stock_info.get("previousClose"))
        if close_price is None:
            raise ValueError("Could not retrieve close price from API")
        return close_price
    
    def _prepare_features(self, date_num, distance, close_price):
        x_input = torch.tensor([[date_num, distance, close_price]], dtype=torch.float32)
        x_normalized = (x_input - self.X_mean) / self.X_std
        return x_normalized.to(device)

    def populate(self, interval=INTERVAL, sample_count=SAMPLE_COUNT):
        df = get_moving_average(self.ticker, interval)
        close_series = df[("Close", self.ticker)]
        sma_series = df[(f"{interval}-Day SMA", "")]
        distance = close_series - sma_series
        target = close_series.shift(-1)
        df2 = pd.DataFrame({
            "Close": close_series.values,
            "Distance": distance.values,
            "Target": target.values
        }, index=df.index)
        df2 = df2.dropna()
        self.reference_date = df2.index[0]
        df2["DateNum"] = (df2.index - self.reference_date).days
        X = df2[["DateNum", "Distance", "Close"]].values.astype(float)
        y = df2["Target"].values.astype(float).reshape(-1, 1)
        if sample_count and sample_count < len(df2):
            X = X[-sample_count:]
            y = y[-sample_count:]
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)
        X_tensor = self._normalize_features(X_tensor)
        return X_tensor, y_tensor

    def predict(self, target_date: str, interval: int = INTERVAL):
        if self.X_mean is None or self.X_std is None:
            raise ValueError("Model must be populated before making predictions")
        if self.reference_date is None:
            raise ValueError("Reference date not set. Run populate() first.")
        target_date_ts = pd.Timestamp(target_date)
        try:
            close_price = self._fetch_close_price_from_api()
            df = get_moving_average(self.ticker, interval)
            if df.empty:
                raise ValueError("No historical data available to calculate SMA.")
            latest_sma = df.iloc[-1][(f"{interval}-Day SMA", "")]
            #print(f"Using latest SMA ({df.index[-1].strftime('%Y-%m-%d')}): {latest_sma:.2f}")
            distance = close_price - latest_sma
            date_num = (target_date_ts - self.reference_date).days
            #print(f"Predicting for date: {target_date}, DateNum: {date_num}")
            x_normalized = self._prepare_features(date_num, distance, close_price)
            self.eval()
            with torch.no_grad():
                pred_normalized = self(x_normalized)
            pred = self._denormalize_prediction(pred_normalized)
            return pred.item()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")


def train_model(model, train_loader, test_loader, y_test, optimizer, loss_fn, 
                epochs=MAX_ITER, patience=PATIENCE):
    best_loss = float('inf')
    epochs_no_improve = 0
    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = loss_fn(pred, y_batch)
            loss.backward()
            optimizer.step()
        model.eval()
        test_loss_total = 0.0
        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                test_pred = model(X_batch)
                test_loss_total += loss_fn(test_pred, y_batch).item() * X_batch.size(0)
        test_loss_avg = test_loss_total / len(y_test)
        if test_loss_avg < best_loss:
            best_loss = test_loss_avg
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                print(f"Early stopping at epoch {epoch}")
                break
        if epoch % patience == 0:
            print(f"Epoch {epoch}: Test Loss = {test_loss_avg:.4f}")
    print(f"Training complete. Best Test Loss: {best_loss:.4f}")
    return best_loss


def create_model(ticker: str = TICKER):
    model = LinearRegression(ticker=ticker, api_base_url=API_BASE_URL).to(device)
    optimizer = optim.SGD(model.parameters(), lr=LR, momentum=MOMENTUM)
    loss_fn = nn.MSELoss()
    # Populate data
    X, y = model.populate()
    # Split data
    split_idx = int(len(X) * TRAIN_RATIO)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    # Normalize targets
    y_train_scaled = model._normalize_targets(y_train)
    y_test_scaled = (y_test - model.y_mean) / model.y_std
    # Create data loaders
    train_loader = DataLoader(
        TensorDataset(X_train, y_train_scaled), 
        batch_size=BATCH_SIZE, 
        shuffle=True
    )
    test_loader = DataLoader(
        TensorDataset(X_test, y_test_scaled), 
        batch_size=BATCH_SIZE
    )
    train_model(model, train_loader, test_loader, y_test, optimizer, loss_fn)    
    save_model(model, model.get_dir())
    return model

#TESTING:
#if __name__ == "__main__":
#    model = create_model(TICKER)
#    target_date = (pd.Timestamp.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
#    pred = model.predict(target_date=target_date)
#    print(f"Prediction for {TICKER} on {target_date}: ${pred:.2f}")