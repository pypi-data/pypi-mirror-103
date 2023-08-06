from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException):
    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": None
    }, status_code=200)
