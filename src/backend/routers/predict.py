from fastapi import APIRouter
from db import get_prediction
from routers.stock_router import get_current_price


router = APIRouter()


@router.get("/predict/{ticker}")
async def get_predictions(ticker: str):
	currPrice = await get_current_price(ticker)
	linear_prediction = float(get_prediction(ticker)[3])

	last_price = currPrice['last_price'] if 'last_price' in currPrice else linear_prediction

	percent_diff = (linear_prediction - last_price) / last_price

	toReturn = {
		"recommendation": "HOLD",
		"current_price": last_price,
		"predictions": []
	}

	if percent_diff > 0.02:
		toReturn["recommendation"] = "BUY"
	elif percent_diff < -0.02:
		toReturn["recommendation"] = "SELL"
	toReturn["predictions"].append({
		"model_name": "Linear Regression",
		"predicted_price": linear_prediction
	})

	return toReturn


