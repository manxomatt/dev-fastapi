import time
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.request")


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.time()
        try:
            response = await call_next(request)
            elapsed = (time.time() - start) * 1000
            logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({elapsed:.2f}ms)")
            return response
        except Exception as exc:  # log and re-raise
            elapsed = (time.time() - start) * 1000
            logger.error(f"{request.method} {request.url.path} -> 500 ERROR ({elapsed:.2f}ms) - {exc}")
            raise
