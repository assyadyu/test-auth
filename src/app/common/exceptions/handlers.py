import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.common.exceptions.exceptions import (
    ObjectDoesNotExistException,
    UsernameAlreadyRegisteredException,
    EmailAlreadyRegisteredException,
    InvalidTokenException,
)


def object_does_not_exist_exception_handler(request: Request, exc: ObjectDoesNotExistException):
    message = exc.args[0]
    logging.error(f"URL: {request.url} MESSAGE: {message}")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": message})


def auth_errors_handler(
        request: Request,
        exc: [UsernameAlreadyRegisteredException, EmailAlreadyRegisteredException, InvalidTokenException]
):
    message = exc.args[0]
    logging.error(f"URL: {request.url} MESSAGE: {message}")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
