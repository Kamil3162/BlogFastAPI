import datetime

from pydantic import ValidationError
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

def setup_server_exc_handler(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ) -> JSONResponse:
        print(exc)
        print(exc.status_code)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "detail": exc.detail,
                "error_code": f"HTTP_{exc.status_code}",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "test": "test msg"
            }
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": "Data validation error",
                "error_code": "VALIDATION_ERROR",
                "detail": exc.errors(),
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        )

