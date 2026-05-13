import logging
import traceback
from typing import Awaitable, Callable

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import AppError

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Catches unhandled exceptions and returns a consistent JSON error body."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            return await call_next(request)
        except (StarletteHTTPException, RequestValidationError):
            raise
        except AppError as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": exc.message,
                    "code": exc.code,
                },
            )
        except Exception as exc:  # noqa: BLE001 — intentional last-resort handler
            logger.exception("Unhandled error: %s", exc)
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "code": "INTERNAL_ERROR",
                    "trace": traceback.format_exc() if _expose_trace(request) else None,
                },
            )


def _expose_trace(request: Request) -> bool:
    return request.app.debug is True
