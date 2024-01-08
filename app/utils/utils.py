import os
from BlogFastAPI.app.db.database import SessionLocal
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from .responses import HTTP_EXCEPTION
from ..db.models.models import RevokedToken
from dotenv import load_dotenv
from pathlib import Path

config_file = Path(__file__).parent.parent / 'config.env'
load_dotenv(config_file)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, str(os.getenv("SECRET_KEY")),
                          algorithms=["HS256"])
    except JWTError:
        raise HTTP_EXCEPTION


# Function to add a revoked token to the database
def revoke_token(db: Session, token: str):
    try:
        db_blocked_token = RevokedToken(token=token)
        db.add(db_blocked_token)
        db.commit()
        db.refresh(db_blocked_token)
        return db_blocked_token
    except Exception as e:
        # Handle the exception here or log it
        db.rollback()  # Rollback the transaction in case of an error
        raise e  # Reraise the exception to propagate it or log it