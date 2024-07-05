import time
from app.database import engine, SessionLocal
from app.fetch_data import fetch_symbols
from app.workers import display_symbols, store_symbols, subscribe_market_data, display_market_data

def init_db():
    """
    Initializes the database by creating all the tables defined in the models.

    This function uses SQLAlchemy's metadata to create all tables that are defined
    in the Base model. It binds these tables to the engine, which is configured
    to connect to the database.
    
    Args:
        None

    Returns:
        None
    """
    from app.models import Base
    Base.metadata.create_all(bind=engine)

def main_menu():
    """
    Displays the main menu and handles user choices.

    This function enters a loop that continually displays a menu with options
    to view symbols, subscribe to market data, or exit the program. It prompts
    the user for input and calls the appropriate function based on the user's choice.
    
    Args:
        None

    Returns:
        None
    """
    # Dictionary mapping user choices to corresponding handler functions.
    menu_options = {
        '1': handle_view_symbols,
        '2': handle_subscribe_market_data,
        '3': handle_view_market_data,
        '4': exit
    }

    while True:
        # Display the main menu.
        print("\nMain Menu")
        print("1. Consult and view available symbols")
        print("2. Subscribe to market data")
        print("3. View stored market data")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        # Get the action corresponding to the user's choice. If the choice is invalid, use handle_invalid_choice.
        action = menu_options.get(choice, handle_invalid_choice)
        action()

def handle_view_symbols():
    """
    Fetches and stores available symbols, then displays them.

    This function first fetches symbol data from an external API. It then
    stores this data in the database and finally displays the stored symbols
    in a tabulated format.

    Args:
        None

    Returns:
        None
    """
    # Fetch symbol data from the API.
    symbols_data = fetch_symbols()
    # Store the symbols in the database.
    store_symbols(symbols_data)
    # Display the stored symbols.
    display_symbols()

def handle_subscribe_market_data():
    """
    Prompts the user for a symbol and subscribes to receive market data for it.

    This function asks the user to input a symbol for which they want to receive
    market data. It then calls the function to subscribe to market data updates
    for that symbol, displaying the data as it is received.

    Args:
        None

    Returns:
        None
    """
    symbol = input("Enter the symbol to subscribe for market data: ")
    print("-" * 90)
    # Subscribe to receive market data for the provided symbol.
    subscribe_market_data(symbol)

def handle_view_market_data():
    """
    Displays the stored market data.

    This function fetches and displays the market data stored in the database
    in a tabulated format.

    Args:
        None

    Returns:
        None
    """
    display_market_data()

def handle_invalid_choice():
    """
    Informs the user that the choice is invalid.

    This function is called when the user makes a choice that is not
    recognized by the main menu. It simply prints an error message.

    Args:
        None

    Returns:
        None
    """
    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Initialize the database.
    init_db()
    # Start the main menu.
    main_menu()
