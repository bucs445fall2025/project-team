import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
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
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(3, 1)

    def forward(self, x):
        return self.linear(x)

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
        df2["DateNum"] = (df2.index - df2.index[0]).days
        X = df2[["DateNum", "Distance", "Close"]].values.astype(float)
        y = df2["Target"].values.astype(float).reshape(-1, 1)
        if sample_count and sample_count < len(df2):
            X = X[-sample_count:]
            y = y[-sample_count:]
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)
        # Normalize features
        X_mean = X_tensor.mean(dim=0, keepdim=True)
        X_std = X_tensor.std(dim=0, keepdim=True)
        X_tensor = (X_tensor - X_mean) / X_std
        return X_tensor, y_tensor

model = LinearRegression().to(device)
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=LR, momentum=MOMENTUM)
X, y = model.populate()

# Train/test split
split_idx = int(len(X) * TRAIN_RATIO)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]
# Y normalization
y_mean = y_train.mean(dim=0, keepdim=True)
y_std = y_train.std(dim=0, keepdim=True)
y_train_scaled = (y_train - y_mean) / y_std
y_test_scaled = (y_test - y_mean) / y_std

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