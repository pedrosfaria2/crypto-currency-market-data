from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import Config, TestConfig

# Create a base class for declarative class definitions
Base = declarative_base()

# Create a new SQLAlchemy engine instance for the main database
engine = create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False})

# Create a new SQLAlchemy engine instance for the test database
test_engine = create_engine(TestConfig.DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class for the main database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a configured "Session" class for the test database
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_db():
    """
    Dependency that provides a SQLAlchemy session for the main database.

    This function creates a new database session, provides it to the caller,
    and ensures it is closed after use.

    Yields:
        sqlalchemy.orm.Session: A SQLAlchemy session object.

    Usage:
        Used in FastAPI dependency injection for route handlers.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db():
    """
    Dependency that provides a SQLAlchemy session for the test database.

    This function creates a new database session, provides it to the caller,
    and ensures it is closed after use.

    Yields:
        sqlalchemy.orm.Session: A SQLAlchemy session object.

    Usage:
        Used in tests for dependency injection.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
