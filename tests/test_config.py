import unittest
from app.config import Config

class TestConfig(unittest.TestCase):
    def test_database_url(self):
        """
        Ensure the DATABASE_URL environment variable is not None.

        This test verifies that the DATABASE_URL, which is essential for database 
        connections, is loaded correctly from the environment variables. If this 
        value is None, it indicates a misconfiguration or a missing environment variable.
        
        Asserts:
            Config.DATABASE_URL is not None.
        """
        self.assertIsNotNone(Config.DATABASE_URL, "DATABASE_URL should not be None")

    def test_api_url(self):
        """
        Ensure the API_URL environment variable is not None.

        This test checks that the API_URL, which is used as the base URL for API 
        requests, is properly loaded from the environment variables. A None value 
        would suggest a misconfiguration or a missing environment variable.
        
        Asserts:
            Config.API_URL is not None.
        """
        self.assertIsNotNone(Config.API_URL, "API_URL should not be None")

if __name__ == '__main__':
    unittest.main()
