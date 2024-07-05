from dotenv import load_dotenv
import os

# Load environment variables from a .env file into the environment.
load_dotenv()

class Config:
    """
    Configuration class to hold environment variables for the application.

    This class loads and provides access to configuration values, such as
    the database URL and the API URL, from environment variables. These
    values are typically stored in a .env file for security and convenience.

    Attributes:
        DATABASE_URL (str): The URL for the database connection, loaded from
                            the environment variable "DATABASE_URL".
        API_URL (str): The base URL for the API, loaded from the environment
                       variable "API_URL".
    """

    # The URL for the database connection.
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # The base URL for the API.
    API_URL = os.getenv("API_URL")

class TestConfig(Config):
    """
    Configuration class to hold environment variables for the test environment.

    This class extends the Config class and overrides specific configuration
    values for the test environment, such as the database URL.

    Attributes:
        DATABASE_URL (str): The URL for the test database connection, loaded
                            from the environment variable "TEST_DATABASE_URL".
    """
    # Override the database URL for the test environment
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")
