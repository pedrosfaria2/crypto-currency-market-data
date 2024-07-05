import threading
import textwrap
import time
import signal
from app.database import engine
from app.fetch_data import fetch_symbols
from app.workers import display_symbols, store_symbols, subscribe_market_data, display_market_data

def init_db():
    """
    Initializes the database by creating all the tables defined in the models.
    """
    from app.models import Base
    Base.metadata.create_all(bind=engine)

# Event to signal stopping the market data subscription
stop_event = threading.Event()

def main_menu():
    """
    Displays the main menu and handles user choices.
    """
    menu_options = {
        '1': handle_view_symbols,
        '2': handle_subscribe_market_data,
        '3': handle_view_market_data,
        '4': exit
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        action = menu_options.get(choice, handle_invalid_choice)
        action()

def print_menu():
    """
    Prints the main menu.
    """
    print(textwrap.dedent("""
        Main Menu
        1. Consult and view available symbols
        2. Subscribe to market data. Press CTRL + C to stop the subscription.
        3. View stored market data
        4. Exit
    """))

def handle_view_symbols():
    """
    Fetches and stores available symbols, then displays them.
    """
    print("\nFetching and storing symbols...")
    symbols_data = fetch_symbols()
    store_symbols(symbols_data)
    display_symbols()

def handle_subscribe_market_data():
    """
    Handles the user's request to subscribe to market data for a specific symbol.

    This function does the following:
    1. Prompts the user to enter the desired symbol.
    2. Clears the global `stop_event` flag, indicating that the subscription should start.
    3. Creates a new daemon thread (`subscription_thread`) to run the `subscribe_market_data` function.
       - Daemon threads are automatically terminated when the main program exits.
    4. Starts the subscription thread.
    5. Enters a loop that waits for the user to press Ctrl+C (KeyboardInterrupt).
    6. If Ctrl+C is pressed, the following happens:
       - Sets the `stop_event` flag to signal the subscription thread to stop.
       - Waits for the `subscription_thread` to finish using `join()`.
       - Prints a message indicating that the subscription has been stopped.
    7. After the subscription thread has finished (either by stopping or error), the main menu is re-displayed.
    """

    global subscription_thread  # Access the global subscription_thread variable

    symbol = input("Enter the symbol to subscribe for market data: ")
    print(textwrap.fill(f"Subscribing to market data for symbol: {symbol}", width=70))
    print("-" * 90)

    # Clear the stop event before starting a new subscription
    stop_event.clear()

    # Create and start a new thread for the subscription
    subscription_thread = threading.Thread(target=subscribe_market_data, args=(symbol, stop_event))
    subscription_thread.daemon = True  # Set as a daemon thread
    subscription_thread.start()

    try:
        # Wait for the user to press Ctrl+C to stop the subscription
        while subscription_thread.is_alive():  # Continue while the thread is alive
            time.sleep(1)
    except KeyboardInterrupt:
        # Signal the subscription thread to stop and wait for it to finish
        stop_event.set()
        subscription_thread.join()
        print("\nMarket data subscription stopped.")


def handle_view_market_data():
    """
    Displays the stored market data.
    """
    print("\nDisplaying stored market data...")
    display_market_data()

def handle_stop_subscription():
    """
    Signals the subscription thread to stop.
    """
    stop_event.set()
    print("\nMarket data subscription stopped.")

def handle_invalid_choice():
    """
    Informs the user that the choice is invalid.
    """
    print(textwrap.fill("Invalid choice. Please try again.", width=70))

if __name__ == "__main__":
    init_db()
    signal.signal(signal.SIGINT, lambda sig, frame: handle_stop_subscription())
    main_menu()
