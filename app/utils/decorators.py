from sqlalchemy.exc import SQLAlchemyError
from .deps import CustomHTTPExceptions

def check_db_operations(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exceptiopn(e)
    return wrapper

