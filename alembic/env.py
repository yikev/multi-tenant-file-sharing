import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the backend directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import your SQLAlchemy models and Base metadata
from app.models import Base
from app.config import settings  # Make sure this loads DATABASE_URL

# Alembic Config object
config = context.config

# Inject your DB URL into Alembic config
config.set_main_option(
    "sqlalchemy.url",
    "postgresql://multi_tenant_fs_user:uOCGvjHrrWJCkoKHDFJHtHSeAa0lQiSr@dpg-d1cehkidbo4c73cpqqqg-a.oregon-postgres.render.com/multi_tenant_fs"
)

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogeneration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()