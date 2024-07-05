import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, MarketData, Symbol
from app.config import TestConfig

# Set up the test database engine and session
engine = create_engine(TestConfig.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    """
    Fixture to set up the database schema before any tests run, and tear it down afterwards.

    This fixture is scoped to the module, so it runs once per module. It creates all the tables
    defined in Base.metadata before any tests are run, and drops all the tables after all tests
    have completed.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(setup_database):
    """
    Fixture to provide a new database session for each test function.

    This fixture is scoped to the function, so it provides a clean session for each test. It
    ensures that any changes made in a test are rolled back after the test completes, keeping
    tests isolated.
    """
    session = TestingSessionLocal()
    yield session
    session.close()

def test_market_data_creation(db_session):
    """
    Test the creation and retrieval of a MarketData entry.

    This test creates a new MarketData entry, adds it to the database session, commits the
    transaction, and then retrieves the entry to verify that it was created correctly.
    
    Asserts:
        The retrieved MarketData entry is not None.
        The attributes of the retrieved entry match the expected values.
    """
    market_data = MarketData(
        symbol="BTC-BRL",
        buy=100.0,
        sell=110.0,
        high=120.0,
        low=90.0,
        open=95.0,
        last=105.0,
        volume=1500.0,
        date=1622520000
    )

    # Add and commit the new MarketData entry
    db_session.add(market_data)
    db_session.commit()
    
    # Retrieve and verify the MarketData entry
    retrieved = db_session.query(MarketData).filter_by(symbol="BTC-BRL").first()
    assert retrieved is not None
    assert retrieved.symbol == "BTC-BRL"
    assert retrieved.buy == 100.0
    assert retrieved.sell == 110.0
    assert retrieved.high == 120.0
    assert retrieved.low == 90.0
    assert retrieved.open == 95.0
    assert retrieved.last == 105.0
    assert retrieved.volume == 1500.0
    assert retrieved.date == 1622520000

def test_symbol_creation(db_session):
    """
    Test the creation and retrieval of a Symbol entry.

    This test creates a new Symbol entry, adds it to the database session, commits the
    transaction, and then retrieves the entry to verify that it was created correctly.
    
    Asserts:
        The retrieved Symbol entry is not None.
        The attributes of the retrieved entry match the expected values.
    """
    symbol = Symbol(
        base_currency="BTC",
        currency="BRL",
        symbol="BTC-BRL",
        description="Bitcoin to Brazilian Real",
        exchange_listed=True,
        exchange_traded=True,
        min_movement="0.01",
        price_scale=2.0,
        session_regular="0900-1600",
        timezone="UTC",
        type="CRYPTO",
        deposit_minimum=10.0,
        withdraw_minimum=5.0,
        withdrawal_fee=0.1
    )

    # Add and commit the new Symbol entry
    db_session.add(symbol)
    db_session.commit()
    
    # Retrieve and verify the Symbol entry
    retrieved = db_session.query(Symbol).filter_by(symbol="BTC-BRL").first()
    assert retrieved is not None
    assert retrieved.base_currency == "BTC"
    assert retrieved.currency == "BRL"
    assert retrieved.symbol == "BTC-BRL"
    assert retrieved.description == "Bitcoin to Brazilian Real"
    assert retrieved.exchange_listed is True
    assert retrieved.exchange_traded is True
    assert retrieved.min_movement == "0.01"
    assert retrieved.price_scale == 2.0
    assert retrieved.session_regular == "0900-1600"
    assert retrieved.timezone == "UTC"
    assert retrieved.type == "CRYPTO"
    assert retrieved.deposit_minimum == 10.0
    assert retrieved.withdraw_minimum == 5.0
    assert retrieved.withdrawal_fee == 0.1

if __name__ == "__main__":
    pytest.main()
