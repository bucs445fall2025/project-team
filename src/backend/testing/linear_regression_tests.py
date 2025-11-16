from utils.predictors import run_all_predictions, save_sp500
from utils.purge_old_models import purge_old_models
#save_sp500()
purge_old_models("cached_models/", "11-06-2025")
run_all_predictions()