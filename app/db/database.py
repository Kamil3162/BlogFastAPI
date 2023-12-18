from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def connection_checker():
    connection = engine.connect()
    print(connection.info)

def execute_db_migrations():
    print("db migrations execute")
    Base.metadata.create_all(bind=engine)

# def list_tables():
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     inspector = inspect(engine)
#     all_tables = inspector.get_table_names()
#     print(all_tables)