from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware, \
    RequestResponseEndpoint
from BlogFastAPI.app.utils.deps import CustomHTTPExceptions
from starlette.responses import Response


class DataBaseErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except SQLAlchemyError as e:
            return CustomHTTPExceptions.handle_db_exceptiopn(e)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"Detail": "An unexpected error occured"}
            )






