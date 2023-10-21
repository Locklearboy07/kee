import bitmart
import talib
from bitmart.api_spot import APISpot

api_key = "039c26c7f5316ab9891ed924b3a4885bf35c70fe"
secret_key = "866cee39cb5a66816c815ee46481530f4d6b984bcf8eb9f9676715ee46fe2e37"
memo = "5"
url = "https://api-cloud.bitmart.com/spot/v1/ticker_detail"

api = APISpot(api_key, secret_key, memo, url)

# Function to get the current price of the BNT/USDT trading pair
def get_current_price():
    ticker = api.get_ticker('BNT_USDT')
    return ticker['data']['last_price']

# Function to calculate the moving average of the BNT/USDT pair
def calculate_moving_average():
    prices = api.get_candlestick('BNT_USDT', '1h', 21)
    close_prices = [float(price['close']) for price in prices['data']]
    moving_average = talib.SMA(close_prices, timeperiod=20)
    return moving_average[-1]

# Function to calculate the upper and lower Bollinger Bands of the BNT/USDT pair
def calculate_bollinger_bands():
    prices = api.get_candlestick('BNT_USDT', '1h', 21)
    close_prices = [float(price['close']) for price in prices['data']]
    upper_band, middle_band, lower_band = talib.BBANDS(close_prices, timeperiod=20)
    return upper_band[-1], middle_band[-1], lower_band[-1]

# Function to place a buy order for BNT at the specified price
def buy_BNT(price):
    api.create_order('BNT_USDT', 'limit', 'buy', price, '10')

# Function to place a sell order for BNT at the specified price
def sell_BNT(price):
    api.create_order('BNT_USDT', 'limit', 'sell', price, '10')

# Main function to monitor the price, moving average, and Bollinger Bands and execute buy/sell orders accordingly
def main():
    price = get_current_price()
    moving_average = calculate_moving_average()
    upper_band, middle_band, lower_band = calculate_bollinger_bands()

    while True:
        price = get_current_price()
        moving_average = calculate_moving_average()
        upper_band, middle_band, lower_band = calculate_bollinger_bands()

        if price > upper_band:
            sell_BNT(price)
        elif price < lower_band:
            buy_BNT(price)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()