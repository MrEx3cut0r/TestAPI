import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.domain.exceptions.domain_exceptions import DomainException

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            raise http_exc
        except DomainException as domain_exc:
            logger.warning(f"Domain exception: {str(domain_exc)}")
            return JSONResponse(
                status_code=400,
                content={
                    "detail": str(domain_exc),
                    "error_code": type(domain_exc).__name__
                }
            )
        except Exception as exc:
            logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_code": "INTERNAL_SERVER_ERROR"
                }
            )