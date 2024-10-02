from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, \
    RequestResponseEndpoint
from starlette.responses import RedirectResponse, Response


class DocsBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define the condition for allowing access to the docs
        # This example checks for a specific token in the query params
        # You can adapt this to your authentication mechanism

        device_type = request.headers.get('Device-Type')

        allowed_token = "secret_token"
        request_token = request.query_params.get("token")

        if request.url.path in ["/docs",
                                "/redoc"] and request_token != allowed_token:
            return RedirectResponse(url='/')

        response = await call_next(request)
        return response