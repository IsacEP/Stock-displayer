
import matplotlib.pyplot as plt
import pandas as pd
import requests

ALPHA_VANTAGE_API_KEY = 'API KEY'

def get_user_input(prompt):
    return input(prompt).strip()

def get_alpha_vantage_data(symbol):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()['Time Series (Daily)']
        df = pd.DataFrame(data).T
        df.index = pd.to_datetime(df.index)
        df['Close'] = pd.to_numeric(df['4. close'])
        return df[['Close']]
    except requests.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def plot_graph(stock_data, stock_name):
    plt.figure(figsize=(10, 8))
    plt.plot(stock_data.index, stock_data['Close'], 'r-', label=stock_name)
    plt.title(f"Stock Price for {stock_name}")
    plt.ylabel("Price per share (USD)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def main():
    while True:
        user_stock = get_user_input("Enter stock symbol (e.g., AAPL, MSFT, GOOGL), or type 'exit' to quit: ").upper()

        if user_stock == 'EXIT':
            print("Exiting program. Goodbye!")
            break

        stock_data = get_alpha_vantage_data(user_stock)

        if not stock_data.empty:
            plot_graph(stock_data, user_stock)
        else:
            print("Unable to fetch stock data. Please check the symbol or try again later.")

if __name__ == "__main__":
    main()
