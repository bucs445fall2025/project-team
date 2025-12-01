# Pelosi's Stash
## CS 445 Final Project
### Fall, 2025

### Team: 😃
- Brendon Paolino
- Michael Zheng
- Gavin Suber

### Software Requirement Specification
[Link to google doc here](https://docs.google.com/document/d/1DFohPjYLa29_scmMElGaCI5ZswPOue50vu_ada64PMI/edit?usp=drivesdk)
## Getting Started
- This is a stock prediction app/website. We are not liable for any financial decisions that you make based on our data. You will find the true stock prices and our predictions for the future for each of the S&P500 stocks as well as a daily summary on how the stock is performing. We do not guarantee the accuracy of any of these predictions. If you are going to invest in the stock market, you can use this app as a tool to gather more information, but nobody can truly predict the future.

### Roadmap
- [ ] Add More Models
  
### Prerequisites
* [Docker](https://www.docker.com/)
* [NextJS](https://nextjs.org/)

### Installing
  - Download project files
  - Ensure Docker is running, run (in src/backend):  
    `docker build -t stock_prediction_app .`  
    `docker run [-detatch] stock_prediction_app`
    (the detatch argument is optional-- only use if you want to run in a separate terminal)
  - Then go to src/frontend, make sure npm is installed, run:  
    `npm run dev`
### Creating Models (predictors.py)
  - Run the function `save_sp500(count, file_path, model_type)` to create and train models for the S&P 500.
  - Use `run_prediction(file_path, ticker, input, device, insert_to_db)` to predict from a single model.
  - Use `run_all_predictions(file_path, input_date, model_type, device)` to predict from all available models of a certain type (e.g. LINEAR)

## Built With
* [PyTorch](https://pytorch.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [NextJS](https://nextjs.org/)
* [requests](https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request) - request for humans

## License
GPL-3.0 license

## Acknowledgments
* 😃
