"""
Database configuration and session management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment or default SQLite
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./attrition.db')

# Configure engine based on database type
if DATABASE_URL.startswith('sqlite'):
    # For SQLite, use StaticPool to work with threading
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # For PostgreSQL or other databases
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Test connections before using
        echo=False,  # Set to True for SQL logging
    )

# Create SessionLocal for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    """
    Dependency injection for database session.
    Usage: db = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def reset_db():
    """
    Drop all tables (use with caution!).
    """
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped")
