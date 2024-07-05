import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Symbol, MarketData
from app.config import TestConfig
from app.fetch_data import fetch_symbols, fetch_market_data
from app.workers import store_symbols, store_market_data

# Database configuration for tests
engine = create_engine(TestConfig.DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    """
    Fixture to set up the database before any test is run,
    and clean it up after all tests have been completed.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(setup_database):
    """
    Fixture to provide a new database session for each test function.
    """
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.mark.benchmark(group="fetch_symbols")
def test_benchmark_fetch_symbols(benchmark):
    """
    Benchmark for fetch_symbols function.
    """
    result = benchmark(fetch_symbols)
    assert result is not None

@pytest.mark.benchmark(group="store_symbols")
def test_benchmark_store_symbols(benchmark, db_session):
    """
    Benchmark for store_symbols function.
    """
    db_session.query(Symbol).delete()
    db_session.commit()
    symbols_data = fetch_symbols()

    def store():
        store_symbols(symbols_data)
        db_session.commit()

    benchmark(store)

@pytest.mark.benchmark(group="fetch_market_data")
def test_benchmark_fetch_market_data(benchmark):
    """
    Benchmark for fetch_market_data function.
    """
    symbols = ["BTC-BRL"]
    result = benchmark(lambda: fetch_market_data(symbols))
    assert result is not None

@pytest.mark.benchmark(group="store_market_data")
def test_benchmark_store_market_data(benchmark, db_session):
    """
    Benchmark for store_market_data function.
    """
    db_session.query(MarketData).delete()
    db_session.commit()
    symbols = ["BTC-BRL"]
    market_data = fetch_market_data(symbols)

    def store():
        store_market_data(market_data)
        db_session.commit()

    benchmark(store)
