import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Ensure the Alembic migration tool can find the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base  # Import the Base from your models

# Get the Alembic configuration object, which provides access to the .ini file
config = context.config

# Set up Python logging using the configuration file
fileConfig(config.config_file_name)

# MetaData object for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    
    In this mode, Alembic generates SQL scripts without connecting to the database.
    This is useful for environments where database access is restricted.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Run migrations in 'online' mode.
    
    In this mode, Alembic connects to the database and applies migrations directly.
    This method requires database access and is useful for development and deployment.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Determine if Alembic should run migrations in 'offline' or 'online' mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
