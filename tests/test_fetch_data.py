import unittest
from unittest.mock import patch
import urllib3
from app.fetch_data import fetch_symbols, fetch_market_data

class TestFetchData(unittest.TestCase):
    """
    Unit tests for the functions in `fetch_data.py`.

    This class contains tests to ensure that the `fetch_symbols` and 
    `fetch_market_data` functions behave as expected when interacting with
    external APIs.
    """

    @patch('app.fetch_data.requests.get')
    def test_fetch_symbols(self, mock_get):
        """
        Test `fetch_symbols` function.

        This test verifies that the `fetch_symbols` function correctly handles
        the response from an API call. It uses `unittest.mock.patch` to mock
        the `requests.get` method, simulating a successful API response with
        specific data. The test then checks if the returned data contains
        the expected keys.
        
        Args:
            mock_get (MagicMock): Mock object for `requests.get`.
        """
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"base-currency": ["BTC"], "symbol": ["BTC-BRL"]}

        # Call the function to test
        data = fetch_symbols()
        
        # Assertions to ensure the returned data is as expected
        self.assertIn("base-currency", data)
        self.assertIn("symbol", data)

    @patch('app.fetch_data.requests.get')
    def test_fetch_market_data(self, mock_get):
        """
        Test `fetch_market_data` function.

        This test verifies that the `fetch_market_data` function correctly handles
        the response from an API call. It uses `unittest.mock.patch` to mock
        the `requests.get` method, simulating a successful API response with
        specific data. The test then checks if the returned data matches the
        expected structure and content.
        
        Args:
            mock_get (MagicMock): Mock object for `requests.get`.
        """
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "pair": "BTC-BRL",
                "buy": "30000",
                "sell": "31000",
                "high": "32000",
                "low": "29000",
                "open": "30500",
                "last": "31000",
                "vol": "10",
                "date": "1720182706"
            }
        ]

        # Call the function to test
        data = fetch_market_data(["BTC-BRL"])
        
        # Assertions to ensure the returned data is as expected
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pair"], "BTC-BRL")

if __name__ == '__main__':
    unittest.main()
