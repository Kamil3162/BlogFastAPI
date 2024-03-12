from sqlalchemy.exc import SQLAlchemyError
from BlogFastAPI.app.utils.exceptions_functions import CustomHTTPExceptions


def check_db_operations(func):
    def wrapper(*args, **kwargs):
        try:
            print("decorator execution")
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)

    return wrapper

def check_data_key(func):
    def wrapper(*args, **kwargs):
        try:
            print("check key error")
            return func(*args, **kwargs)
        except KeyError:
            CustomHTTPExceptions.not_found()
    return wrapper

def check_db_delete(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)

    return wrapper
