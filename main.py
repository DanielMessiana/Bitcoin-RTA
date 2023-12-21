import numpy as np
import pandas as pd
import streamlit as st
import time, requests, csv

st.title("Bitcoin Data")


def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        bitcoin_price = data['bitcoin']['usd']
        return bitcoin_price
    except Exception as e:
        print(f"Error: {e}")
        return None

def write_to_csv(file_path, timestamp, bitcoin_price):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, bitcoin_price])

def main():
    file_path = 'bitcoin_prices.csv'

    # Write header to CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Bitcoin Price (USD)'])

    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        bitcoin_price = get_bitcoin_price()

        if bitcoin_price is not None:
            f"{timestamp} - Bitcoin Price (USD): {bitcoin_price}"
            write_to_csv(file_path, timestamp, bitcoin_price)

        time.sleep(10)  # Sleep for 60 seconds (adjust as needed)

if __name__ == "__main__":
    main()
