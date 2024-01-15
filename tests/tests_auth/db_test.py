import pytest
from BlogFastAPI.app.db.database import SessionLocal
from BlogFastAPI.app.core.config import Settings
from BlogFastAPI.app.db.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DB_URL = f"postgresql://postgres:admin@localhost:5432/BlogTestDB"
SQLALCHEMY_DATABASE_TEST_URL = DB_URL


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL)
    Base.metadata.create_all(engine)  # Create tables if they don't exist

    # Create a sessionmaker
    testing_session_local = sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine)

    # Start a transaction
    session = testing_session_local()
    transaction = session.begin()

    yield session

    # Rollback and close the session after the test
    transaction.rollback()
    session.close()