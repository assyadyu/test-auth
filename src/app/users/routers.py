from fastapi import (
    APIRouter,
    Depends,
)

from app.users.schemas import (
    UserSignupSchema,
    UserSigninSchema,
    UserSchema,
    TokenSchema,
    TokenPayload,

)
from app.users.services import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/signup", response_model=UserSchema)
async def signup(
        request_data: UserSignupSchema,
        service: UserService = Depends(),
):
    return await service.create_user(request_data)


@user_router.post("/signin", response_model=TokenSchema)
async def signin(
        request_data: UserSigninSchema,
        service: UserService = Depends(),
):
    return await service.signin_user(request_data)


@user_router.post("/validate", response_model=TokenPayload)
async def validate(
        request_data: TokenSchema,
        service: UserService = Depends(),
):
    return await service.validate_token(request_data)
