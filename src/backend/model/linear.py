import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import requests
from utils.moving_average import get_moving_average

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
API_BASE_URL = "http://localhost:8000"  # Your FastAPI server

device = torch.device("cpu")
# gpu support
if GPU_TRAIN:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("CUDA available:", torch.cuda.is_available())
    print("Device:", torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU only")
else:
    print("GPU training disabled, using CPU only")

class LinearRegression(nn.Module):
    def __init__(self, api_base_url=API_BASE_URL):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(3, 1)
        # Store normalization parameters
        self.X_mean = None
        self.X_std = None
        self.y_mean = None
        self.y_std = None
        self.api_base_url = api_base_url
        self.reference_date = None

    def forward(self, x):
        return self.linear(x)
    
    def _normalize_features(self, X_tensor):
        """Normalize features using stored mean and std."""
        if self.X_mean is None or self.X_std is None:
            # Compute and store normalization parameters
            self.X_mean = X_tensor.mean(dim=0, keepdim=True)
            self.X_std = X_tensor.std(dim=0, keepdim=True)
        return (X_tensor - self.X_mean) / self.X_std
    
    def _normalize_targets(self, y_train):
        """Normalize target values and store parameters."""
        self.y_mean = y_train.mean(dim=0, keepdim=True)
        self.y_std = y_train.std(dim=0, keepdim=True)
        return (y_train - self.y_mean) / self.y_std
    
    def _denormalize_prediction(self, pred_normalized):
        """Denormalize a prediction using stored parameters."""
        if self.y_mean is not None and self.y_std is not None:
            return pred_normalized * self.y_std + self.y_mean
        return pred_normalized
    
    def _fetch_close_price_from_api(self, symbol):
        """Fetch current close price from API with fallback options."""
        response = requests.get(f"{self.api_base_url}/api/v1/stock/{symbol}")
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch stock data: {response.text}")
        
        stock_info = response.json()
        
        # Try specific endpoint first
        close_price_response = requests.get(
            f"{self.api_base_url}/api/v1/stock/{symbol}/currentPrice"
        )
        
        if close_price_response.status_code == 200:
            return close_price_response.json()
        
        # Fallback to stock info fields
        close_price = (stock_info.get("currentPrice") or 
                      stock_info.get("regularMarketPrice") or 
                      stock_info.get("previousClose"))
        
        if close_price is None:
            raise ValueError("Could not retrieve close price from API")
        
        return close_price
    
    def _get_nearest_date(self, df, target_date):
        """Find the nearest available date in the dataframe."""
        target_date_ts = pd.Timestamp(target_date)
        
        if target_date_ts not in df.index:
            nearest_idx = df.index.get_indexer([target_date_ts], method='nearest')[0]
            target_date_ts = df.index[nearest_idx]
            print(f"Using nearest date: {target_date_ts}")
        
        return target_date_ts
    
    def _prepare_features(self, date_num, distance, close_price):
        """Prepare and normalize input features for prediction."""
        x_input = torch.tensor([[date_num, distance, close_price]], dtype=torch.float32)
        x_normalized = (x_input - self.X_mean) / self.X_std
        return x_normalized.to(device)

    def populate(self, ticker=TICKER, interval=INTERVAL, sample_count=SAMPLE_COUNT):
        df = get_moving_average(ticker, interval)
        close_series = df[("Close", ticker)]
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

    def predict(self, symbol: str, target_date: str, interval: int=INTERVAL):
        """
        Predict the next day's close price using API data.
        
        Args:
            symbol (str): Stock ticker symbol
            target_date (str): The date to predict from (format: "YYYY-MM-DD")
            interval (int): Moving average interval
            
        Returns:
            float: Predicted next day's close price (denormalized)
        """
        if self.X_mean is None or self.X_std is None:
            raise ValueError("Model must be populated before making predictions")
        
        if self.reference_date is None:
            raise ValueError("Reference date not set. Run populate() first.")
        
        try:
            # Fetch stock info from API
            response = requests.get(f"{self.api_base_url}/api/v1/stock/{symbol}")
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch stock data: {response.text}")
            stock_info = response.json()            
            close_price_response = requests.get(
                f"{self.api_base_url}/api/v1/stock/{symbol}/currentPrice"
            )
            if close_price_response.status_code == 200:
                close_price = close_price_response.json()
            else:
                # Fallback: use regularMarketPrice or previousClose
                close_price = stock_info.get("currentPrice") or \
                             stock_info.get("regularMarketPrice") or \
                             stock_info.get("previousClose")
            if close_price is None:
                raise ValueError("Could not retrieve close price from API")            
            df = get_moving_average(symbol, interval)            
            target_date_ts = pd.Timestamp(target_date)            
            if target_date_ts not in df.index:
                # Find nearest date
                nearest_idx = df.index.get_indexer([target_date_ts], method='nearest')[0]
                target_date_ts = df.index[nearest_idx]
                print(f"Using nearest date: {target_date_ts}")
            # Get SMA for the target date
            sma = df.loc[target_date_ts, (f"{interval}-Day SMA", "")]            
            close_from_df = df.loc[target_date_ts, ("Close", symbol)]            
            distance = close_price - sma            
            date_num = (target_date_ts - self.reference_date).days
            x_input = torch.tensor([[date_num, distance, close_price]], dtype=torch.float32)
            # Normalize input
            x_normalized = (x_input - self.X_mean) / self.X_std
            x_normalized = x_normalized.to(device)
            # Make prediction
            self.eval()
            with torch.no_grad():
                pred_normalized = self(x_normalized)            
            if self.y_mean is not None and self.y_std is not None:
                pred = pred_normalized * self.y_std + self.y_mean
            else:
                pred = pred_normalized
            return pred.item()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")

model = LinearRegression(api_base_url=API_BASE_URL).to(device)
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=LR, momentum=MOMENTUM)
X, y = model.populate()

# Train/test split
split_idx = int(len(X) * TRAIN_RATIO)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# Y normalization using helper function
y_train_scaled = model._normalize_targets(y_train)
y_test_scaled = (y_test - model.y_mean) / model.y_std

# DataLoaders
train_loader = DataLoader(TensorDataset(X_train, y_train_scaled), batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test, y_test_scaled), batch_size=BATCH_SIZE)

# Early Stopping
best_loss = float('inf')
epochs_no_improve = 0
early_stop = False

for epoch in range(MAX_ITER):
    if early_stop:
        print(f"Early stopping at epoch {epoch}")
        break
	# Train Set
    model.train()
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        pred = model(X_batch)
        loss = loss_fn(pred, y_batch)
        loss.backward()
        optimizer.step()
    # Test Set
    model.eval()
    test_loss_total = 0.0
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            test_pred = model(X_batch)
            test_loss_total += loss_fn(test_pred, y_batch).item() * X_batch.size(0)
    test_loss_avg = test_loss_total / len(y_test)
    # Early Stopping
    if test_loss_avg < best_loss:
        best_loss = test_loss_avg
        epochs_no_improve = 0
    else:
        epochs_no_improve += 1
        if epochs_no_improve >= PATIENCE:
            early_stop = True

    if epoch % PATIENCE == 0 or early_stop:
        print(f"Epoch {epoch}: Test Loss = {test_loss_avg:.4f}")

print("Training complete. Best Test Loss:", best_loss)

# Example usage with API:
# predicted_price = model.predict(symbol="AAPL", target_date="2024-01-15")
# print(f"Predicted next day close: ${predicted_price:.2f}")