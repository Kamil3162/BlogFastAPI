# First we import session to generate connection with out db
from sqlalchemy.orm import Session
from .session import engine
from .session import Base
from ..core.config import settings

def init_db() -> None:
    # Create all tables
    print("create db")
    Base.metadata.create_all(bind=engine)



