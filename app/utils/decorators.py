from sqlalchemy.exc import SQLAlchemyError
from BlogFastAPI.app.utils.deps import CustomHTTPExceptions


def check_db_operations(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
    return wrapper

