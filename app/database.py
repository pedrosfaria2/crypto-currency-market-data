from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config, TestConfig
from sqlalchemy.orm import declarative_base
Base = declarative_base()


# Create a new SQLAlchemy engine instance
engine = create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False})
test_engine = create_engine(TestConfig.DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create a base class for declarative class definitions
Base = declarative_base()

def get_db():
    """
    Dependency that provides a SQLAlchemy session.

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
