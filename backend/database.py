from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from config import settings

# Create engine (NullPool disables connection pooling for dev, easier to reset)
engine = create_engine(
    settings.database_url,
    echo=settings.sqlalchemy_echo,
    poolclass=NullPool if settings.environment == "development" else None,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """Dependency injection for FastAPI routes to get a DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Run this once on startup in development."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all tables. Careful with this."""
    Base.metadata.drop_all(bind=engine)
