# Importing logging configuration handler and Alembic context setup modules
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context



# Getting the Alembic config object
config = context.config



# Loading the logging configuration from the .ini file 
if config.config_file_name is not None:
    fileConfig(config.config_file_name)



# Adding the project directory to the system path to resolve app module imports
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# Importing SQLAlchemy Base and all ORM models for schema autogeneration
from app.Database import Base
from app.models import User, Role, Task, Report, Project, ProjectUser



# Setting metadata target for Alembic to use during migration autogeneration
target_metadata = Base.metadata



# Running migrations in offline mode (without DB connection)
def run_migrations_offline() -> None:
    """Running migrations in 'offline' mode.

    Configuring the context with just a URL and not an Engine.
    Emitting SQL statements via context.execute().
    """
    
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()



# Running migrations in online mode (with active DB connection)
def run_migrations_online() -> None:
    """Running migrations in 'online' mode.

    Creating a SQLAlchemy engine and using it to run migration commands.
    """
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()



# Checking if Alembic is in offline mode and running appropriate migration function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
