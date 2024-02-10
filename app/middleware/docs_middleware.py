from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, \
    RequestResponseEndpoint
from starlette.responses import RedirectResponse, Response


class DocsBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define the condition for allowing access to the docs
        # This example checks for a specific token in the query params
        # You can adapt this to your authentication mechanism
        print(request.query_params)

        allowed_token = "secret_token"
        request_token = request.query_params.get("token")

        # Check if the path is for the docs or redoc and the token is not the allowed one
        if request.url.path in ["/docs",
                                "/redoc"] and request_token != allowed_token:
            # Here you can choose to either block access
            # return HTTPException(status_code=403, detail="Not allowed")
            # Or redirect the user to another page, for example, the homepage
            return RedirectResponse(url='/')

        # If the request does not try to access the docs or is allowed, proceed as normal
        response = await call_next(request)
        return response