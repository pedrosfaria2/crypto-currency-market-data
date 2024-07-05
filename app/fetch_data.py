import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from .config import Config

# Disable security warnings for unverified HTTPS requests
disable_warnings(InsecureRequestWarning)

# API URL configuration using environment variables
API_URL = os.getenv("API_URL", Config.API_URL)

# Global session for reusing connections
session = requests.Session()

def fetch_symbols():
    """
    Fetches the list of available trading symbols from the API.

    This function makes a GET request to the API endpoint for symbols,
    handles the response, and returns the parsed JSON data.

    Returns:
        dict: A dictionary containing the symbol data fetched from the API.

    Raises:
        requests.RequestException: If there is an error during the HTTP request.
    """
    url = f"{API_URL}symbols"
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Parse and return JSON response
    except requests.RequestException as e:
        print(f"Error fetching symbols: {e}")
        raise

def fetch_market_data(symbols):
    """
    Fetches market data for the given list of symbols from the API.

    This function makes a GET request to the API endpoint for market data,
    handles the response, and returns the parsed JSON data.

    Args:
        symbols (list): A list of symbol strings (e.g., ["BTC-BRL", "ETH-BRL"]).

    Returns:
        list: A list of dictionaries containing market data for each symbol.

    Raises:
        requests.RequestException: If there is an error during the HTTP request.
    """
    url = f"{API_URL}tickers"
    params = {
        "symbols": ",".join(symbols)  # Join the list of symbols into a single comma-separated string
    }
    try:
        response = session.get(url, params=params, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Parse and return JSON response
    except requests.RequestException as e:
        print(f"Error fetching market data for symbols {symbols}: {e}")
        raise
