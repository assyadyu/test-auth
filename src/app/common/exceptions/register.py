import fastapi as fa

from app.common.exceptions.exceptions import (
    ObjectDoesNotExistException,
    UsernameAlreadyRegisteredException,
    EmailAlreadyRegisteredException,
    InvalidTokenException,
)
from app.common.exceptions.handlers import (
    object_does_not_exist_exception_handler,
    auth_errors_handler,
)


def register_exception_handler(app: fa.FastAPI):
    app.add_exception_handler(ObjectDoesNotExistException, object_does_not_exist_exception_handler)
    app.add_exception_handler(UsernameAlreadyRegisteredException, auth_errors_handler)
    app.add_exception_handler(EmailAlreadyRegisteredException, auth_errors_handler)
    app.add_exception_handler(InvalidTokenException, auth_errors_handler)
