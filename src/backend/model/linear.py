import torch
from torch.autograd import Variable
import numpy as np

MAX_ITER = 1000

# FEATURES: DATE, DISTANCE TO 50-DAY, PRICE

class LinearRegression(torch.nn.Module):
	def __init__(self):
		super(LinearRegression, self).__init__()
		self.linear = torch.nn.Linear(3, 1)

	def forward(self, x):
		return self.linear(x)
	
yf_model = LinearRegression()

loss_f = torch.nn.MSELoss(size_average=False)
optimizer = torch.optim.SGD(yf_model.parameters(), lr=.01)


def populate(sample_count):
	return

x_data = populate()
y_data = {}
for epoch in range(MAX_ITER):
	pred_y = yf_model(x_data)
	loss = loss_f(pred_y, y_data)

	optimizer.zero_grad()
	loss.backward()
	optimizer.step()