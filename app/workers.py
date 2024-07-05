import time
from app.database import SessionLocal
from app.fetch_data import fetch_market_data
from app.models import Symbol, MarketData

def safe_float(value):
    """
    Converts a value to float, returning 0.0 if the conversion fails.

    Args:
        value (str): The value to convert.

    Returns:
        float: The converted float value, or 0.0 if conversion fails.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def store_symbols(data):
    """
    Stores symbol data in the database.

    Args:
        data (dict): The symbol data to store. Expected keys include 'base-currency', 
                     'currency', 'symbol', 'description', 'exchange-listed', 
                     'exchange-traded', 'minmovement', 'pricescale', 'session-regular', 
                     'timezone', 'type', 'deposit-minimum', 'withdraw-minimum', 'withdrawal-fee'.
    """
    symbols_stored = 0
    with SessionLocal() as db:
        for i in range(len(data['base-currency'])):
            symbol = data['symbol'][i]
            if not db.query(Symbol).filter_by(symbol=symbol).first():
                symbol_entry = Symbol(
                    base_currency=data['base-currency'][i],
                    currency=data['currency'][i],
                    symbol=symbol,
                    description=data['description'][i],
                    exchange_listed=data['exchange-listed'][i],
                    exchange_traded=data['exchange-traded'][i],
                    min_movement=data['minmovement'][i],
                    price_scale=safe_float(data['pricescale'][i]),
                    session_regular=data['session-regular'][i],
                    timezone=data['timezone'][i],
                    type=data['type'][i],
                    deposit_minimum=safe_float(data['deposit-minimum'][i]),
                    withdraw_minimum=safe_float(data['withdraw-minimum'][i]),
                    withdrawal_fee=safe_float(data['withdrawal-fee'][i])
                )
                print(f"Storing symbol: {symbol}")
                db.add(symbol_entry)
                symbols_stored += 1
        db.commit()
    print(f"Stored {symbols_stored} symbols.")

def store_market_data(data):
    """
    Stores market data in the database and returns the created MarketData objects.

    Args:
        data (list of dict): The market data to store. 

    Returns:
        list: A list of MarketData objects that were created.
    """
    market_data_objects = []

    with SessionLocal() as db:
        try:
            for item in data:
                market_data = MarketData(
                    symbol=item['pair'],
                    buy=safe_float(item['buy']),
                    sell=safe_float(item['sell']),
                    high=safe_float(item['high']),
                    low=safe_float(item['low']),
                    open=safe_float(item['open']),
                    last=safe_float(item['last']),
                    volume=safe_float(item['vol']),
                    date=int(item['date'])
                )

                db.add(market_data)
                market_data_objects.append(market_data)

            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error occurred: {e}")

    return market_data_objects

def print_market_data(market_data_list):
    """
    Prints market data in a tabular format.

    Args:
        market_data_list (list of list): The market data to print. Each inner list contains 
                                         'symbol', 'buy', 'sell', 'high', 'low', 'open', 'last', 'volume', 'date'.
    """
    for item in market_data_list:
        print(f"{item[0]:<10} | {item[1]:<10} | {item[2]:<10} | {item[3]:<10} | {item[4]:<10} | {item[5]:<10} | {item[6]:<10} | {item[7]:<10} | {item[8]}")

def display_symbols():
    """
    Displays symbols stored in the database in a tabular format.
    """
    with SessionLocal() as db:
        symbols = db.query(Symbol).order_by(Symbol.symbol).all()
    
    if not symbols:
        print("No symbols available.")
    else:
        headers = ["Symbol", "Description"]
        print(f"{headers[0]:<10} | {headers[1]:<40}")
        print("-" * 51)
        for symbol in symbols:
            print(f"{symbol.symbol:<10} | {symbol.description:<40}")

def display_market_data():
    """
    Displays market data stored in the database in a tabular format.
    """
    with SessionLocal() as db:
        market_data = db.query(MarketData).order_by(MarketData.date).all()

    if not market_data:
        print("No market data available.")
    else:
        headers = ["Symbol", "Buy", "Sell", "High", "Low", "Open", "Last", "Volume", "Date"]
        print(f"{headers[0]:<10} {headers[1]:<10} {headers[2]:<10} {headers[3]:<10} {headers[4]:<10} {headers[5]:<10} {headers[6]:<10} {headers[7]:<10} {headers[8]}")
        print("-" * 90)
        for data in market_data:
            print(f"{data.symbol:<10} {data.buy:<10} {data.sell:<10} {data.high:<10} {data.low:<10} {data.open:<10} {data.last:<10} {data.volume:<10} {data.date}")

def subscribe_market_data(symbol):
    """
    Subscribes to market data for a specific symbol and continuously fetches and stores the data.

    Args:
        symbol (str): The symbol to subscribe to for market data.
    """
    print("Symbol     | Buy        | Sell       | High       | Low        | Open       | Last       | Volume     | Date")
    print("-" * 90)
    while True:
        try:
            market_data = fetch_market_data([symbol])
            market_data_list = [
                [
                    item['pair'],
                    item['buy'],
                    item['sell'],
                    item['high'],
                    item['low'],
                    item['open'],
                    item['last'],
                    item['vol'],
                    item['date']
                ]
                for item in market_data
            ]
            print_market_data(market_data_list)
            store_market_data(market_data)
            time.sleep(1)  # Wait 1 second before fetching data again
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  # Wait 1 second before trying again
