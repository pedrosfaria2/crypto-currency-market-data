import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Symbol, MarketData
from app.config import TestConfig

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up class-level resources.

        This method is called once for the class. It creates a database engine
        and sets up the database schema based on the models defined in `Base`.
        """
        cls.engine = create_engine(TestConfig.DATABASE_URL, connect_args={"check_same_thread": False})
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class-level resources.

        This method is called once for the class. It drops the database schema
        to clean up the database after all tests have run.
        """
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        """
        Set up resources before each test.

        This method is called before every test method. It creates a new database
        session to ensure that each test runs in isolation.
        """
        self.db = self.Session()

    def tearDown(self):
        """
        Clean up resources after each test.

        This method is called after every test method. It closes the database
        session to release resources and ensure isolation between tests.
        """
        self.db.close()

    def test_symbol_creation(self):
        """
        Test the creation of a `Symbol` entry in the database.

        This test creates a new `Symbol` entry, adds it to the session, commits
        the transaction, and then retrieves the entry to verify that it was
        created correctly.
        """
        symbol = Symbol(
            base_currency='BTC',
            currency='BRL',
            symbol='BTC-BRL',
            description='Bitcoin to BRL',
            exchange_listed=True,
            exchange_traded=True,
            min_movement='1',
            price_scale=1000.0,
            session_regular='24x7',
            timezone='UTC',
            type='CRYPTO',
            deposit_minimum=0.01,
            withdraw_minimum=0.01,
            withdrawal_fee=0.001
        )
        self.db.add(symbol)
        self.db.commit()
        retrieved = self.db.query(Symbol).filter_by(symbol='BTC-BRL').first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.symbol, 'BTC-BRL')

if __name__ == '__main__':
    unittest.main()
