import csv
import requests
import sqlite3  # for our sql db
import time

import streamlit as st

st.title("Bitcoin Data")


#  get_bitcoin_price() - retrieves current btc price and timestamp from coin gecko api
#  input : None
#  return : formatted bitcoin data from coin gecko
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


#  write_to_csv : writes prices and timestamp to a csv file
#  input : 'file_path' - CSV filepath, 'timestamp' - timestamp of current price, 'price' - current btc price
#  return : none
def write_to_csv(file_path, timestamp, bitcoin_price):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, bitcoin_price])


#  init_sql : creates our database if it does not exist already
#  input : 'dbName' - Name of SQL database
#  return : none
def init_sql(dbName):
    conn = sqlite3.connect(dbName)  # make connection
    curs = conn.cursor()
    curs.execute('''
        CREATE TABLE IF NOT EXISTS bitcoin_prices (
            Timestamp TEXT,
            Bitcoin_Price_USD REAL
        )
    ''')
    conn.commit()
    conn.close()


#  write_sql : writes prices and timestamp to the sql table
#  input : 'dbName' - SQLite database, 'timestamp' - timestamp of current price, 'price' - current btc price
#  return : none
def write_sql(dbName, timestamp, price):
    conn = sqlite3.connect(dbName)
    curs = conn.cursor()
    curs.execute('''
        INSERT INTO bitcoin_prices (Timestamp, Bitcoin_Price_USD)
        VALUES (?, ?)
    ''', (timestamp, price))
    conn.commit()
    conn.close()


#  Main : main method - the loop
#  input : None
#  return : None
def main():
    dbName = 'bitcoin_prices'

    # init sql db
    init_sql(dbName)

    # setup columns
    col1, col2 = st.columns(2)

    # placeholders so we dont render new elements everytime
    best_price = col2.empty()
    worst_price = col2.empty()
    ave_price = col2.empty()

    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        bitcoin_price = get_bitcoin_price()

        if bitcoin_price is not None:
            col1.write(f"{timestamp} - Bitcoin Price (USD): {bitcoin_price}")  # write data on left
            write_sql(dbName, timestamp, bitcoin_price)  # write the data to the db

            # hookup to the db
            conn = sqlite3.connect(dbName)
            curs = conn.cursor()

            # grab highest value
            curs.execute("SELECT MAX(Bitcoin_Price_USD), Timestamp FROM bitcoin_prices")
            max_price, max_timestamp = curs.fetchone()

            # grab lowest value
            curs.execute("SELECT MIN(Bitcoin_Price_USD), Timestamp FROM bitcoin_prices")
            min_price, min_timestamp = curs.fetchone()

            # grab average value
            curs.execute("SELECT AVG(Bitcoin_Price_USD), Timestamp FROM bitcoin_prices")
            avg_price = curs.fetchone()[0]  # grab just index 0 for price

            # grab first time stamp for records
            curs.execute("SELECT Timestamp FROM bitcoin_prices ORDER BY Timestamp ASC LIMIT 1")
            first_log = curs.fetchone()[0]

            # disconnect
            conn.close()

            # display results in column 2
            best_price.metric("Best Price (USD)", f"{max_price:.2f}", max_timestamp)
            worst_price.metric("Worst Price (USD)", f"{min_price:.2f}", min_timestamp)
            ave_price.metric(f"Average Price (USD) since {first_log}", f"{avg_price:.2f}")

        time.sleep(10)  # Sleep for 60 seconds (adjust as needed)


if __name__ == "__main__":
    main()
