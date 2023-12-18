from db.database import SessionLocal
from jose import jwt
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )