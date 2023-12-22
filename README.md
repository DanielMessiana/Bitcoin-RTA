# Overview #
This project is a real-time Bitcoin price analysis tool that uses streamlit to visualize data from the CoinGecko API. It records each price along with its timestamp in a SQLite database and displays the highest, lowest, and average Bitcoin prices since the first recorded entry.

This is an early iteration and serves as a foundation for future work. 

![image](https://github.com/DanielMessiana/Bitcoin-RTA/assets/63567335/0dbf59fc-012a-4529-ac4e-cb271a7ff9a3)

# Features #
- Fetch real-time Bitcoin prices from the CoinGecko API.
- Record and display Bitcoin prices with timestamps.
- Show metrics for the highest, lowest, and average prices.
- Utilizes Streamlit for a clean streamlined web interface
- Store data in a SQLite database for persistence and analysis.

# Usage #
Currently this tool allows for the live viewing of BTC in USD. Next we will plot the data and start attmepting to make predictions.

## Prereqs ##
- Python 3.x
- pip

# Planned features #
- Data Visualization: Implementation of live plotting to visualize Bitcoin price trends over time using plotly or matplotlib.
- Price Prediction: Integration of machine learning models for predicting future Bitcoin prices based on collected data.
