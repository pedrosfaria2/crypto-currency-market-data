import pytest
import timeit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Symbol, MarketData  # Importing database models
from app.config import TestConfig  # Importing test configuration
from app.fetch_data import fetch_symbols, fetch_market_data  # Importing data fetching functions
from app.workers import store_symbols, store_market_data  # Importing data storing functions

# Database configuration for tests
engine = create_engine(TestConfig.DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    """
    Fixture to set up the database before any test is run,
    and clean it up after all tests have been completed.
    """
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables in the database
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(setup_database):
    """
    Fixture to provide a new database session for each test function.
    """
    session = TestingSessionLocal()
    yield session
    session.rollback()  # Rollback any changes after the test
    session.close()  # Close the session

def test_fetch_symbols_performance():
    """
    Performance test for the fetch_symbols function.
    Measures the time taken to fetch symbols.
    """
    execution_time = timeit.timeit(fetch_symbols, number=10)
    print(f"Execution time for fetch_symbols: {execution_time:.4f} seconds")
    # Adjust the time limit as necessary
    assert execution_time < 2, "fetch_symbols test is taking longer than expected."

def test_store_symbols_performance(db_session):
    """
    Performance test for the store_symbols function.
    Measures the time taken to store symbols in the database.
    """
    # Clear tables before the test
    db_session.query(Symbol).delete()
    db_session.commit()

    # Fetch symbol data
    symbols_data = fetch_symbols()

    # Measure the time to store symbols
    start_time = timeit.default_timer()
    store_symbols(symbols_data)
    db_session.commit()
    execution_time = timeit.default_timer() - start_time
    print(f"Execution time for store_symbols: {execution_time:.4f} seconds")
    # Adjust the time limit as necessary
    assert execution_time < 2, "store_symbols test is taking longer than expected."

def test_fetch_market_data_performance():
    """
    Performance test for the fetch_market_data function.
    Measures the time taken to fetch market data.
    """
    symbols = ["BTC-BRL"]
    execution_time = timeit.timeit(lambda: fetch_market_data(symbols), number=10)
    print(f"Execution time for fetch_market_data: {execution_time:.4f} seconds")
    # Adjust the time limit as necessary
    assert execution_time < 2, "fetch_market_data test is taking longer than expected."

def test_store_market_data_performance(db_session):
    """
    Performance test for the store_market_data function.
    Measures the time taken to store market data in the database.
    """
    # Clear tables before the test
    db_session.query(MarketData).delete()
    db_session.commit()

    # Fetch market data
    symbols = ["BTC-BRL"]
    market_data = fetch_market_data(symbols)

    # Measure the time to store market data
    start_time = timeit.default_timer()
    store_market_data(market_data)
    db_session.commit()
    execution_time = timeit.default_timer() - start_time
    print(f"Execution time for store_market_data: {execution_time:.4f} seconds")
    # Adjust the time limit as necessary
    assert execution_time < 2, "store_market_data test is taking longer than expected."
