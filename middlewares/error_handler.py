from typing import Any, Coroutine
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)


    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
            # return await super().dispatch(request, call_next)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})